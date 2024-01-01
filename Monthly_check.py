from Binance_api import *
from BTC_weekly import *

'''
30 stands for the 30th minute of the hour.
6 is the hour in 24-hour format, which is 6 AM.
* in the day_of_month field means every day of the month.
* in the month field means every month.
1 in the day_of_week field represents Monday (where 0 or 7 is Sunday, 1 is Monday, and so on).
'''

if __name__ == '__main__':
    # Crontab job, run once a day at 00:00
    '''13 8 1 * * cd /home/preangel/Expenditure_bot && /home/preangel/anaconda3/envs/expenditure_ai/bin/python3 /home/preangel/Expenditure_bot/Monthly_check.py >> /home/preangel/Expenditure_bot/cron.log 2>&1'''

    # print current time string format and the function is running
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} Weekly_check.py is running ...')

    try: get_btc_data_with_rsi(timeframe='1M', from_id=TG_BOT_OWNER_ID)
    except: pass

    try: montly_summary()
    except: pass
