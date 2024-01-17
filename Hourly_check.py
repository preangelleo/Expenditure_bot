from datetime import datetime

if __name__ == '__main__':
    # Crontab job, run once a hour
    '''3 * * * * cd /home/preangel/Expenditure_bot && /home/preangel/anaconda3/envs/expenditure_ai/bin/python3 /home/preangel/Expenditure_bot/Hourly_check.py >> /home/preangel/Expenditure_bot/cron.log 2>&1'''

    # print current time string format and the function is running
    print(f'\n{datetime.now().strftime("%Y-%m-%d %H:%M")} Hourly_check.py is running ...')

    # try: daily_profit_take()
    # except Exception as e: print(f'daily_profit_take() error:\n\n{e}\n\n')
