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
    twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)

    # or a multiplex socket can be started like this
    # see Binance docs for stream names
    streams = [f'{symbol}@miniTicker', f'{symbol}@bookTicker']
    twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)

    twm.join()


if __name__ == "__main__":
   main()