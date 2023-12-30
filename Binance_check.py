from Trading_bot import *
from Gmail_api import *

if __name__ == '__main__':
    # Crontab job, run once every 3 minutes, check hot coins to see if they are profitable chance.
    '''*/5 * * * * cd /home/preangel/Expenditure_bot && /home/preangel/anaconda3/envs/expenditure_ai/bin/python3 /home/preangel/Expenditure_bot/Binance_check.py >> /home/preangel/Expenditure_bot/cron.log 2>&1'''

    # print current time string format and the function is running
    print(f'\n{datetime.now().strftime("%Y-%m-%d %H:%M")} Binance_check.py is running ...')

    current_bot_status = False

    try: current_bot_status = trading_bot_switch_status()
    except: pass

    # try: 
    #     long_or_short = analyze_symbol('BTC')
    #     '''{'long': True, 'short': False}'''
    #     long = long_or_short['long']
    #     short = long_or_short['short']

    #     if long and not current_bot_status: 
    #         webhook_switch_on_bot(f"BTC is good to long now. Turning on the bot", TG_BOT_OWNER_ID)
    #         current_bot_status = True
    #     if short and current_bot_status: 
    #         webhook_switch_off_bot(f"BTC is good to short now. Turning off the bot", TG_BOT_OWNER_ID)
    #         current_bot_status = False

    # except: pass

    chat_id = TG_BOT_OWNER_ID if not current_bot_status else None
    try: binance_today_hot_coins_check(chat_id, trading_volume_limit = TRADING_VOLUME_LIMIT, tradingbot_status = current_bot_status)
    except: pass

    try: read_emails()
    except: pass