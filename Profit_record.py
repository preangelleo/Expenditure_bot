from BTC_weekly import *
from Trading_bot import *
from Gmail_api import *

if __name__ == '__main__':
    # Crontab job, run once a day at 00:00
    '''17 5 * * * cd /home/preangel/Expenditure_bot && /home/preangel/anaconda3/envs/expenditure_ai/bin/python3 /home/preangel/Expenditure_bot/Profit_record.py >> /home/preangel/Expenditure_bot/cron.log 2>&1'''

    # print current time string format and the function is running
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} Profit_record.py is running ...')

    current_bot_status = False

    try: current_bot_status = trading_bot_switch_status()
    except: pass

    try: binance_auto_position_check(None, None, True, table_name='binance_position_buy')
    except Exception as e: print(f'binance_auto_position_check() error:\n\n{e}\n\n')

    try: get_btc_data_with_rsi(timeframe='1d', from_id=TG_BOT_OWNER_ID)
    except Exception as e: print(f'get_btc_data_with_rsi() error:\n\n{e}\n\n')

    try: calculate_hot_coin_price_change()
    except Exception as e: print(f'calculate_hot_coin_price_change() error:\n\n{e}\n\n')

    try: binance_today_hot_coin(trading_volume_limit = TRADING_VOLUME_LIMIT, tradingbot_status = current_bot_status, coin_in_positions=[])
    except Exception as e: print(f'binance_today_hot_coin() error:\n\n{e}\n\n')

    try: binance_adjust_profit(from_id = None)
    except Exception as e: print(f'binance_adjust_profit() error:\n\n{e}\n\n')

    try: send_file(TG_BOT_OWNER_ID, 'cron.log', 'Operation log of crontab job')
    except Exception as e: print(f'send_file() error:\n\n{e}\n\n')
