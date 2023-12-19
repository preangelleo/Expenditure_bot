from Trading_bot import *
from binance import ThreadedWebsocketManager


def main():

    symbol = 'WLDUSDT'

    twm = ThreadedWebsocketManager(api_key=BINANCE_API, api_secret=BINANCE_SECRET)
    # start is required to initialise its internal loop
    twm.start()

    def handle_socket_message(msg):
        print(f"message type: {msg['e']}")
        print(msg)

    twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)

    # multiple sockets can be started
    # twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)

    # or a multiplex socket can be started like this
    # see Binance docs for stream names
    # streams = [f'{symbol}@miniTicker', f'{symbol}@bookTicker']
    # twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)

    '''message type: kline
    {'e': 'kline', 'E': 1703007176955, 's': 'WLDUSDT', 'k': {'t': 1703007120000, 'T': 1703007179999, 's': 'WLDUSDT', 'i': '1m', 'f': 19390238, 'L': 19390795, 'o': '3.79600000', 'c': '3.76900000', 'h': '3.80300000', 'l': '3.76300000', 'v': '28197.50000000', 'n': 558, 'x': False, 'q': '106502.66510000', 'V': '8444.30000000', 'Q': '31911.54130000', 'B': '0'}}
    message type: depthUpdate
    {'e': 'depthUpdate', 'E': 1703007177421, 's': 'WLDUSDT', 'U': 522904682, 'u': 522904762, 'b': [['3.76900000', '275.00000000'], ['3.76800000', '83.80000000'], ['3.76700000', '157.70000000'], ['3.76600000', '686.00000000'], ['3.76400000', '770.80000000'], ['3.76300000', '1753.70000000'], ['3.76200000', '3615.80000000'], ['3.76100000', '5123.30000000'], ['3.76000000', '22855.90000000'], ['3.75900000', '396.40000000'], ['3.75800000', '2644.50000000'], ['3.75500000', '1213.50000000'], ['3.75400000', '596.50000000'], ['3.74400000', '1180.10000000'], ['3.74300000', '74.90000000'], ['3.74000000', '2864.40000000'], ['3.72900000', '616.80000000'], ['3.72100000', '560.00000000'], ['3.66400000', '2.30000000'], ['3.47900000', '44.40000000']], 'a': [['3.76900000', '0.00000000'], ['3.77000000', '299.80000000'], ['3.77100000', '154.50000000'], ['3.77200000', '558.40000000'], ['3.77300000', '626.00000000'], ['3.77400000', '1743.80000000'], ['3.77500000', '2541.00000000'], ['3.77600000', '2123.60000000'], ['3.77700000', '947.90000000'], ['3.77900000', '448.00000000'], ['3.78200000', '375.20000000'], ['3.78400000', '611.50000000'], ['3.78600000', '1070.70000000'], ['3.79200000', '1719.20000000'], ['3.79300000', '107.10000000'], ['3.81100000', '9949.80000000'], ['3.81200000', '277.50000000'], ['3.83600000', '1380.30000000'], ['3.85100000', '1.40000000']]}
    '''
    twm.join()


if __name__ == "__main__":
   print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} Binance_wss.py is running ...')
   main()