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
    long_or_short = analyze_symbol(symbol)
    '''{'long': True, 'short': False}'''
    long = long_or_short['long']
    short = long_or_short['short']

    if long: 
        if weekly_rsi_over_high(symbol): return send_msg(f"{symbol.upper()}'s trend is good, but the weekly RSI is higher than 89, please be careful.", from_id)

        turnover_ratio_eth = get_turnover_ratio_from_coinmarketcap(coin='ETH')
        token_info = get_token_market_cap_and_ratio(symbol, turnover_ratio_eth)
        if token_info:
            '''{'market_cap': 153456101, 'fully_diluted_market_cap': 303272927, 'circulation_ratio': 0.51, 'turnover_ratio': 0.07}'''
            fully_diluted_market_cap = token_info['fully_diluted_market_cap']
            circulating_ratio = token_info['circulation_ratio']
            turnover_ratio = token_info['turnover_ratio']
            token_slug = token_info['token_slug']
            current_price = token_info['current_price']
            coin_rank = token_info['coin_rank']
            URL = f'https://coinmarketcap.com/currencies/{token_slug}/'
            reply_string = f"[{symbol}]({URL}) | Rank {coin_rank} | {format_number(current_price)} | {round(circulating_ratio, 2)} | {round(turnover_ratio, 2)}\nFully_Diluted_Market_Cap: {format_number(fully_diluted_market_cap)}"
            send_msg_markdown(reply_string, from_id)
            return send_msg(f"{symbol.upper()} is good to buy now.", from_id)
        else: send_msg(f"{symbol.upper()} is not good to buy because of one of below reasons:\n\n1. The coin is not listed in CoinMarketCap.\n2. The coin's market cap is less than {format_number(MARKET_CAP_DOWN_LIMIT)} or more than {format_number(FULLLY_DILUTED_MARKET_CAP_UP_LIMIT)}.\n3. The coin's turnover ratio is less than ETH's {format_number(turnover_ratio_eth)}.\n4. The coin's circulation ratio is less than {int(CIRCULATION_RATIO*100)}%.", from_id)

    elif short: return send_msg(f"{symbol.upper()} is good to short now.", from_id)

    return send_msg(f"{symbol.upper()} is not good to long or short now. Wait for the next chance. Be patient please 😘", from_id)


def is_coin_recently_listed(symbol: str, days=7):
    try: days = int(days)
    except: days = 7

    # Binance API endpoint for K-line data
    url = "https://api.binance.com/api/v3/klines"

    # if symbol is not endsweith 'USDT', add 'USDT' to the end, if symbol is endsweith USDT, do nothing
    if not symbol.endswith('USDT'): symbol = symbol + 'USDT'

    # Calculate timestamps for 7 days ago and now
    end_time = int(time.time() * 1000)  # Current time in milliseconds
    start_time = end_time - 24 * 60 * 60 * 1000 * days  # 7 days ago

    # Parameters for the API request
    params = {
        'symbol': symbol,
        'interval': '1d',  # Daily intervals
        'startTime': start_time,
        'endTime': end_time,
        'limit': days
    }

    # Send the request
    response = requests.get(url, params=params)
    
    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        if len(data) < days: 
            print(f'{symbol[:-4]} is recently listed in less than {days} days.')
            return True
        else: return False

    return True


def binance_today_hot_coins_check(chat_id=TG_BOT_OWNER_ID, user_nick_name='Dear', crontab=False, trading_volume_limit = TRADING_VOLUME_LIMIT, tradingbot_status = False):
    coin_in_positions = []
    try:
        df_auto_position = get_df_from_position_buy_table(None, 'binance_position_buy')
        df_manual_position = get_df_from_position_buy_table(None, 'binance_manually_buy')
        df_limit_buy_order = get_open_limit_orders(None, 'binance_limit_buy_order')
        if df_auto_position.shape[0] + df_manual_position.shape[0] + df_limit_buy_order.shape[0] >= POSITIONS_LIMIT:
            if not crontab: send_msg(f"{user_nick_name}, You have full positions already ({df_auto_position.shape[0] + df_manual_position.shape[0]}), please wait for some positions to be closed with profit, be patient please 😘\n\nOr, you can send '/set_position_limit 10' to reset the position limit to 10 or any other number. Or cancel some limit orders.", chat_id)
            return
        coin_in_positions = df_auto_position['coin'].values.tolist() + df_manual_position['coin'].values.tolist()
        if not df_auto_position.empty: 
            df_limit_buy_order['coin'] = df_limit_buy_order['symbol'].apply(lambda x: x[:-4])
            coin_in_positions += df_limit_buy_order['coin'].values.tolist()
    except: pass # if the table is not exist, ignore and wait for the next time to be created automatically
    REMAINING_POSITIONS = POSITIONS_LIMIT - (df_auto_position.shape[0] + df_manual_position.shape[0])
    today_hot_coin_dict = binance_today_hot_coin(trading_volume_limit, tradingbot_status, coin_in_positions)
    if not today_hot_coin_dict: return 
    for coin in today_hot_coin_dict:
        if REMAINING_POSITIONS <= 0: break
        if coin in coin_in_positions: continue
        if is_coin_recently_listed(coin, 7): 
            print(f'{coin} is recently listed, ignore.')
            continue
        try: 
            target_profit = float(today_hot_coin_dict[coin])
            do_market_buy_one_unit(coin, chat_id)
            binance_position_set_limit_sell(target_profit, chat_id, coin, table_name = 'binance_position_buy')
            REMAINING_POSITIONS -= 1
        except Exception as e: print(f'Failed to buy {coin} or set limit order...\n\n{e}')
    return


def only_check_hot_coins(from_id = None):
    tradingbot_status = trading_bot_switch_status()
    return binance_today_hot_coin(trading_volume_limit = TRADING_VOLUME_LIMIT, tradingbot_status = tradingbot_status, coin_in_positions=[])


if __name__ == '__main__':
    print('Start running Trading_bot.py ...')
