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
    print("UMFUTURE Received Message:")
    print(json.dumps(data, indent=2, sort_keys=True))

    # 如果订单状态是 FILLED，发送 send_msg 给 telegram
    if data['e'] == 'ORDER_TRADE_UPDATE' and data['o']['X'] == 'FILLED':
        try: send_msg(f"UMFUTURE Order Filled: {data['o']['s']} {data['o']['q']} at {data['o']['L']}")
        except Exception as e: print(f"UMFUTURE Send Message Error: \n\n{e}\n\n")

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

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
