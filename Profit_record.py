from Binance_api import *
from BTC_weekly import *

if __name__ == '__main__':
    # Crontab job, run once a day at 00:00
    '''1 0 * * * cd /root/Expenditure_bot && /root/anaconda3/envs/expenditure_ai/bin/python3 /root/Expenditure_bot/Profit_record.py >> /root/Expenditure_bot/cron.log 2>&1'''

    try: binance_position_buy_check_all(target_profit=TARGET_PROFIT, coin=None, chat_id=None, crontab_profit_record=True)
    except: pass

    try: get_btc_data_with_rsi(chat_id=TG_BOT_OWNER_ID)
    except: pass

