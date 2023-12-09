from Binance_api import *


TRADING_VOLUME_LIMIT = int(os.getenv('TRADING_VOLUME_LIMIT', 50_000_000))
INITIAL_FUND = int(os.getenv('INITIAL_FUND', 100_000))
CHECK_SIZE = int(os.getenv('CHECK_SIZE', 10_000))
POSITIONS_LIMIT = int(INITIAL_FUND / CHECK_SIZE)
# print(f"TRADING_VOLUME_LIMIT: {TRADING_VOLUME_LIMIT}, INITIAL_FUND: {INITIAL_FUND}, CHECK_SIZE: {CHECK_SIZE}, POSITIONS_LIMIT: {POSITIONS_LIMIT}")


''' Strategy:
1. **Unique Coin List Creation**: The process begins by querying a database table named `binance_ticker_top_30`. This table provides a distinct list of coins that have been traded in the last 30 days. In instances where this table is non-existent or empty, the fallback is an empty list.

2. **Data Acquisition and Initial Filtering**: The next step involves fetching the latest ticker data from Binance's API. This data is then filtered to focus on symbols that end with 'USDT'. Additional filters are applied to select coins with a positive price change percentage and a trading volume that surpasses a predefined threshold. The selection is further refined to include coins whose last price falls within a specific range.

3. **Sorting and Trimming the List**: Following the initial filtering, the data is sorted based on quote volume. The top 30 entries are then selected for further consideration. Any coins with 'USD' in their names or those included in a predetermined ignore list are excluded at this stage.

4. **Comparison with Previously Traded Coins**: The selected coins are compared against the unique coin list derived from the `binance_ticker_top_30` table. Coins that are already on this list are removed from consideration.

5. **Enhancement with Market Cap Data**: Each coin on the list is then enriched with additional data such as market cap, fully diluted market cap, and a specific ratio. This data is sourced from another function. Coins for which this additional information is not available are omitted.

6. **Final Selection Based on Market Cap**: A final filter is applied to retain only those coins with a market cap between 100 million and 10 billion USD.

7. **Database Update and Retrieval**: The refined list of coins is used to update the `binance_ticker_top_30` table with an incremented `update_id`. The list is then retrieved back from the table, now updated with the latest data.

8. **Output Presentation**: The culmination of this process is the generation of a list termed 'today's hot coins', which is presented in a formatted string.
'''

def binance_today_hot_coin(trading_volume_limit = TRADING_VOLUME_LIMIT):
    
    # Read out the unique coin list from 'binance_ticker_top_30' table, make a empty list if binance_ticker_top_30 table is not exist or empty
    try:
        query = "SELECT DISTINCT coin FROM binance_ticker_top_30 WHERE openTime > :openTime"
        params = {'openTime': int(time.time() * 1000) - 30 * 24 * 60 * 60 * 1000}
        result = engine.connect().execute(text(query), params)
        df_30_days = pd.DataFrame(result.fetchall(), columns=result.keys())
        unique_coin_list = df_30_days['coin'].values.tolist()
    except: unique_coin_list = []

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

    # Keep the top 30 coins
    df_ticker = df_ticker.head(30)

    # Ignore the coins in unique_coin_list
    df_ticker = df_ticker[~df_ticker['coin'].isin(unique_coin_list)]
    if df_ticker.empty: return []

    # Update ticker with market cap and fully diluted market cap
    df_ticker['market_cap'] = 0
    df_ticker['fully_diluted_market_cap'] = 0
    df_ticker['ratio'] = 0.01
    for index, row in df_ticker.iterrows():
        coin = row['coin']
        token_info = get_token_market_cap_and_ratio(coin)
        if token_info:
            '''token_info = {'market_cap': 154794584.58836213, 'fully_diluted_market_cap': 305918151.36, 'ratio': 0.5060000000006607}'''
            df_ticker.loc[index, 'market_cap'] = int(token_info['market_cap'])
            df_ticker.loc[index, 'fully_diluted_market_cap'] = int(token_info['fully_diluted_market_cap'])
            df_ticker.loc[index, 'ratio'] = float(token_info['ratio'])
        else: df_ticker.drop(index, inplace=True)

    # Filter out the coins with market_cap between 100M and 10B
    df_ticker = df_ticker[(df_ticker['market_cap'] > 100_000_000) & (df_ticker['market_cap'] < 10_000_000_000)]

    if df_ticker.empty: return []

    df_ticker = df_ticker.reset_index(drop=True)

    # Read out the latest update_id from 'binance_ticker_top_30' table
    try: 
        result = engine.connect().execute(text("SELECT MAX(update_id) FROM binance_ticker_top_30"))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        update_id = df['MAX(update_id)'].values[0]
    except: update_id = 0
    update_id = int(update_id)

    df_ticker['update_id'] = update_id + 1

    # Append df_ticker to the 'binance_ticker_top_30' table
    df_ticker.to_sql('binance_ticker_top_30', engine, if_exists='append', index=False)

    # Read out the latest update_id from 'binance_ticker_top_30' table
    df_ticker = pd.DataFrame(engine.connect().execute(text("SELECT * FROM binance_ticker_top_30 WHERE update_id=:update_id"), {'update_id': update_id + 1}).fetchall())

    # create today_hot_coin_list
    today_hot_coin_list = df_ticker['coin'].values.tolist()

    today_hot_coin_list_str = ', '.join(today_hot_coin_list)

    print(f"today_hot_coin_list: {today_hot_coin_list_str}")

    return today_hot_coin_list
