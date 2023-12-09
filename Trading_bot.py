from Binance_api import *


TRADING_VOLUME_LIMIT = int(os.getenv('TRADING_VOLUME_LIMIT', 50_000_000))


# 通过 df_ticker = pd.read_json(BINANCE_TICKER_URL) 获得最新的 ticker 信息
def binance_today_hot_coin(trading_volume_limit = TRADING_VOLUME_LIMIT):
    
    # 读出 binance_ticker_top_30 中 的 openTime 在最近 30 天内的所有行 unique coin, 转换为 pandas df 并生成一个 unique_coin_list
    try:
        query = "SELECT DISTINCT coin FROM binance_ticker_top_30 WHERE openTime > :openTime"
        params = {'openTime': int(time.time() * 1000) - 30 * 24 * 60 * 60 * 1000}
        result = engine.connect().execute(text(query), params)
        df_30_days = pd.DataFrame(result.fetchall(), columns=result.keys())
        unique_coin_list = df_30_days['coin'].values.tolist()
    except: unique_coin_list = []

    df_ticker = pd.read_json(BINANCE_TICKER_URL)

    # 保留 symbol, priceChangePercent, lastPrice, openPrice, highPrice, lowPrice, volume, quoteVolume, openTime, closeTime
    df_ticker = df_ticker.loc[:, ['symbol', 'priceChangePercent', 'lastPrice', 'openPrice', 'highPrice', 'lowPrice', 'quoteVolume', 'openTime', 'closeTime']]

    # pick up the symbol endswith 'USDT'
    df_ticker = df_ticker[df_ticker['symbol'].str.endswith('USDT')]

    # Filter out the coins with priceChangePercent > 0 and quoteVolume > trading_volume_limit
    df_ticker = df_ticker[(df_ticker['priceChangePercent'] > 0) & (df_ticker['quoteVolume'] > trading_volume_limit)]

    # Filter out the coins with lastPrice between 0.0001 and 1000
    df_ticker = df_ticker[(df_ticker['lastPrice'] > 0.0001) & (df_ticker['lastPrice'] < 1000)]

    df_ticker = df_ticker.sort_values(by='quoteVolume', ascending=False)
    df_ticker['coin'] = df_ticker['symbol'].str[:-4]

    # 剔除 coin 包含 USD 的币
    df_ticker = df_ticker[~df_ticker['coin'].str.contains('USD')]

    # 剔除掉 IGNORE_LIST 中的币
    # IGNORE_LIST = get_all_token_symbol_from_ignore_coin_list_table()
    # df_ticker = df_ticker[~df_ticker['coin'].isin(IGNORE_LIST)]

    df_ticker = df_ticker.head(30)

    # 剔除掉 unique_coin_list 中的币
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
        else:
            df_ticker.drop(index, inplace=True)

    # Filter out the coins with market_cap between 100M and 10B
    df_ticker = df_ticker[(df_ticker['market_cap'] > 100_000_000) & (df_ticker['market_cap'] < 10_000_000_000)]

    if df_ticker.empty: return []

    df_ticker = df_ticker.reset_index(drop=True)

    # 读出 binance_ticker_top_30 中的 update_id 的最大值, 赋值给 update_id
    try: 
        result = engine.connect().execute(text("SELECT MAX(update_id) FROM binance_ticker_top_30"))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        update_id = df['MAX(update_id)'].values[0]
    except: update_id = 0
    update_id = int(update_id)

    # conn = get_db_connection()
    # cursor = conn.cursor()
    # cursor.execute("SHOW TABLES LIKE 'binance_ticker_top_30'")
    # if cursor.fetchone() is None: update_id = 0
    # else:
    #     cursor.execute("SELECT MAX(update_id) FROM binance_ticker_top_30")
    #     result = cursor.fetchone()
    #     update_id = result[0] if result else 0
    # cursor.close()
    # conn.close()

    df_ticker['update_id'] = update_id + 1

    # Append df_ticker to the 'binance_ticker_top_30' table
    df_ticker.to_sql('binance_ticker_top_30', engine, if_exists='append', index=False)

    # 读出 binance_ticker_top_30 中的 update_id = update_id + 1 的所有行, 赋值给 df_ticker
    df_ticker = pd.DataFrame(engine.connect().execute(text("SELECT * FROM binance_ticker_top_30 WHERE update_id=:update_id"), {'update_id': update_id + 1}).fetchall())

    # create today_hot_coin_list
    today_hot_coin_list = df_ticker['coin'].values.tolist()

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
'''我跑了一个月的程序化交易策略逻辑和效果：
每个小时轮训一次，读取出今日币安涨幅排行榜中交易量大于 5000w USDT 的所有币， 剔除 ignore list 中的币以及一个月内已经上过榜的币，然后再剔除掉市值信息获取失败的币（从 coinmarketcap 读取失败），最后返回所有币的 List。调用 Market Buy 按照市场价买入清单中所有的币（跳过目前还持有仓位的币），每三分钟轮训一次价格查询，如果涨幅超过 7% 则调用 Market Sell 以市场价清仓卖出，自动止盈。
六月份开始跑这个策略，到目前一个月，总收益 13%，剔除掉现有仓位的浮亏，净收益 6%。
'''



