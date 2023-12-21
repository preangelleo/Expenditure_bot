from BTC_weekly import *
from Trading_bot import *
from Gmail_api import *

if __name__ == '__main__':
    # Crontab job, run once a day at 00:00
    '''15 5 * * * cd /home/preangel/Expenditure_bot && /home/preangel/anaconda3/envs/expenditure_ai/bin/python3 /home/preangel/Expenditure_bot/Profit_record.py >> /home/preangel/Expenditure_bot/cron.log 2>&1'''

    # print current time string format and the function is running
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} Profit_record.py is running ...')


    try: binance_position_buy_check_all(target_profit=TARGET_PROFIT, coin=None, chat_id=None, crontab_profit_record=True)
    except Exception as e: print(f'binance_position_buy_check_all() error:\n\n{e}\n\n')

    try: get_btc_data_with_rsi(timeframe='1d', from_id=TG_BOT_OWNER_ID)
    except Exception as e: print(f'get_btc_data_with_rsi() error:\n\n{e}\n\n')

    try: check_and_buy_bnb(coin = 'BNB', check_limit = 1, chat_id=TG_BOT_OWNER_ID)
    except Exception as e: print(f'check_and_buy_bnb() error:\n\n{e}\n\n')

    try: binance_position_reset_limit_sell(target_profit = 0.01, transactTime = 3, from_id = TG_BOT_OWNER_ID)
    except Exception as e: print(f'binance_position_reset_limit_sell() error:\n\n{e}\n\n')

    try: calculate_hot_coin_price_change()
    except Exception as e: print(f'calculate_hot_coin_price_change() error:\n\n{e}\n\n')

    try: binance_today_hot_coin(trading_volume_limit = TRADING_VOLUME_LIMIT, only_check = True, from_id = TG_BOT_OWNER_ID)
    except Exception as e: print(f'binance_today_hot_coin() error:\n\n{e}\n\n')

    try: send_file(TG_BOT_OWNER_ID, 'cron.log', 'Operation log of crontab job')
    except Exception as e: print(f'send_file() error:\n\n{e}\n\n')

    try: send_email('Profit_record job finished!', f'{datetime.now().strftime("%Y-%m-%d %H:%M")} Profit_record.py has finished successfully!', GMAIL_ADDRESS_MAIN)
    except Exception as e: print(f'send_email() error:\n\n{e}\n\n')