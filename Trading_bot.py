from Binance_api import *


'''COINMARKETCAP RETURN
{
"id": 3964,
"name": "Reserve Rights",
"symbol": "RSR",
"slug": "reserve-rights",
"num_market_pairs": 179,
"date_added": "2019-05-24T00:00:00.000Z",
"tags": [
    "store-of-value",
    "defi",
    "coinbase-ventures-portfolio",
    "dcg-portfolio",
    "real-world-assets"
],
"max_supply": 100000000000,
"circulating_supply": 50600000000,
"total_supply": 100000000000,
"platform": {
    "id": 1027,
    "name": "Ethereum",
    "symbol": "ETH",
    "slug": "ethereum",
    "token_address": "0x320623b8e4ff03373931769a31fc52a4e78b5d70"
},
"is_active": 1,
"infinite_supply": false,
"cmc_rank": 255,
"is_fiat": 0,
"self_reported_circulating_supply": null,
"self_reported_market_cap": null,
"tvl_ratio": null,
"last_updated": "2023-12-08T04:57:00.000Z",
"quote": {
    "USD": {
    "price": 0.003022959829617387,
    "volume_24h": 9627813.39949622,
    "volume_change_24h": -10.9172,
    "percent_change_1h": -0.3184558,
    "percent_change_24h": 1.89929244,
    "percent_change_7d": 7.74822681,
    "percent_change_30d": 23.45831876,
    "percent_change_60d": 67.36675515,
    "percent_change_90d": 63.50005519,
    "market_cap": 152961767.3786398,
    "market_cap_dominance": 0.0095,
    "fully_diluted_market_cap": 302295982.96,
    "tvl": null,
    "last_updated": "2023-12-08T04:57:00.000Z"
    }
}
}
{'market_cap': 152961767.3786398, 'fully_diluted_market_cap': 302295982.96, 'ratio': 0.5060000000029103}
'''

'''STRATEGY:
- Setting Limits: Define various limits such as TRADING_VOLUME_LIMIT, INITIAL_FUND, CHECK_SIZE, and POSITIONS_LIMIT.
- Fetching Market Data: Fetches market data from Binance for coins with a trading volume above TRADING_VOLUME_LIMIT. It filters coins based on several criteria including price change percentage, last price, and quote volume.
- Filtering Criteria: Coins are filtered to include only those with price change percent > 0, quote volume > TRADING_VOLUME_LIMIT, and last price within a specific range.
- Exclusions: Only trade coins in white list.
- Market Cap Analysis: Fetches market cap and fully diluted market cap for each coin from CoinMarketCap. Coins are filtered based on their market cap, circulation ratio and turnover ratio.
- Selecting Top Coins: The top 30 coins are selected based on quote volume.
- Position Check: The binance_today_hot_coins_check function checks if the current number of open positions is below the POSITIONS_LIMIT. If not, no further action is taken.
- Coin Eligibility: For each eligible coin, the strategy checks if it is already in an open position. If not, it fetches price information from CoinMarketCap and send to trader.
- Trading: If the coin meets all criteria, a market buy order is placed with a size defined by CHECK_SIZE.
'''
def analyze_symbol_for_user(symbol: str, from_id=TG_BOT_OWNER_ID):
    symbol = symbol.upper()
    if not symbol.endswith('USDT'): symbol = symbol + 'USDT'
    coin = symbol[:-4]
    calculate_missed_profit_for_coin(coin, from_id)
    data_dict = get_resistant_price(symbol, interval = '4h', for_webhook = True)
    if data_dict: send_msg('\n'.join([f"{key}: {format_number(value)}" for key, value in data_dict.items()]), from_id)
    get_token_info(coin, from_id)
    return


def only_check_hot_coins(from_id = None):
    tradingbot_status = trading_bot_switch_status()
    return binance_today_hot_coin(TRADING_VOLUME_LIMIT, tradingbot_status)


def get_webhook_signature(message: str, from_id=TG_BOT_OWNER_ID):
    token = hash_md5(message)
    data = {'token': token, 'is_used': 0, 'created_day': datetime.now().strftime("%Y-%m-%d"), 'created_time': datetime.now().strftime("%H:%M:%S"), 'message': message}
    data_to_table(data, 'webhook_signature')
    symbol = message.split(' ')[-1]
    data_dict = get_resistant_price(symbol, interval = '4h', for_webhook = True)
    if not data_dict: return send_msg(token, from_id)
    data_dict['token'] = token
    data_dict['message'] = message
    '''{'target_profit': format_number(target_profit), 'resistant_price': format_number(nearest_resistance_level), 'support_price': format_number(nearest_support_level), 'deviation_percentage': f"{format_number(deviation_percentage * 100)}%"}'''
    reply_string = '\n'.join([f"{key}: {format_number(value)}" for key, value in data_dict.items()])
    return send_msg(reply_string, from_id)


def validate_webhook_signature(token):
    message = None
    try:
        with engine.connect() as connection: df = pd.DataFrame(connection.execute(text(f"SELECT message FROM webhook_signature WHERE token = '{token}' AND is_used = 0")).fetchall())
        if not df.empty: message = df['message'].values[0]
    except: pass
    return message


def set_webhook_signature_used(token):
    try: 
        with engine.connect() as connection: connection.execute(text(f"UPDATE webhook_signature SET is_used = 1 WHERE token = '{token}'"))
        return True
    except: pass
    return


if __name__ == '__main__':
    print('Start running Trading_bot.py ...')
