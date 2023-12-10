from Trading_bot import *


if __name__ == '__main__':
    # Crontab job, run once every 4 hours, check hot coins to see if they are profitable chance.
    '''0 */4 * * * cd /root/Expenditure_bot && /root/anaconda3/envs/av/bin/python3 /root/Expenditure_bot/Binance_hotcoins.py >> /root/Expenditure_bot/cron.log 2>&1'''

    try: binance_today_hot_coins_check(chat_id=TG_BOT_OWNER_ID, user_nick_name='Dear', crontab=True, trading_volume_limit = TRADING_VOLUME_LIMIT, check_size = CHECK_SIZE)
    except: pass
