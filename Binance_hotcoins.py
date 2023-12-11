from Trading_bot import *


if __name__ == '__main__':
    # Crontab job, run once every 4 hours, check hot coins to see if they are profitable chance.
    '''0 */4 * * * cd /root/Expenditure_bot && /root/anaconda3/envs/expenditure_ai/bin/python3 /root/Expenditure_bot/Binance_hotcoins.py >> /root/Expenditure_bot/cron.log 2>&1'''

    # Check if trading bot is on
    trading_bot_status = trading_bot_switch_status()
    if trading_bot_status:
        # If trading bot is on, check hot coins
        try: binance_today_hot_coins_check(chat_id=TG_BOT_OWNER_ID, user_nick_name='Dear', crontab=True, trading_volume_limit = TRADING_VOLUME_LIMIT, check_size = CHECK_SIZE)
        except: pass
