from Top_functions import *
import matplotlib.dates as mpl_dates


def get_btc_data_with_rsi(chat_id):
    print('Start running get_btc_data_with_rsi() ...')
    # Initialize Binance Client
    exchange = ccxt.binance()

    # Fetch historical data for BTC/USDT
    btc_data = exchange.fetch_ohlcv('BTC/USDT', timeframe='1w', limit=216)

    # Convert to DataFrame
    df = pd.DataFrame(btc_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Calculate RSI
    delta = df['close'].diff()
    gain = (delta > 0) * delta
    loss = (delta < 0) * -delta
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # Plotting
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Convert timestamp to a format suitable for matplotlib
    df['timestamp'] = df['timestamp'].map(mpl_dates.date2num)

    # Plot candlestick chart
    candlestick_ohlc(ax1, df[['timestamp', 'open', 'high', 'low', 'close']].values, width=0.6, colorup='green', colordown='red', alpha=0.8)
    ax1.xaxis_date()
    ax1.xaxis.set_major_formatter(mpl_dates.DateFormatter('%Y-%m-%d'))
    ax1.set_xlabel('Date')
    ax1.set_ylabel('BTC Price')
    ax1.set_title('BTC Weekly Chart with RSI')

    # Create a secondary y-axis for the RSI
    ax2 = ax1.twinx()
    ax2.plot(df['timestamp'], df['RSI'], color='blue', label='RSI')
    ax2.axhline(80, color='red', linestyle='--', linewidth=1)
    ax2.axhline(20, color='green', linestyle='--', linewidth=1)
    ax2.set_ylabel('RSI')
    ax2.legend(loc='upper left')

    # Improve layout
    fig.tight_layout()

    file_name = 'net_profit_daily_record/BTC_Weekly.png'
    # Save plot to file
    plt.savefig(file_name)
    plt.close(fig)

    if chat_id: send_img(chat_id, file_name)

    return file_name

if __name__ == '__main__':
    print('Start running Trading_bot.py ...')
    get_btc_data_with_rsi(TG_BOT_OWNER_ID)

    
