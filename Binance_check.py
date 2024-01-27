from Trading_bot import *
from Gmail_api import *

if __name__ == '__main__':
    # Crontab job, run once every 3 minutes, check hot coins to see if they are profitable chance.
    '''*/6 * * * * cd /home/preangel/Expenditure_bot && /home/preangel/anaconda3/envs/expenditure_ai/bin/python3 /home/preangel/Expenditure_bot/Binance_check.py >> /home/preangel/Expenditure_bot/cron.log 2>&1'''

    # print current time string format and the function is running
    print(f'\n{datetime.now().strftime("%Y-%m-%d %H:%M")} Binance_check.py is running ...')

    try: binance_today_top_coin()
    except: pass

    try: read_emails()
    except: pass

    if '23:50' < datetime.now().strftime("%H:%M") < '23:59':  profit_taken_today(TG_BOT_OWNER_ID, report = True)