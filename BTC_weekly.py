from Top_functions import *
import matplotlib.dates as mpl_dates


def get_btc_data_with_rsi(chat_id):
    # Initialize Binance Client
    exchange = ccxt.binance()

    # Fetch historical data for BTC/USDT
    btc_data = exchange.fetch_ohlcv('BTC/USDT', timeframe='1w', limit=52)

    # Convert to DataFrame
    df = pd.DataFrame(btc_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Calculate RSI
    delta = df['close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [2, 1]})

    # Format the timestamp for matplotlib
    df['timestamp'] = df['timestamp'].apply(mpl_dates.date2num)

    # Plot candlestick chart
    candlestick_ohlc(ax1, df[['timestamp', 'open', 'high', 'low', 'close']].values, width=0.6, colorup='green', colordown='red')
    ax1.xaxis_date()
    ax1.xaxis.set_major_formatter(mpl_dates.DateFormatter('%Y-%m-%d'))
    ax1.set_xlabel('Date')
    ax1.set_ylabel('BTC Price')
    ax1.set_title('BTC Weekly Candlestick with RSI')

    # Plot RSI
    ax2.plot(df['timestamp'], df['RSI'], color='blue')
    ax2.axhline(70, color='red', linestyle='--', linewidth=1)
    ax2.axhline(30, color='green', linestyle='--', linewidth=1)
    ax2.xaxis_date()
    ax2.xaxis.set_major_formatter(mpl_dates.DateFormatter('%Y-%m-%d'))
    ax2.set_xlabel('Date')
    ax2.set_ylabel('RSI')

    # Improve layout
    plt.tight_layout()

    file_name = 'net_profit_daily_record/BTC_Weekly.png'
    # Save plot to file
    plt.savefig(file_name)
    plt.close(fig)

    if chat_id: send_img(chat_id, file_name)

    return file_name

# You need to define the send_msg function according to your chat bot's API and include the chat_id
# Example placeholder for the TG_BOT_OWNER_ID (you should replace this with the actual ID)

get_btc_data_with_rsi(TG_BOT_OWNER_ID)