def binance_today_hot_coins_check(chat_id=BOTOWNER_CHAT_ID, user_nick_name='亲爱的', crontab=False, trading_volume_limit = 50_000_000, check_size = 1000):
    today_hot_coin_list = binance_today_hot_coin(trading_volume_limit)
    if not today_hot_coin_list: 
        if not crontab: send_msg(f"{user_nick_name}, 今天币安没有热门币种, 你可以明天再来看看哦 😘", chat_id)
        return 

    # query_list  = []
    for coin in today_hot_coin_list:
        
        token_info = get_token_info_from_coinmarketcap(coin)
        if not token_info: continue

        output_dict = {
            '名称': token_info['name'],
            '排名': token_info['cmc_rank'],
            '现价': f"{format_number(token_info['quote']['USD']['price'])} usd/{coin.lower()}",
            '交易量': f"{format_number(token_info['quote']['USD']['volume_24h'])} usd",
            '流通市值': f"{format_number(token_info['quote']['USD']['market_cap'])} usd | {token_info['circulating_supply'] / token_info['total_supply'] * 100:.1f}%",
            '24小时波动': f"{token_info['quote']['USD']['percent_change_24h']:.2f}%",
            '全流通市值': f"{format_number(token_info['quote']['USD']['fully_diluted_market_cap'])} usd",
            '代币总发行': f"{format_number(token_info['total_supply'])} {coin.lower()}",
            '本次更新时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        # 用 '\n' join k: v
        output_dict_str = '\n'.join([f"{k}: {v}" for k, v in output_dict.items()])
        send_msg(output_dict_str, chat_id)

        # 检查 binance_position_buy table 中 is_closed = 0 的 row 是否超过 10 个，如果没有超过 10 个则调用 binance_market_buy() 买入 1000 usdt
        df_balance = pd.DataFrame(engine.connect().execute(text('SELECT * FROM binance_position_buy WHERE is_closed = 0')).fetchall())
        if df_balance.shape[0] < 10: 
            # 检查 coin 是否在 binance_position_buy table 中，如果不在则调用 binance_market_buy() 买入 1000 usdt
            if coin not in df_balance['coin'].values: send_msg(do_market_buy(coin, check_size), chat_id)
        
        # query_list.append(f"Latest news about crypto project: {token_info['name']} {coin}")

    # for query in query_list:
    #     try: create_crypto_news_from_bing_search(query, chat_id)
    #     except: pass


    return

if __name__ == '__main__':
    print('Start running Trading_bot.py ...')
    today_hot_coin_list = binance_today_hot_coin(trading_volume_limit = TRADING_VOLUME_LIMIT)
    print(today_hot_coin_list)