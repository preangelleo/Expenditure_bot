from Top_functions import *

import ccxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates

def get_btc_data_with_rsi(chat_id=TG_BOT_OWNER_ID):
    # Initialize Binance Client
    exchange = ccxt.binance()

    # Fetch historical data for BTC/USDT
    btc_data = exchange.fetch_ohlcv('BTC/USDT', timeframe='1w', limit=52)

    # Convert to DataFrame
    df = pd.DataFrame(btc_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Calculate RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [2, 1]})

    # Convert timestamp to a format suitable for matplotlib
    df['timestamp'] = df['timestamp'].apply(mpl_dates.date2num)
    candlestick_ohlc(ax1, df[['timestamp', 'open', 'high', 'low', 'close']].values, width=0.6, colorup='green', colordown='red')

    ax1.set_xlabel('Date')
    ax1.set_ylabel('BTC Price')
    ax1.set_title('BTC Weekly Candlestick with RSI')

    # Plot RSI
    ax2.plot(df['timestamp'], df['RSI'], color='blue')
    ax2.axhline(70, color='red', linestyle='--')
    ax2.axhline(30, color='green', linestyle='--')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('RSI')

    file_name = 'net_profit_daily_record/BTC_Weekly.png'
    # Save plot
    plt.savefig(file_name)
    # plt.show()

    send_msg(file_name, chat_id)
    return file_name

# Call the function
file_path = get_btc_data_with_rsi()
file_path
