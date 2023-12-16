from Trading_bot import *


if __name__ == '__main__':
    # Crontab job, run once every 4 hours, check hot coins to see if they are profitable chance.
    '''0 */1 * * * cd /home/preangel/Expenditure_bot && /home/preangel/anaconda3/envs/expenditure_ai/bin/python3 /home/preangel/Expenditure_bot/Binance_hotcoins.py >> /home/preangel/Expenditure_bot/cron.log 2>&1'''

    # print current time string format and the function is running
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} Binance_hotcoins.py is running ...')

    # Check if trading bot is on
    trading_bot_status = trading_bot_switch_status()
    if trading_bot_status:
        print(f'Trading bot is on, checking hot coins ...')
        # If trading bot is on, check hot coins
        try: binance_today_hot_coins_check(chat_id=TG_BOT_OWNER_ID, user_nick_name='Dear', crontab=True, trading_volume_limit = TRADING_VOLUME_LIMIT)
        except: pass
    else: print(f'Trading bot is off, not checking hot coins ...')
