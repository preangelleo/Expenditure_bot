from Binance_api import *



if __name__ == '__main__':
    # Crontab job, run once every 3 minutes, check hot coins to see if they are profitable chance.
    '''*/3 * * * * cd /root/Expenditure_bot && /root/anaconda3/envs/expenditure_ai/bin/python3 /root/Expenditure_bot/Binance_check.py >> /root/Expenditure_bot/cron.log 2>&1'''

    # print current time string format and the function is running
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} Binance_check.py is running ...')

    target_profit = read_target_profit_default()

    TARGET_PROFIT = target_profit if target_profit else float(os.getenv('TARGET_PROFIT', 0.05))

    # try: binance_position_buy_check_all(target_profit=TARGET_PROFIT, coin=None, chat_id=None, crontab_profit_record=False)
    # except: pass

    # Check limit order status
    try: binance_limit_order_status_check(target_profit=TARGET_PROFIT, coin=None, chat_id=None, crontab_profit_record=False)
    except: pass
