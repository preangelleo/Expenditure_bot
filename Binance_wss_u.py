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

        print(json.dumps(data, indent=2, sort_keys=True))

        if data['o']['S'] == 'SELL' and data['o']['ps'] == 'SHORT':
            try: 
                send_msg(f"UMFUTURE {data['o']['ps']} SHORT at {data['o']['ap']}", TG_BOT_OWNER_ID)
                # 将新订单json转换成 dataframe 并写入table 'umfuture_short_orders', append
                df = pd.DataFrame(data['o'], index=[0])
                df.to_sql('umfuture_short_orders', engine, if_exists='append', index=False)
            except Exception as e: print(f"UMFUTURE Send Message Error: \n\n{e}\n\n")

        if data['o']['S'] == 'BUY' and data['o']['ps'] == 'SHORT':
            try:
                df = pd.DataFrame(engine.connect().execute(text('SELECT * FROM umfuture_short_orders WHERE s = :s AND S = :S ORDER BY T DESC LIMIT 1'), {'s': data['o']['s'], 'S': 'SELL'}).fetchall())
                if not df.empty:
                    coin = data['o']['s'][:-4]
                    price_change = float(df['ap']) - float(data['o']['ap'])
                    profit = price_change * float(df['q']) * 10000
                    profit = format_number(profit)
                    send_msg(f"UMFUTURE {coin} SHORT closed >> {profit} usdt", TG_BOT_OWNER_ID)
            except: pass

        if data['o']['S'] == 'BUY' and data['o']['ps'] == 'LONG':
            try: 
                send_msg(f"UMFUTURE {data['o']['ps']} LONG at {data['o']['ap']}", TG_BOT_OWNER_ID)
                # 将新订单json转换成 dataframe 并写入table 'umfuture_long_orders', append
                df = pd.DataFrame(data['o'], index=[0])
                df.to_sql('umfuture_long_orders', engine, if_exists='append', index=False)
            except Exception as e: print(f"UMFUTURE Send Message Error: \n\n{e}\n\n")
        
        if data['o']['S'] == 'SELL' and data['o']['ps'] == 'LONG':
            try:
                df = pd.DataFrame(engine.connect().execute(text('SELECT * FROM umfuture_long_orders WHERE s = :s AND S = :S ORDER BY T DESC LIMIT 1'), {'s': data['o']['s'], 'S': 'BUY'}).fetchall())
                if not df.empty:
                    coin = data['o']['s'][:-4]
                    price_change = float(data['o']['ap']) - float(df['ap'])
                    profit = price_change * float(df['q']) * 10000
                    profit = format_number(profit)
                    send_msg(f"UMFUTURE {coin} LONG closed >> {profit} usdt", TG_BOT_OWNER_ID)
            except: pass


''' {
    "E": 1703309262526,
    "T": 1703309262515,
    "e": "ORDER_TRADE_UPDATE",
    "o": {
        "L": "0.11690",
        "N": "USDT",
        "R": true,
        "S": "BUY",
        "T": 1703309262515,
        "V": "NONE",
        "X": "FILLED",
        "a": "0",
        "ap": "0.11685",
        "b": "0",
        "c": "web_NNeR7Cr9DzP26sOr5jCr",
        "cp": false,
        "f": "GTC",
        "gtd": 0,
        "i": 3550168631,
        "l": "307",
        "m": false,
        "n": "0.01794415",
        "o": "MARKET",
        "ot": "MARKET",
        "p": "0",
        "pP": false,
        "pm": "NONE",
        "ps": "SHORT",
        "q": "86311",
        "rp": "-0.33710002",
        "s": "ROSEUSDT",
        "si": 0,
        "sp": "0",
        "ss": 0,
        "t": 149011642,
        "wt": "CONTRACT_PRICE",
        "x": "TRADE",
        "z": "86311"
    }}'''

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
