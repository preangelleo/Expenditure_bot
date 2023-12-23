from Trading_bot import *
import websocket

api_key = BINANCE_API
api_secret = BINANCE_SECRET

# 获取listenKey
def get_listen_key():
    url = "https://fapi.binance.com/fapi/v1/listenKey"
    headers = {"X-MBX-APIKEY": api_key}
    response = requests.post(url, headers=headers)
    return response.json()['listenKey']

# WebSocket回调
def on_message(ws, message):
    data = json.loads(message)
    
    # 如果订单状态是 FILLED，发送 send_msg 给 telegram
    if data['e'] == 'ORDER_TRADE_UPDATE' and data['o']['X'] == 'FILLED':
        # print(json.dumps(data, indent=2, sort_keys=True))
        coin = data['o']['s'][:-4]

        if data['o']['S'] == 'SELL' and data['o']['ps'] == 'SHORT':
            try: 
                send_msg(f"UMFUTURE {coin} SHORT at {data['o']['ap']}", TG_BOT_OWNER_ID)
                # 将新订单json转换成 dataframe 并写入table 'umfuture_orders_short', append
                new_data = {
                    'coin': coin,
                    'symbol': data['o']['s'],
                    'price': data['o']['ap'],
                    'direction': 'SHORT',
                    'type': 'SELL',
                    'trade_time': data['o']['T'],
                    'trade_id': data['o']['c']
                }
                df = pd.DataFrame(new_data, index=[0])
                df.to_sql('umfuture_orders_short', engine, if_exists='append', index=False)
            except Exception as e: print(f"UMFUTURE Send Message Error: \n\n{e}\n\n")

        if data['o']['S'] == 'BUY' and data['o']['ps'] == 'SHORT':
            try:
                df = pd.DataFrame(engine.connect().execute(text('SELECT * FROM umfuture_orders_short WHERE coin = :coin AND type = :type ORDER BY trade_time DESC LIMIT 1'), {'coin': coin, 'type': 'SELL'}).fetchall())
                if not df.empty:
                    price_change = float(df['price'].iloc[0]) - float(data['o']['ap'])
                    profit = price_change / float(df['price'].iloc[0]) * 10000
                    profit = format_number(profit)
                    send_msg(f"UMFUTURE {coin} SHORT closed >> {profit} usdt", TG_BOT_OWNER_ID)

                    duration = data['o']['T'] - df['trade_time']
                    new_data = {
                        'coin': coin,
                        'symbol': data['o']['s'],
                        'price': data['o']['ap'],
                        'direction': 'SHORT',
                        'profit': profit,
                        'trade_time': data['o']['T'],
                        'trade_id': data['o']['c'],
                        'duration': duration
                    }
                    df = pd.DataFrame(new_data, index=[0])
                    df.to_sql('umfuture_orders_profit', engine, if_exists='append', index=False)
                    # df = pd.DataFrame(engine.connect().execute(text('SELECT * FROM umfuture_orders_profit WHERE coin = :coin'), {'coin': coin}).fetchall())
                    profit = get_umfuture_profit(TG_BOT_OWNER_ID, coin)
            except: pass

        if data['o']['S'] == 'BUY' and data['o']['ps'] == 'LONG':
            try: 
                send_msg(f"UMFUTURE {coin} LONG at {data['o']['ap']}", TG_BOT_OWNER_ID)
                # 将新订单json转换成 dataframe 并写入table 'umfuture_orders_long', append
                new_data = {
                    'coin': coin,
                    'symbol': data['o']['s'],
                    'price': data['o']['ap'],
                    'direction': 'LONG',
                    'type': 'BUY',
                    'trade_time': data['o']['T'],
                    'trade_id': data['o']['c']
                }
                df = pd.DataFrame(new_data, index=[0])
                df.to_sql('umfuture_orders_long', engine, if_exists='append', index=False)
            except Exception as e: print(f"UMFUTURE Send Message Error: \n\n{e}\n\n")
        
        if data['o']['S'] == 'SELL' and data['o']['ps'] == 'LONG':
            try:
                df = pd.DataFrame(engine.connect().execute(text('SELECT * FROM umfuture_orders_long WHERE coin = :coin AND type = :type ORDER BY trade_time DESC LIMIT 1'), {'coin': coin, 'type': 'BUY'}).fetchall())
                if not df.empty:
                    price_change = float(data['o']['ap']) - float(df['price'].iloc[0])
                    profit = price_change / float(df['price'].iloc[0]) * 10000
                    profit = format_number(profit)
                    send_msg(f"UMFUTURE {coin} LONG closed >> {profit} usdt", TG_BOT_OWNER_ID)
                    duration = data['o']['T'] - df['trade_time']
                    new_data = {
                        'coin': coin,
                        'symbol': data['o']['s'],
                        'price': data['o']['ap'],
                        'direction': 'LONG',
                        'profit': profit,
                        'trade_time': data['o']['T'],
                        'trade_id': data['o']['c'],
                        'duration': duration
                    }
                    df = pd.DataFrame(new_data, index=[0])
                    df.to_sql('umfuture_orders_profit', engine, if_exists='append', index=False)
                    # df = pd.DataFrame(engine.connect().execute(text('SELECT * FROM umfuture_orders_profit WHERE coin = :coin'), {'coin': coin}).fetchall())
                    profit = get_umfuture_profit(TG_BOT_OWNER_ID, coin)
            except: pass


def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")
    print(close_status_code, close_msg)

def on_open(ws):
    print("WebSocket Connected")

if __name__ == "__main__":
    listen_key = get_listen_key()
    ws = websocket.WebSocketApp(f"wss://fstream.binance.com/ws/{listen_key}",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
