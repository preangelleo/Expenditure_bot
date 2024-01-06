from Trading_bot import *
from binance import ThreadedWebsocketManager

from_id = TG_BOT_OWNER_ID

def handle_socket_message(msg):
    if msg['e'] == 'outboundAccountPosition':
        # Handle account position update
        print('Account position update:')
        print(msg)
        '''outboundAccountPosition
        {
        "e": "outboundAccountPosition", // 事件类型
        "E": 1564034571105,             // 事件时间
        "u": 1564034571073,             // 账户末次更新时间戳
        "B": [                          // 余额
            {
            "a": "ETH",                 // 资产名称
            "f": "10000.000000",        // 可用余额
            "l": "0.000000"             // 冻结余额
            }
        ]
        }'''
        # Make a dataframe from the 'B' value in the message, save to sql and append the old one if exists
        df = pd.DataFrame(msg['B'])
        df['timestamp'] = msg['E']
        df['update_time'] = msg['u']
        df['asset'] = df['a']
        df['free'] = df['f'].astype(float)
        df['locked'] = df['l'].astype(float)
        df = df[['asset', 'free', 'locked', 'timestamp', 'update_time']]
        with engine.connect() as connection: df.to_sql('binance_balance_history', connection, if_exists='append', index=False)
        try:
            bnb_df = df[df['asset'] == 'BNB']
            if not bnb_df.empty:
                if bnb_df['free'].values[0] < 2: check_and_buy_bnb(coin = 'BNB', check_limit = 1, chat_id=TG_BOT_OWNER_ID)
        except Exception as e: print(f'check_and_buy_bnb() error:\n\n{e}\n\n')


    elif msg['e'] == 'balanceUpdate':
        # Handle balance update
        print('Balance update:')
        '''balanceUpdate
        {
        "e": "balanceUpdate",         //Event Type
        "E": 1573200697110,           //Event Time
        "a": "ABC",                   //Asset
        "d": "100.00000000",          //Balance Delta
        "T": 1573200697068            //Clear Time
        }'''
        # Make a string from the message and send to the telegram from_id
        coin = msg['a']
        delta = msg['d']
        add_or_subtract = 'added' if float(delta) > 0 else 'subtracted'
        time_of_update = datetime.fromtimestamp(msg['E']/1000).strftime("%Y-%m-%d %H:%M")
        alert_msg = f"Binance Balance Update:\n\n{coin} {add_or_subtract} {format_number(delta)}\n\n{time_of_update}"
        send_msg(alert_msg, from_id)

    elif msg['e'] == 'executionReport':
        # Handle execution report
        print('Execution report:')
        print(json.dumps(msg, indent=2, sort_keys=True))

        '''Payload: 订单更新
        订单通过executionReport事件进行更新。

        执行类型:

        NEW - 新订单已被引擎接受。
        CANCELED - 订单被用户取消。
        REPLACED - (保留字段，当前未使用)
        REJECTED - 新订单被拒绝 （这信息只会在撤消挂单再下单中发生，下新订单被拒绝但撤消挂单请求成功）。
        TRADE - 订单有新成交。
        EXPIRED - 订单已根据 Time In Force 参数的规则取消（e.g. 没有成交的 LIMIT FOK 订单或部分成交的 LIMIT IOC 订单）或者被交易所取消（e.g. 强平或维护期间取消的订单）。
        TRADE_PREVENTION - 订单因 STP 触发而过期。
        请查阅公开API参数文档获取更多枚举定义。

        备注: 通过将Z除以z可以找到平均价格。

        如果订单是OCO，则除了显示executionReport事件外，还将显示一个名为ListStatus的事件。

        executionReport 中的仅在满足特定条件时才会出现的字段：
        字段  名称  描述  示例
        d   Trailing Delta  出现在追踪止损订单中。 "d": 4
        D   Trailing Time   "D": 1668680518494
        j   Strategy Id 如果在请求中添加了strategyId参数，则会出现。 "j": 1
        J   Strategy Type   如果在请求中添加了strategyType参数，则会出现。   "J": 1000000
        v   Prevented Match Id  只有在因为 STP 导致订单失效时可见。    "v": 3
        A   Prevented Quantity  "A":"3.000000"
        B   Last Prevented Quantity "B":"3.000000"
        u   Trade Group Id  "u":1
        U   Counter Order Id    "U":37
        Cs  Counter Symbol  "Cs": "BTCUSDT"
        pl  Prevented Execution Quantity    "pl":"2.123456"
        pL  Prevented Execution Price   "pL":"0.10000001"
        pY  Prevented Execution Quote Qty   "pY":"0.21234562"
        W   Working Time    只有在订单在订单簿上时可见   "W": 1668683798379
        b   Match Type  只有在订单有分配时可见 "b":"ONE_PARTY_TRADE_REPORT"
        a   Allocation ID   "a":1234
        k   Working Floor   只有在订单可能有分配时可见   "k":"SOR"
        uS  UsedSor 只有在订单使用 SOR 时可见 "uS":true'''
        '''executionReport            
        {
        "e": "executionReport",        // 事件类型
        "E": 1499405658658,            // 事件时间
        "s": "ETHBTC",                 // 交易对
        "c": "mUvoqJxFIILMdfAW5iGSOW", // clientOrderId
        "S": "BUY",                    // 订单方向
        "o": "LIMIT",                  // 订单类型
        "f": "GTC",                    // 有效方式
        "q": "1.00000000",             // 订单原始数量
        "p": "0.10264410",             // 订单原始价格
        "P": "0.00000000",             // 止盈止损单触发价格
        "F": "0.00000000",             // 冰山订单数量
        "g": -1,                       // OCO订单 OrderListId
        "C": "",                       // 原始订单自定义ID(原始订单，指撤单操作的对象。撤单本身被视为另一个订单)
        "x": "NEW",                    // 本次事件的具体执行类型
        "X": "NEW",                    // 订单的当前状态
        "r": "NONE",                   // 订单被拒绝的原因
        "i": 4293153,                  // orderId
        "l": "0.00000000",             // 订单末次成交量
        "z": "0.00000000",             // 订单累计已成交量
        "L": "0.00000000",             // 订单末次成交价格
        "n": "0",                      // 手续费数量
        "N": null,                     // 手续费资产类别
        "T": 1499405658657,            // 成交时间
        "t": -1,                       // 成交ID
        "v": 3,                        // 被阻止撮合交易的ID; 这仅在订单因 STP 触发而过期时可见
        "I": 8641984,                  // 请忽略
        "w": true,                     // 订单是否在订单簿上？
        "m": false,                    // 该成交是作为挂单成交吗？
        "M": false,                    // 请忽略
        "O": 1499405658657,            // 订单创建时间
        "Z": "0.00000000",             // 订单累计已成交金额
        "Y": "0.00000000",             // 订单末次成交金额
        "Q": "0.00000000",             // Quote Order Quantity
        "W": 1499405658657,            // Working Time; 订单被添加到 order book 的时间
        "V": "NONE"                    // SelfTradePreventionMode
        }'''
        # Handle execution report
        
        symbol = msg['s']
        coin = symbol.replace('USDT', '')
        clientOrderId = msg['C'] if msg['C'] else msg['c']
        orderId = msg['i']
        table_name = 'binance_limit_buy_order' if msg['S'] == 'BUY' else 'binance_limit_sell_order'
        
        if msg['X'] in ['CANCELED', 'CANCELLED']:
            ''' {'e': 'executionReport', 'E': 1703029327337, 's': 'RUNEUSDT', 'c': 'web_4ef308e8a5034b259fd36acf1b18fdd6', 'S': 'SELL', 'o': 'LIMIT', 'f': 'GTC', 'q': '1515.40000000', 'p': '6.66500000', 'P': '0.00000000', 'F': '0.00000000', 'g': -1, 'C': 'KkrTVdDuxAc5ggTIUErslC', 'x': 'CANCELED', 'X': 'CANCELED', 'r': 'NONE', 'i': 1269148511, 'l': '0.00000000', 'z': '0.00000000', 'L': '0.00000000', 'n': '0', 'N': None, 'T': 1703029327336, 't': -1, 'I': 2630955099, 'w': False, 'm': False, 'M': False, 'O': 1703019729294, 'Z': '0.00000000', 'Y': '0.00000000', 'Q': '0.00000000', 'W': 1703019729294, 'V': 'EXPIRE_MAKER'}'''
            if msg['c'].startswith('web_'): mark_limit_order_as_canceled_by_orderId(orderId, msg['X'], table_name)

        elif msg['X'] in ['EXPIRED']: mark_limit_order_as_canceled_by_orderId(orderId, msg['X'], table_name)

        elif msg['X'] == 'FILLED':
            # check direction is BUY or SELL
            if msg['S'] == 'SELL':
                '''{'e': 'executionReport', 'E': 1703032385551, 's': 'NEARUSDT', 'c': 'b1vSFIYMRLWZrz4ecPsPaZ', 'S': 'SELL', 'o': 'LIMIT', 'f': 'GTC', 'q': '3960.70000000', 'p': '2.55000000', 'P': '0.00000000', 'F': '0.00000000', 'g': -1, 'C': '', 'x': 'TRADE', 'X': 'FILLED', 'r': 'NONE', 'i': 2110473867, 'l': '3960.70000000', 'z': '3960.70000000', 'L': '2.55000000', 'n': '0.02982221', 'N': 'BNB', 'T': 1703032385543, 't': 138267320, 'I': 4348096316, 'w': False, 'm': True, 'M': True, 'O': 1703019732394, 'Z': '10099.78500000', 'Y': '10099.78500000', 'Q': '0.00000000', 'W': 1703019732394, 'V': 'EXPIRE_MAKER'}'''
                try: binance_limit_sell_order_status(symbol, orderId, table_name = 'binance_position_buy')
                except: pass
            elif msg['S'] == 'BUY':
                try: binance_limit_buy_order_status(symbol, orderId, table_name = 'binance_manually_buy')
                except: pass

        # if msg['X'] == 'NEW':
        #     if clientOrderId.startswith('web_'):
        #         binance_manually_buy_dict = {
        #             'symbol': symbol,
        #             'orderId': orderId,
        #             'orderListId': msg['g'],
        #             'clientOrderId': clientOrderId,
        #             'transactTime': msg['T'],
        #             'price': msg['p'],
        #             'origQty': msg['q'],
        #             'executedQty': msg['z'],
        #             'cummulativeQuoteQty': msg['Z'],
        #             'status': msg['X'],
        #             'timeInForce': msg['f'],
        #             'type': msg['o'],
        #             'side': msg['S'],
        #             'workingTime': msg['W'],
        #             'selfTradePreventionMode': msg['V'],
        #             'coin': coin,
        #             'buy_cost_bnb': 0,
        #             'buy_bnb_price': 0,
        #             'update_id': 0,
        #             'is_closed': 0
        #         }
        #         if data_to_table(binance_manually_buy_dict, 'binance_manually_buy'): binance_position_set_limit_sell(0.1, TG_BOT_OWNER_ID, coin, 'binance_manually_buy')

def main():
    twm = ThreadedWebsocketManager(api_key=BINANCE_API, api_secret=BINANCE_SECRET)
    twm.start()
    twm.start_user_socket(callback=handle_socket_message)
    twm.join()


if __name__ == "__main__":
   print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} Binance_wss.py is running ...')
   main()