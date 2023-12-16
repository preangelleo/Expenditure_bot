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
                
            return {'market_cap': int(market_cap), 'fully_diluted_market_cap': int(fully_diluted_market_cap), 'circulation_ratio': circulating_ratio, 'turnover_ratio': turnover_ratio, 'token_slug': token_info['slug']}
    except: return 


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



def binance_today_hot_coin(trading_volume_limit = TRADING_VOLUME_LIMIT, only_check = False, from_id = TG_BOT_OWNER_ID):
    
    df_ticker = pd.read_json(BINANCE_TICKER_URL)

    # Keep symbol, priceChangePercent, lastPrice, openPrice, highPrice, lowPrice, volume, quoteVolume, openTime, closeTime
    df_ticker = df_ticker.loc[:, ['symbol', 'priceChangePercent', 'lastPrice', 'openPrice', 'highPrice', 'lowPrice', 'quoteVolume', 'openTime', 'closeTime']]

    # pick up the symbol endswith 'USDT'
    df_ticker = df_ticker[df_ticker['symbol'].str.endswith('USDT')]

    df_ticker = df_ticker[(df_ticker['priceChangePercent'] > 1) & (df_ticker['quoteVolume'] > trading_volume_limit) & (df_ticker['priceChangePercent'] < 20) & (df_ticker['lastPrice'] > 0.0001) & (df_ticker['lastPrice'] < 1000)]

    if df_ticker.empty:
        print(f"1) No hot coin today after filtering the coins with priceChangePercent > 1 and quoteVolume > {trading_volume_limit} and priceChangePercent < 20 and lastPrice between 0.0001 and 1000")
        if only_check: broadcast_text(f"No hot coin today after filtering the coins with 20% > priceChangePercent > 1% and quoteVolume > {format_number(trading_volume_limit)} and lastPrice between 0.0001 and 1000")
        return []

    # df_ticker = df_ticker.sort_values(by='quoteVolume', ascending=False)
    df_ticker['coin'] = df_ticker['symbol'].str[:-4]

    # Eliminate the coins with 'USD' in coin name
    df_ticker = df_ticker[~df_ticker['coin'].str.contains('USD')]

    # Eliminate the coins in IGNORE_LIST
    IGNORE_LIST = get_ignore_list()
    df_ticker = df_ticker[~df_ticker['coin'].isin(IGNORE_LIST)]

    if df_ticker.empty:
        print(f"2) No hot coin today after eliminating the coins in IGNORE_LIST")
        if only_check: broadcast_text(f"No hot coin today after eliminating the coins in IGNORE_LIST")
        return []
    
    # pd.DataFrame(engine.connect().execute(text('SELECT * FROM binance_position_buy')).fetchall())
    # from binance_position_buy find out the latested bought 30 coins
    try:
        df_30_days = pd.DataFrame(engine.connect().execute(text('SELECT coin FROM binance_position_buy ORDER BY transactTime Desc LIMIT 30')).fetchall())
        unique_coin_set = set(df_30_days['coin'].values.tolist())
    except: unique_coin_set = set()

    # try to read hot_coins from hot_coin_history table of only yesterday, not table not exist, make a [] list
    try: 
        df_hot_coin_history = pd.DataFrame(engine.connect().execute(text('SELECT * FROM hot_coin_history WHERE date > DATE_SUB(NOW(), INTERVAL 1 DAY)')).fetchall())
        yesterday_hot_coin_set = set(df_hot_coin_history['coin'].values.tolist())
    except: yesterday_hot_coin_set = set()

    # make a unique coin list of unique_coin_set and yesterday_hot_coin_set together
    unique_coin_list = list(unique_coin_set | yesterday_hot_coin_set)

    # Ignore the coins in unique_coin_list
    df_ticker = df_ticker[~df_ticker['coin'].isin(unique_coin_list)]
    if df_ticker.empty: 
        print(f"3) No hot coin today, after ignore the latest hot coin list: {unique_coin_list}")
        return []

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
            df_ticker.loc[index, 'token_slug'] = token_info['token_slug']
        else: df_ticker.drop(index, inplace=True)

    # Filter out the coins with market_cap between 100M and 5B
    df_ticker = df_ticker[(df_ticker['market_cap'] > 100_000_000) & (df_ticker['market_cap'] < 5_000_000_000)]

    if df_ticker.empty:
        print(f"4) No hot coin today after filtering the coins with market_cap between 100M and 5B and turnover_ratio > ETH's {turnover_ratio_eth} and circulation_ratio > {CIRCULATION_RATIO}")
        if only_check: broadcast_text(f"No hot coin today after filtering the coins with market_cap between 100M and 5B and turnover_ratio > ETH's {turnover_ratio_eth} and circulation_ratio > {CIRCULATION_RATIO}")
        return []

    # add a new column 'turnover_by_priceChangePercent' = turnover_ratio / priceChangePercent
    df_ticker['turnover_by_priceChangePercent'] = df_ticker['turnover_ratio'] / df_ticker['priceChangePercent']

    # sort by 'turnover_by_priceChangePercent' in descending order
    df_ticker = df_ticker.sort_values(by='turnover_by_priceChangePercent', ascending=False)

    # Keep the top 30 coins
    df_ticker = df_ticker.head(10)

    # make a coin list
    today_hot_coin_list = df_ticker['coin'].values.tolist()

    if today_hot_coin_list and only_check: 

        if from_id: send_msg(f"Today's hot coins are: {', '.join(today_hot_coin_list)}", from_id)

        counts_of_hot_coins = len(today_hot_coin_list)

        strategy_info = f'''STRATEGY: \n\nFiltering the coins with 'Daily Trading Volume' > {format_number(trading_volume_limit)} USD and PriceChangePercent between 1% ~ 20% and lastPrice between 0.0001 ~ 1000 and market_cap between 100M ~ 5B and turnover_ratio > ETH's {turnover_ratio_eth} and circulation_ratio > {int(CIRCULATION_RATIO*100)}%, then eliminate the coins in IGNORE_LIST and the coins in the latest 30 days positions and ignore yesterday's hot coins, then sort by 'turnover_ratio / priceChangePercent' in descending order and keep the top 10 coins. We got {counts_of_hot_coins} hot coin(s) for today.'''
        print(strategy_info)
        broadcast_text(strategy_info)

        i = 0
        for index, row in df_ticker.iterrows():
            i += 1
            coin = row['coin']
            price = row['lastPrice']
            priceChangePercent = row['priceChangePercent']
            turnover_ratio = row['turnover_ratio']
            turnover_by_priceChangePercent = row['turnover_by_priceChangePercent']
            token_slug = row['token_slug']
            URL = f'https://coinmarketcap.com/currencies/{token_slug}/'
            reply_string = f"{i}/{counts_of_hot_coins} [{coin}]({URL}) | +{priceChangePercent}% | {format_number(price)} | {round(turnover_ratio, 2)} | {round(turnover_by_priceChangePercent*100, 3)}"

            # make a dictionary of this coin and append to "hot_coin_history"
            hot_coin_history = {
                'coin': coin, 
                'priceChangePercent': priceChangePercent, 
                'price': price, 
                'turnover_ratio': turnover_ratio, 
                'turnover_by_priceChangePercent': turnover_by_priceChangePercent,
                'token_slug': token_slug,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                }

            # make dictionary to dataframe
            df_hot_coin_history = pd.DataFrame(hot_coin_history, index=[0])
            
            # append df_hot_coin_history to hot_coin_history table
            df_hot_coin_history.to_sql('hot_coin_history', engine, if_exists='append', index=False)

            # send_msg_markdown(reply_string, from_id)
            broadcast_markdown(reply_string)

    return today_hot_coin_list


