from BTC_weekly import *
from Trading_bot import *
from Gmail_api import *

if __name__ == '__main__':
    # Crontab job, run once a day at 00:00
    '''17 5 * * * cd /home/preangel/Expenditure_bot && /home/preangel/anaconda3/envs/expenditure_ai/bin/python3 /home/preangel/Expenditure_bot/Profit_record.py >> /home/preangel/Expenditure_bot/cron.log 2>&1'''

    # print current time string format and the function is running
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} Profit_record.py is running ...')

    try: binance_spot_position_check(None, None, True)
    except Exception as e: print(f'binance_spot_position_check() error:\n\n{e}\n\n')

    try: binance_adjust_profit()
    except Exception as e: print(f'binance_adjust_profit() error:\n\n{e}\n\n')

    try: get_btc_data_with_rsi(timeframe = '1d', from_id = TG_BOT_OWNER_ID)
    except Exception as e: print(f'get_btc_data_with_rsi() error:\n\n{e}\n\n')

    # try: get_coin_list_from_trading_pairs()
    # except Exception as e: print(f'get_coin_list_from_trading_pairs() error:\n\n{e}\n\n')

    try: send_file(TG_BOT_OWNER_ID, 'cron.log', 'Operation log of crontab job')
    except Exception as e: print(f'send_file() error:\n\n{e}\n\n')
