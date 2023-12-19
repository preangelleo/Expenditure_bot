from Trading_bot import *
from binance import ThreadedWebsocketManager


def handle_socket_message(msg):
    if msg['e'] == 'outboundAccountPosition':
        # Handle account position update
        print('Account position update:')
        print(msg)
    elif msg['e'] == 'balanceUpdate':
        # Handle balance update
        print('Balance update:')
        print(msg)
    elif msg['e'] == 'executionReport':
        # Handle execution report
        print('Execution report:')
        # Handle execution report
        if msg['X'] == 'CANCELED': print('Order was canceled:')
        elif msg['X'] == 'FILLED': print('Order was filled:')

        print(msg)


def main():
    twm = ThreadedWebsocketManager(api_key=BINANCE_API, api_secret=BINANCE_SECRET)
    twm.start()
    twm.start_user_socket(callback=handle_socket_message)
    twm.join()


if __name__ == "__main__":
   print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} Binance_wss.py is running ...')
   main()