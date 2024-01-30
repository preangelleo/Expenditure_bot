from Bot_messages import *



# Define a handler for telegram messages from webhook
def handel_webhook_push_from_trading_view(token):
    message = validate_webhook_signature(token)
    if not message: return
    # if not set_webhook_signature_used(token): return

    # If sender's chat_id is not TG_BOT_OWNER_ID, then ignore the message
    from_id = TG_BOT_OWNER_ID
    first_word = message.split()[0].lower()
    rest_word = message.split()[1:]

    is_command = False
    # check if first_word starts with '/'
    if first_word.startswith('/'): 
        # Remove '/' from the first word
        first_word = first_word.replace('/', '')
        is_command = True

    first_word = BOT_COMMAND_DICT.get(first_word, first_word)

    if first_word in NONE_PARAMETER_COMMAND_LIST:

        # Get the corresponding function

        func = NONE_PARAMETER_COMMAND_LIST[first_word]

        # Call the function and return
        return func(from_id)
    
    # If the first word is in COMMAND_LIST, then call the corresponding function
    elif first_word in ONE_PARAMETER_COMMAND_LIST:

        # If there's no rest word, then reply the description of the command
        if not rest_word: return send_msg(ONE_PARAMETER_COMMAND_LIST[first_word]['description'], from_id)

        first_parameter = rest_word[0]

        # Get the corresponding function
        func = ONE_PARAMETER_COMMAND_LIST[first_word]['function']

        # Call the function and return
        return func(first_parameter.upper(), from_id)

    elif first_word in TWO_PARAMETER_COMMAND_LIST:

        # If there's no rest word, then reply the description of the command
        if len(rest_word) < 2: return send_msg(TWO_PARAMETER_COMMAND_LIST[first_word]['description'], from_id)

        first_parameter = rest_word[0]
        second_parameter = rest_word[1]

        # Get the corresponding function
        func = TWO_PARAMETER_COMMAND_LIST[first_word]['function']

        # Call the function and return
        return func(first_parameter, second_parameter, from_id)
    
    elif first_word in THREE_PARAMETER_COMMAND_LIST:

        # If there's no rest word, then reply the description of the command
        if len(rest_word) < 3: return send_msg(THREE_PARAMETER_COMMAND_LIST[first_word]['description'], from_id)

        first_parameter = rest_word[0]
        second_parameter = rest_word[1]
        third_parameter = rest_word[2]

        # Get the corresponding function
        func = THREE_PARAMETER_COMMAND_LIST[first_word]['function']

        # Call the function and return
        return func(first_parameter, second_parameter, third_parameter, from_id)
    
    elif first_word in FOUR_PARAMETER_COMMAND_LIST:
            
        # If there's no rest word, then reply the description of the command
        if len(rest_word) < 4: return send_msg(FOUR_PARAMETER_COMMAND_LIST[first_word]['description'], from_id)

        first_parameter = rest_word[0]
        second_parameter = rest_word[1]
        third_parameter = rest_word[2]
        fourth_parameter = rest_word[3]

        # Get the corresponding function
        func = FOUR_PARAMETER_COMMAND_LIST[first_word]['function']

        # Call the function and return
        return func(first_parameter, second_parameter, third_parameter, fourth_parameter, from_id)
    
    elif first_word in SENTENCE_AS_PARAMETER_COMMAND_LIST:

        # If there's no rest word, then reply the description of the command
        if not rest_word: return send_msg(SENTENCE_AS_PARAMETER_COMMAND_LIST[first_word]['description'], from_id)

        # Get the corresponding function
        func = SENTENCE_AS_PARAMETER_COMMAND_LIST[first_word]['function']

        rest_word = ' '.join(rest_word)

        # Call the function and return
        return func(rest_word, from_id)

    elif is_command: 

        if check_if_from_id_in_telegram_messages_table(first_word):
            user_from_id = first_word
            forward_msg = ' '.join(rest_word)
            return send_msg(forward_msg, int(user_from_id))
        
    return


def tradingview_webhook_handler(data):
    condition = data.get('condition', 'NONE')
    message = data.get('message', 'WEBHOOK')
    interval = data.get('interval', 'NONE')
    symbol = data.get('symbol', 'NONE')
    current_price = float(data.get('current_price', 0))
    score = int(float(data.get('score', 0)))
    coin = symbol.replace('BINANCE:', '').replace('USDT', '').replace('USD', '')

    if coin in ['BTC']:
        send_msg(f"BTC {interval}_KDJ turned {condition}\nCurrent price: {current_price}\nScore: {score}", TG_BOT_OWNER_ID)
        if condition == 'ON': 
            reset_target_profit_for_resistance(from_id = TG_BOT_OWNER_ID)
            return webhook_switch_on_bot(message, TG_BOT_OWNER_ID)
        if condition == 'OFF': 
            if interval == '240': reset_target_profit_for_coins(limit_hour = 0, target_profit = 0.01, from_id = TG_BOT_OWNER_ID)
            return webhook_switch_off_bot(message, TG_BOT_OWNER_ID)

    if coin not in ['NONE', 'BTC']:
        is_strong = True if score == 4 else False
        if coin in ['EH', 'HSAI']: return send_email(f"{coin} {interval}_KDJ turned {condition}\nCurrent price: {current_price}\nScore: {score}", get_stock_info(coin), GMAIL_ADDRESS_MAIN)
        
        bot_current_status = trading_bot_switch_status()
        holding_list = read_holding_list()
        if not holding_list: return send_msg("Your holding list is empty! Use below command to add any coin into holding list.\n/hold_RSR", TG_BOT_OWNER_ID)
        is_holding = True if coin in holding_list else False
        step = 0.03 if is_strong and bot_current_status else 0.05 if is_strong else 0.08 if bot_current_status else 0.16
        profit = 0 if is_strong and not bot_current_status else 100

        if condition == 'ON': return coin_create_position(coin, current_price, step, TG_BOT_OWNER_ID, is_holding)
        if condition == 'OFF': return coin_close_position(coin, current_price, profit, TG_BOT_OWNER_ID, is_holding)

    if condition in ['ALERT']: send_msg(message, TG_BOT_OWNER_ID)

    if 'signature' in data: return handel_webhook_push_from_trading_view(data['signature'])

    return



# Run the application
if __name__ == '__main__':
    print('RUNNING: Tradingview_handler.py')
