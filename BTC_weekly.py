from Top_functions import *
import matplotlib.dates as mpl_dates

def get_btc_data_with_rsi(timeframe='1w', chat_id=None):
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} get_btc_data_with_rsi() is running ...')

    exchange = ccxt.binance()

    # Validate and set the timeframe
    valid_timeframes = ['1d', '1w', '1M']
    if timeframe not in valid_timeframes: return send_msg(chat_id, f'Invalid timeframe: {timeframe}')
    
    chart_title = f'BTC Weekly Chart with RSI' if timeframe == '1w' else f'BTC Daily Chart with RSI' if timeframe == '1d' else f'BTC Monthly Chart with RSI'

    file_name = f'net_profit_daily_record/{datetime.now().strftime("%Y-%m-%d")} {chart_title}.png' if timeframe == '1d' else f'net_profit_daily_record/{datetime.now().strftime("%Y-%m-%d")} {chart_title}.png' if timeframe == '1w' else f'net_profit_daily_record/{datetime.now().strftime("%Y-%m-%d")} {chart_title}.png'

    # check if file exists, if yes, return send_img(chat_id, file_name, f'Current Price: {btc_price:.2f} usdt')
    if os.path.exists(file_name): 
        send_img(chat_id, file_name, f'Current Price: {btc_price:.2f} usdt')
        return file_name

    btc_data = exchange.fetch_ohlcv('BTC/USDT', timeframe=timeframe, limit=365)

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
    ax1.set_title(chart_title)

    # Create a secondary y-axis for the RSI
    ax2 = ax1.twinx()
    ax2.plot(df['timestamp'], df['RSI'], color='blue', label='RSI')
    ax2.axhline(80, color='red', linestyle='--', linewidth=1)
    ax2.axhline(20, color='green', linestyle='--', linewidth=1)
    ax2.set_ylabel('RSI')
    ax2.legend(loc='upper left')

    # Improve layout
    fig.tight_layout()

    
    # Save plot to file
    plt.savefig(file_name)
    plt.close(fig)

    # get the price of BTC
    btc_price = df['close'].iloc[-1]

    if chat_id: send_img(chat_id, file_name, f'Current Price: {btc_price:.2f} usdt')
    return file_name


if __name__ == '__main__':
    print('Start running Trading_bot.py ...')
    get_btc_data_with_rsi(timeframe='1d', chat_id=TG_BOT_OWNER_ID)
    get_btc_data_with_rsi(timeframe='1w', chat_id=TG_BOT_OWNER_ID)
    get_btc_data_with_rsi(timeframe='1M', chat_id=TG_BOT_OWNER_ID)

    
