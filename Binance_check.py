from Trading_bot import *


if __name__ == '__main__':
    # Crontab job, run once every 3 minutes, check hot coins to see if they are profitable chance.
    '''*/5 * * * * cd /home/preangel/Expenditure_bot && /home/preangel/anaconda3/envs/expenditure_ai/bin/python3 /home/preangel/Expenditure_bot/Binance_check.py >> /home/preangel/Expenditure_bot/cron.log 2>&1'''

    # print current time string format and the function is running
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} Binance_check.py is running ...')

    # Check limit order status
    try: binance_position_status_check(target_profit=TARGET_PROFIT, chat_id=None, crontab_profit_record=False)
    except: pass

    try: 
        # Check if trading bot is on
        trading_bot_status = trading_bot_switch_status()
        if not trading_bot_status: 
            if analyze_symbol('BTCUSDT'): 
                webhook_switch_on_bot(f"BTC is good to buy now. Turning on the bot", TG_BOT_OWNER_ID)
                trading_bot_status = trading_bot_switch_status()

        try: binance_today_hot_coins_check(chat_id=TG_BOT_OWNER_ID, user_nick_name='Dear', crontab=True, trading_volume_limit = TRADING_VOLUME_LIMIT)
        except: pass

    except: pass
