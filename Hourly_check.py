from Binance_api import *

if __name__ == '__main__':
    # Crontab job, run once a hour
    '''3 * * * * cd /home/preangel/Expenditure_bot && /home/preangel/anaconda3/envs/expenditure_ai/bin/python3 /home/preangel/Expenditure_bot/Hourly_check.py >> /home/preangel/Expenditure_bot/cron.log 2>&1'''

    # print current time string format and the function is running
    print(f'\n{datetime.now().strftime("%Y-%m-%d %H:%M")} Hourly_check.py is running ...')

    try: daily_profit_take(daily_profit_target=1000, table_name = 'binance_position_buy', chat_id=TG_BOT_OWNER_ID)
    except Exception as e: print(f'daily_profit_take() error:\n\n{e}\n\n')

    # Check if it's UTC 11pm, if yes run daily_profit_take_last_check()
    if datetime.now().strftime("%H") == '23':
        try: daily_profit_take_last_check()
        except Exception as e: print(f'daily_profit_take_last_check() error:\n\n{e}\n\n')