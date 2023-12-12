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
- Exclusions: Coins in the ignore list or previously traded in the last 30 days are excluded.
- Market Cap Analysis: Fetches market cap and fully diluted market cap for each coin from CoinMarketCap. Coins are filtered based on their market cap, circulation ratio and turnover ratio.
- Selecting Top Coins: The top 30 coins are selected based on quote volume.
- Position Check: The binance_today_hot_coins_check function checks if the current number of open positions is below the POSITIONS_LIMIT. If not, no further action is taken.
- Coin Eligibility: For each eligible coin, the strategy checks if it is already in an open position. If not, it fetches price information from CoinMarketCap and send to trader.
- Trading: If the coin meets all criteria, a market buy order is placed with a size defined by CHECK_SIZE.
'''
# From the returned dictionary, get market_cap, fully_diluted_market_cap and calculate the circulating ratio
def get_token_market_cap_and_ratio(token_symbol, turnover_ratio_eth=None):
    if not turnover_ratio_eth: turnover_ratio_eth = get_turnover_ratio_from_coinmarketcap(coin='ETH')
    try:
        token_info = get_token_info_from_coinmarketcap(token_symbol)
        if token_info:
            market_cap = token_info['quote']['USD']['market_cap']
            fully_diluted_market_cap = token_info['quote']['USD']['fully_diluted_market_cap']
            if fully_diluted_market_cap > FULLLY_DILUTED_MARKET_CAP_UP_LIMIT: return
            if market_cap < MARKET_CAP_DOWN_LIMIT: return
            circulating_ratio = market_cap / fully_diluted_market_cap
            circulating_ratio = round(circulating_ratio, 2)
            if circulating_ratio < CIRCULATION_RATIO: return 
            # Calculate turnover ratio
            turnover_ratio = token_info['quote']['USD']['volume_24h'] / market_cap
            turnover_ratio = round(turnover_ratio, 2)
            if turnover_ratio < turnover_ratio_eth: return
                
            return {'market_cap': int(market_cap), 'fully_diluted_market_cap': int(fully_diluted_market_cap), 'circulation_ratio': circulating_ratio, 'turnover_ratio': turnover_ratio}
    except: return 


def binance_today_hot_coin(trading_volume_limit = TRADING_VOLUME_LIMIT, only_check = False, from_id = TG_BOT_OWNER_ID):
    
    # pd.DataFrame(engine.connect().execute(text('SELECT * FROM binance_position_buy')).fetchall())
    # from binance_position_buy find out the latested bought 30 coins
    df_30_days = pd.DataFrame(engine.connect().execute(text('SELECT coin FROM binance_position_buy ORDER BY transactTime Desc LIMIT 30')).fetchall())
    if df_30_days.empty: unique_coin_list = []
    else: unique_coin_list = list(set(df_30_days['coin'].values.tolist()))

    df_ticker = pd.read_json(BINANCE_TICKER_URL)

    # Keep symbol, priceChangePercent, lastPrice, openPrice, highPrice, lowPrice, volume, quoteVolume, openTime, closeTime
    df_ticker = df_ticker.loc[:, ['symbol', 'priceChangePercent', 'lastPrice', 'openPrice', 'highPrice', 'lowPrice', 'quoteVolume', 'openTime', 'closeTime']]

    # pick up the symbol endswith 'USDT'
    df_ticker = df_ticker[df_ticker['symbol'].str.endswith('USDT')]

    # Filter out the coins with priceChangePercent > 0 and quoteVolume > trading_volume_limit
    df_ticker = df_ticker[(df_ticker['priceChangePercent'] > 0) & (df_ticker['quoteVolume'] > trading_volume_limit)]

    # Filter out the coins with lastPrice between 0.0001 and 1000
    df_ticker = df_ticker[(df_ticker['lastPrice'] > 0.0001) & (df_ticker['lastPrice'] < 1000)]

    df_ticker = df_ticker.sort_values(by='quoteVolume', ascending=False)
    df_ticker['coin'] = df_ticker['symbol'].str[:-4]

    # Eliminate the coins with 'USD' in coin name
    df_ticker = df_ticker[~df_ticker['coin'].str.contains('USD')]

    # Eliminate the coins in IGNORE_LIST
    IGNORE_LIST = get_ignore_list()
    df_ticker = df_ticker[~df_ticker['coin'].isin(IGNORE_LIST)]

    # Ignore the coins in unique_coin_list
    df_ticker = df_ticker[~df_ticker['coin'].isin(unique_coin_list)]
    if df_ticker.empty: return []

    turnover_ratio_eth = get_turnover_ratio_from_coinmarketcap(coin='ETH')

    # Update ticker with market cap and fully diluted market cap
    df_ticker['market_cap'] = 0
    df_ticker['fully_diluted_market_cap'] = 0
    df_ticker['ratio'] = 0.01
    for index, row in df_ticker.iterrows():
        coin = row['coin']
        token_info = get_token_market_cap_and_ratio(coin, turnover_ratio_eth)
        if token_info:
            '''{'market_cap': 153456101, 'fully_diluted_market_cap': 303272927, 'circulation_ratio': 0.51, 'turnover_ratio': 0.07}'''
            df_ticker.loc[index, 'market_cap'] = int(token_info['market_cap'])
            df_ticker.loc[index, 'fully_diluted_market_cap'] = int(token_info['fully_diluted_market_cap'])
            df_ticker.loc[index, 'circulation_ratio'] = float(token_info['circulation_ratio'])
            df_ticker.loc[index, 'turnover_ratio'] = float(token_info['turnover_ratio'])
        else: df_ticker.drop(index, inplace=True)

    # Filter out the coins with market_cap between 100M and 10B
    df_ticker = df_ticker[(df_ticker['market_cap'] > 100_000_000) & (df_ticker['market_cap'] < 10_000_000_000)]

    # add a new column 'turnover_by_priceChangePercent' = turnover_ratio / priceChangePercent
    df_ticker['turnover_by_priceChangePercent'] = df_ticker['turnover_ratio'] / df_ticker['priceChangePercent']

    # sort by 'turnover_by_priceChangePercent' in descending order
    df_ticker = df_ticker.sort_values(by='turnover_by_priceChangePercent', ascending=False)

    print(df_ticker)

    # Keep the top 30 coins
    df_ticker = df_ticker.head(30)

    # make a coin list
    today_hot_coin_list = df_ticker['coin'].values.tolist()

    if today_hot_coin_list and only_check: 
        # make a reply string, format: "Coin | PriceChangePercent | QuoteVolume | TurnoverRatio | turnover_by_priceChangePercent"
        reply_string = ''
        for index, row in df_ticker.iterrows():
            coin = row['coin']
            priceChangePercent = row['priceChangePercent']
            turnover_ratio = row['turnover_ratio']
            turnover_by_priceChangePercent = row['turnover_by_priceChangePercent']
            reply_string += f"{coin} | +{priceChangePercent}% | {round(turnover_ratio, 2)} | {round(turnover_by_priceChangePercent, 3)}\n"
        
        help_info = '\nThe first number is rais percentage, the second number is the turnover ratio (trading volume / market cap), third number is the turnover_ratio / price_change.'
        send_msg(f"CHECK ONLY\nToday's hot coins are: \n\n{reply_string}{help_info}", from_id)

    return today_hot_coin_list


def binance_today_hot_coins_check(chat_id=TG_BOT_OWNER_ID, user_nick_name='Dear', crontab=False, trading_volume_limit = TRADING_VOLUME_LIMIT, check_size = CHECK_SIZE):

    coin_in_positions = []
    try:
        # Check if there is any open position in binance_position_buy table, if yes, ignore this coin
        df_balance = pd.DataFrame(engine.connect().execute(text('SELECT * FROM binance_position_buy WHERE is_closed = 0')).fetchall())
        if df_balance.shape[0] >= POSITIONS_LIMIT: 
            send_msg(f"{user_nick_name}, You have full positions already ({df_balance.shape[0]}), please wait for some positions to be closed with profit, be patient please 😘", chat_id)
            return
        coin_in_positions = df_balance['coin'].values.tolist()
    except: pass # if the table is not exist, ignore and wait for the next time to be created automatically
    
    today_hot_coin_list = binance_today_hot_coin(trading_volume_limit)
    if not today_hot_coin_list and not crontab: 
        send_msg(f"{user_nick_name}, Your current positions are {len(coin_in_positions)} our of {POSITIONS_LIMIT}, but there is no hot coin today, please wait with patience 😘", chat_id)
        return

    # query_list  = []
    for coin in today_hot_coin_list:

        # Check if coin in coin_in_positions, if yes, ignore this coin
        if coin in coin_in_positions: continue

        # Check coin information from coinmarketcap, if no information, ignore this coin
        if not get_token_price_from_coinmarketcap_and_send_msg(coin, chat_id=None): continue

        try: do_market_buy_one_unit(coin, chat_id)
        except Exception as e: send_msg(f"{user_nick_name}, Failed to buy {coin}...\n\n{e}", chat_id)

    if not crontab: send_msg('All done! 😘', chat_id)
    return


def only_check_hot_coins(from_id):
    return binance_today_hot_coin(trading_volume_limit = TRADING_VOLUME_LIMIT, only_check = True, from_id = from_id)

if __name__ == '__main__':
    print('Start running Trading_bot.py ...')
    binance_today_hot_coin(trading_volume_limit = TRADING_VOLUME_LIMIT)

