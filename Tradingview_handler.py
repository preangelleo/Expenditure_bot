from Bot_messages import *


def tradingview_webhook_handler(data):
    '''{"condition": "ON", "message": "1234567", "token": "xxxxxxxxxxxxxx}'''
    '''{"condition": "OFF", "message": "1234567", "token": "xxxxxxxxxxxxxx}'''

    try: condition = data['condition']
    except: return

    message = data.get('message', 'NONE')

    if condition in ['ON', 'OFF']: 
        trading_bot_status = trading_bot_switch_status()

        if not trading_bot_status and condition == 'ON': webhook_switch_on_bot(message, TG_BOT_OWNER_ID)
        elif trading_bot_status and condition == 'OFF': webhook_switch_off_bot(message, TG_BOT_OWNER_ID)

        return
    
    if condition in ['ALERT']: return send_msg(message, TG_BOT_OWNER_ID)

    return



# Run the application
if __name__ == '__main__':
    print('RUNNING: Tradingview_handler.py')
