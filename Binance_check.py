from Binance_api import *


if __name__ == '__main__':
    # Crontab job, run once every 3 minutes, check hot coins to see if they are profitable chance.
    '''*/3 * * * * cd /root/Expenditure_bot && /root/anaconda3/envs/expenditure_ai/bin/python3 /root/Expenditure_bot/Binance_check.py >> /root/Expenditure_bot/cron.log 2>&1'''

    try: binance_position_buy_check_all(target_profit=TARGET_PROFIT, coin=None, chat_id=None, crontab_profit_record=False)
    except: pass

