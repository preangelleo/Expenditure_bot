from Binance_api import *
from BTC_weekly import *

if __name__ == '__main__':
    # Crontab job, run once a day at 00:00
    '''15 5 * * * cd /root/Expenditure_bot && /root/anaconda3/envs/expenditure_ai/bin/python3 /root/Expenditure_bot/Profit_record.py >> /root/Expenditure_bot/cron.log 2>&1'''

    # print current time string format and the function is running
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} Profit_record.py is running ...')


    try: binance_position_buy_check_all(target_profit=TARGET_PROFIT, coin=None, chat_id=None, crontab_profit_record=True)
    except: pass

    try: get_btc_data_with_rsi(timeframe='1d', from_id=TG_BOT_OWNER_ID)
    except: pass

    try: get_token_price_from_coinmarketcap_and_send_msg('BTC', TG_BOT_OWNER_ID)
    except: pass

    try: send_file(TG_BOT_OWNER_ID, 'cron.log', 'Operation log of crontab job')
    except: pass

