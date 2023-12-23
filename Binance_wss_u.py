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
    # print(json.dumps(data, indent=2, sort_keys=True))

    # 账户变动
    if data['e'] == 'ACCOUNT_UPDATE':
        print(f"UMFUTURE: ACCOUNT_UPDATE")
        '''{
            "E": 1703307809090,
            "T": 1703307809083,
            "a": {
                "B": [
                {
                    "a": "USDT",
                    "bc": "0",
                    "cw": "100767.06273249",
                    "wb": "100767.06273249"
                }
                ],
                "P": [
                {
                    "bep": "0",
                    "cr": "-42.58360980",
                    "ep": "0",
                    "iw": "0",
                    "ma": "USDT",
                    "mt": "cross",
                    "pa": "0",
                    "ps": "SHORT",
                    "s": "RNDRUSDT",
                    "up": "0"
                }
                ],
                "m": "ORDER"
            },
            "e": "ACCOUNT_UPDATE"
            }
        '''
        # try:
        #     for i in data['a']['P']:
        #         profit = float(i['cr'])
        #         direction = i['ps']
        #         symbol = i['s']
        #         coin = symbol[:-4]
        #         send_msg(f"UMFUTURE: {coin} {direction.lower()} closed >> {format_number(profit)} usdt", TG_BOT_OWNER_ID)
        # except Exception as e: print(f"UMFUTURE Send Message Error: \n\n{e}\n\n")

    # 如果订单状态是 FILLED，发送 send_msg 给 telegram
    if data['e'] == 'ORDER_TRADE_UPDATE' and data['o']['X'] == 'FILLED':
        try: send_msg(f"UMFUTURE {data['o']['ps']} {data['o']['s'][:-4]} Order Filled at {format_number(data['o']['ap'])}", TG_BOT_OWNER_ID)
        except Exception as e: print(f"UMFUTURE Send Message Error: \n\n{e}\n\n")

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