def binance_today_hot_coins_check(chat_id=TG_BOT_OWNER_ID, user_nick_name='Dear', crontab=False, trading_volume_limit = TRADING_VOLUME_LIMIT):

    coin_in_positions = []
    try:
        # Check if there is any open position in binance_position_buy table, if yes, ignore this coin
        df_balance = pd.DataFrame(engine.connect().execute(text('SELECT * FROM binance_position_buy WHERE is_closed = 0')).fetchall())
        if df_balance.shape[0] >= POSITIONS_LIMIT: 
            if not crontab: send_msg(f"{user_nick_name}, You have full positions already ({df_balance.shape[0]}), please wait for some positions to be closed with profit, be patient please 😘\n\nOr, you can send '/set_position_limit 10' to reset the position limit to 10 or any other number.", chat_id)
            return
        coin_in_positions = df_balance['coin'].values.tolist()
    except: pass # if the table is not exist, ignore and wait for the next time to be created automatically
    
    today_hot_coin_list = binance_today_hot_coin(trading_volume_limit)
    if not today_hot_coin_list:
        if not crontab: send_msg(f"{user_nick_name}, Your current positions are {len(coin_in_positions)} out of {POSITIONS_LIMIT}, but there is no hot coin today, please wait with patience 😘", chat_id)
        return

    target_profit_in_db = read_target_profit_default()

    # compare target_profit_in_db with 0.01, if target_profit_in_db < 0.01, set target_profit_in_db = 0.01
    if target_profit_in_db < 0.01: target_profit_in_db = 0.01

    # query_list  = []
    for coin in today_hot_coin_list:

        # Check if coin in coin_in_positions, if yes, ignore this coin
        if coin in coin_in_positions: continue

        # Check if coin is recently listed, if yes, ignore this coin
        if is_coin_recently_listed(coin, 7): continue

        try: 
            do_market_buy_one_unit(coin, chat_id)
            binance_position_set_limit_sell(target_profit, chat_id, coin)
        except Exception as e: print(f'Failed to buy {coin} or set limit order...\n\n{e}')

    return


def only_check_hot_coins(from_id):
    return binance_today_hot_coin(trading_volume_limit = TRADING_VOLUME_LIMIT, only_check = True, from_id = from_id)



if __name__ == '__main__':
    print('Start running Trading_bot.py ...')
    # binance_today_hot_coin(trading_volume_limit = TRADING_VOLUME_LIMIT)

    # # Example usage
    # symbol = '1000SATSUSDT'  # Replace with the actual symbol you want to check
    # is_recent = is_coin_recently_listed(symbol, days=14)
    # print(f"Is {symbol} recently listed? {is_recent}")

    # symbol = 'WOO'  # Replace with the actual symbol you want to check
    # is_recent = is_coin_recently_listed(symbol, days=14)
    # print(f"Is {symbol} recently listed? {is_recent}")

    # df_hot_coin_history = pd.DataFrame(engine.connect().execute(text('SELECT * FROM hot_coin_history WHERE date > DATE_SUB(NOW(), INTERVAL 1 DAY)')).fetchall())
    # print(df_hot_coin_history)