''' df_ticker
       symbol  priceChangePercent  lastPrice  openPrice  highPrice  lowPrice   quoteVolume       openTime      closeTime   coin    market_cap  fully_diluted_market_cap     ratio
0    LINAUSDT             -12.865   0.016858   0.019347   0.019950  0.016758  8.166821e+07  1685756785971  1685843185971   LINA  9.362306e+07              1.690495e+08  0.553820
1    PEPEUSDT               0.000   0.000001   0.000001   0.000001  0.000001  2.805064e+07  1685756783945  1685843183945   PEPE  4.987895e+08              5.355822e+08  0.931303
2    ARPAUSDT              -7.641   0.059110   0.064000   0.069590  0.057500  2.727382e+07  1685756784579  1685843184579   ARPA  7.361351e+07              1.184555e+08  0.621444
3   COMBOUSDT             -15.364   1.548000   1.829000   1.834000  1.475000  2.414374e+07  1685756779956  1685843179956  COMBO  1.137270e+08              1.600623e+08  0.710517
4     SXPUSDT               6.367   0.456100   0.428800   0.482900  0.428700  2.303637e+07  1685756786200  1685843186200    SXP  2.579746e+08              2.546665e+08  1.012990
5     CFXUSDT              -4.640   0.269200   0.282300   0.284400  0.265400  2.010361e+07  1685756786075  1685843186075    CFX  7.774646e+08              1.422788e+09  0.546437
6     EPXUSDT              21.801   0.000283   0.000232   0.000324  0.000231  1.886641e+07  1685756786279  1685843186279    EPX  1.903993e+07              3.780582e+07  0.503624
7    RNDRUSDT               2.284   2.597000   2.539000   2.638000  2.534000  1.811841e+07  1685756783529  1685843183529   RNDR  9.506594e+08              1.393014e+09  0.682448
8    SANDUSDT               0.053   0.567500   0.567200   0.582700  0.561600  1.635574e+07  1685756786288  1685843186288   SAND  1.053590e+09              1.705223e+09  0.617861
9     INJUSDT               0.744   7.854000   7.796000   8.172000  7.770000  1.550012e+07  1685756785581  1685843185581    INJ  6.309396e+08              7.886198e+08  0.800056
10    KEYUSDT              -7.082   0.007859   0.008458   0.008700  0.007800  1.543823e+07  1685756785128  1685843185128    KEY  4.179587e+07              4.727175e+07  0.884162
11    MTLUSDT               9.604   1.107000   1.010000   1.130000  1.009000  1.267358e+07  1685756785918  1685843185918    MTL  7.366251e+07              7.366251e+07  1.000000
12   MASKUSDT              -0.775   4.483000   4.518000   4.553000  4.407000  1.267285e+07  1685756780484  1685843180484   MASK  3.679589e+08              4.481156e+08  0.821125
13    FTMUSDT              -0.219   0.319200   0.319900   0.327000  0.317200  1.265156e+07  1685756783652  1685843183652    FTM  8.921519e+08              1.014947e+09  0.879014
14  MAGICUSDT              -2.043   1.006700   1.027700   1.059100  0.991300  1.207562e+07  1685756782567  1685843182567  MAGIC  2.177512e+08              3.501676e+08  0.621848
'''


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
        send_msg(f"{user_nick_name}, Your current positions are {df_balance.shape[0]} our of {POSITIONS_LIMIT}, but there is no hot coin today, please wait with patience 😘", chat_id)
        return

    # query_list  = []
    for coin in today_hot_coin_list:

        # Check if coin in df_balance['coin'].values, if yes, ignore this coin
        if coin in coin_in_positions: continue

        # Check coin information from coinmarketcap, if no information, ignore this coin
        if not get_token_price_from_coinmarketcap_and_send_msg(coin, chat_id): continue

        send_msg(do_market_buy(coin, check_size), chat_id)

    return


if __name__ == '__main__':
    print('Start running Trading_bot.py ...')
    # today_hot_coin_list = binance_today_hot_coin(trading_volume_limit = TRADING_VOLUME_LIMIT)
    # print(today_hot_coin_list)
    binance_today_hot_coins_check(chat_id=TG_BOT_OWNER_ID, user_nick_name='Dear', crontab=False, trading_volume_limit = TRADING_VOLUME_LIMIT, check_size = CHECK_SIZE)