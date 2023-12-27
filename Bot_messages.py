from Trading_bot import *
from English_bot import *
from Gemini_gpt import *

# aiogram 3.2.0
# https://docs.aiogram.dev/en/latest/index.html

# Bot token can be obtained via https://t.me/BotFather
TOKEN = os.getenv('TELEGRAM_TOKEN')
USER_TELEGRAM_LINK = os.getenv('USER_TELEGRAM_LINK')

TELEGRAM_BOT_WEBHOOK_TOKEN = os.getenv('TELEGRAM_BOT_WEBHOOK_TOKEN')

TELEGRAM_BASE_URL = f'https://api.telegram.org/bot{TOKEN}/'
RESET_TELEGRAM_TOKEN = os.getenv('RESET_TELEGRAM_TOKEN')

# All handlers should be attached to the Router (or Dispatcher)
# dp = Dispatcher()

# Function to set the bot commands
def set_commands(from_id=TG_BOT_OWNER_ID):
    url = TELEGRAM_BASE_URL + 'setMyCommands'
    response = requests.post(url, json={'commands': COMMANDS})
    if response.status_code == 200: send_msg('Trading bot menu reset...', from_id)
    else: send_msg(f'Failed to set menu commands...\n\n{response.text}', from_id)


NONE_PARAMETER_COMMAND_LIST = {
    'set_bot_menu': set_commands,
    'get_ignore_list': get_ignore_list, 
    'get_white_list': get_white_list,
    'get_expenditure_now': get_total_spend_of_any_year_any_month,
    'get_last_msg': get_latest_message_from_telegram_messages_table,
    'hot_coins_check': only_check_hot_coins,
    'funding_main_transfer': funding_main_transfer_all_usdt,
    'get_wallet_balance': get_coin_wallet_balance_all_str,
    'binance_position_check': bot_call_binance_position_check,
    'switch_on_bot': switch_on_bot,
    'switch_off_bot': switch_off_bot,
    'read_bot_status': read_trading_bot_status,
    'close_postive_positions': close_postive_positions,
    'read_target_profit': read_target_profit_default,
    'open_orders_list': get_open_orders_list,
    'cancel_all_orders': binance_cancel_all_orders,
    'read_positions_limit': read_positions_limit,
    'hot_coin_update': calculate_hot_coin_price_change,
    'get_future_profit': get_umfuture_profit,
    }


ONE_PARAMETER_COMMAND_LIST = {
    'add_ignore_coin': {'function': add_coin_to_ignore_list, 'description': 'You need to input a coin symbol after this command, for example: /add_ignore_coin BTC'},
    'add_white_list': {'function': add_coin_to_white_list, 'description': 'You need to input a coin symbol after this command, for example: /add_white_list BTC'},
    'get_coin_info': {'function': get_token_info, 'description': 'You need to input a coin symbol after this command, for example: /get_coin_info BTC'},
    'get_stock_info': {'function': get_stock_info, 'description': 'You need to input a stock symbol after this command, for example: /get_stock_info AAPL'},
    'position_coin_check': {'function': bot_call_binance_position_check_coin, 'description': 'You need to input a coin symbol after this command, for example: /position_coin_check BTC'},
    'binance_market_sell': {'function': force_do_market_sell, 'description': 'You need to input a coin symbol after this command, for example: /binance_market_sell FTT'},
    'binance_market_buy': {'function': manually_market_buy_one_unit, 'description': 'You need to input a coin symbol after this command, for example: /binance_market_buy CAKE'},
    'close_all_positions': {'function': close_all_positions, 'description': 'You need to input CONFIRM after this command, for example: /close_all_positions CONFIRM'},
    'set_target_profit': {'function': set_new_target_profit, 'description': 'You need to input a target profit after this command, for example: /set_target_profit 0.07'},
    'remove_ignore_coin': {'function': remove_from_ignore_coin_list, 'description': 'You need to input a coin symbol after this command, for example: /remove_ignore_coin BTC'},
    'remove_white_list': {'function': remove_from_white_list, 'description': 'You need to input a coin symbol after this command, for example: /remove_white_list BTC'},
    'set_limit_sell': {'function': binance_position_set_limit_sell, 'description': 'You need to input target profit after this command, for example: /set_limit_sell 0.01'},
    'btc_rsi_chart': {'function': get_btc_data_with_rsi, 'description': 'You need to input a timeframe (1d, 1w, 1M) after this command, for example: /btc_rsi_chart 1d'},
    'set_position_limit': {'function': set_position_limit_by_user, 'description': 'You need to input a coin symbol and a position limit after this command, for example: /set_position_limit 5'},
    'get_fibonacci_sequence': {'function': fibonacci_sequence, 'description': 'You need to input a number after this command, for example: /fibonacci_sequence 10'},
    'analyze_symbol': {'function': analyze_symbol_for_user, 'description': 'You need to input a coin symbol after this command, for example: /analyze_symbol BTC'},
    'summarize_the_url': {'function': summarize_the_url, 'description': 'You need to input a url after this command, for example: /summarize_the_url https://www.binance.com/en/trade/BTC_USDT'},
    'latest_sell_price': {'function': read_latest_sell_price, 'description': 'You need to input a coin symbol after this command, for example: /latest_sell_price BTC'},
    'get_otp': {'function': get_otp, 'description': 'You need to input a app_name after this command, for example: /get_otp carta'},
    'confirm_token': {'function': binance_withdraw_task_update, 'description': 'You need to input a token after this command, for example: /confirm_token 7Xa5r7QSRC_4Hsr0HwdpAA'},
    }

TWO_PARAMETER_COMMAND_LIST = {
    'coin_deposit_address': {'function': get_coin_deposit_address, 'description': 'You need to input a coin symbol and network name after this command, for example: /coin_deposit_address USDT TRX'},
    'get_expenditure_info': {'function': get_total_spend_of_given_year_and_month, 'description': 'You need to input a year and a month after this command, for example: /get_expenditure_info 2023 12'},
    'calculate_irr': {'function': calculate_irr, 'description': 'You need to input a year and a month after this command, for example, calulate a 7 folds return in 10 years: /calculate_irr 7 10'},
    'calculate_coin_valuation': {'function': calculate_coin_valuation, 'description': 'You need to input a coin symbol and a quantity after this command, for example: /calculate_coin_valuation RSR 100000000'},
    'insert_otp': {'function': insert_otp, 'description': 'You need to input a app_name and a passcode_key after this command, for example: /insert_otp carta your_passcode_key_here'},
    'binance_pay_usdt': {'function': binance_pay_usdt, 'description': 'You need to input an amount and a target TRX address after this command, for example: /binance_pay_usdt 100 TQKgU4QRWpfoUYBno6dG8USABkeYQRvQ72'},
    'manually_limit_order': {'function': manually_limit_order, 'description': 'You need to input a coin symbol, a target profit after this command, for example: /manually_limit_order BONK 0.1'},
    }

THREE_PARAMETER_COMMAND_LIST = {
    'alter_expenditure_record': {'function': alter_expenditure_record, 'description': f'You need to input id column_name new_value after this command, for example: \n/alter_record 103 Spent 47000\n\nColumn Names:\n{EXPENDITURE_COLUMNS_STR}'},
    'transfer_between_accounts': {'function': transfer_between_accounts, 'description': 'You need to input a coin symbol, amount and transfer_type after this command, for example: /transfer_between_accounts USDT 1000 MAIN_UMFUTURE or /transfer_between_accounts USDT 1000 UMFUTURE_MAIN'},
    }

FOUR_PARAMETER_COMMAND_LIST = {
    'binance_send_coin': {'function': binance_send_coin, 'description': '/binance_send_coin 100 BSC USDT 0xb411B974c0ac75C88E5039ea0bf63a84aa7B5377'},
    'sum_category_merchant': {'function': get_total_spend_of_given_year_and_month_for_a_given_category_and_merchant, 'description': 'You need to input a year, a month, a category and a merchant after this command, for example: /sum_category_merchant 2022 12 Electronics Amazon or /sum 2023 12 Electronics ALL or /scm 2023 12 ALL Amazon'},
    }

SENTENCE_AS_PARAMETER_COMMAND_LIST = {
    'gemini': {"function": gemini_gpt, "description": "You need to input a sentence after this command, for example: /gemini What's the meaning of marriage?"},
    'hash_sha256': {"function": hash_sha256_bot, "description": "You need to input a sentence after this command, for example: /hash_sha256_bot Here's the information you want to get hashed by sha256."},
    'hash_md5': {"function": hash_md5_bot, "description": "You need to input a sentence after this command, for example: /hash_md5_bot Here's the information you want to get hashed by md5."},
    'save_trivial_record': {"function": save_trivial_record, "description": "You need to input the information you want to be saved after this command, for example: /save_trivial_record I bought 1 BTC on Dec 1, 2023."},
    'search_trivial_records': {"function": search_trivial_records, "description": "You need to input the keywords you want to search after this command, for example: /search_trivial_records BTC"},
    'chatgpt': {"function": ask_gpt, "description": "You need to input a sentence after this command, for example: /chatgpt What is LLM?"},
    }


# Define a handler for telegram messages from webhook
def handel_telegram_message_from_webhook(message):

    # If sender's chat_id is not TG_BOT_OWNER_ID, then ignore the message
    from_id = message['from']['id']
    message_id = message['message_id']
    text_prompt = message.get('text', None)

    reply_to_message = None
    # Check if there's a reply_to_message, if yes, put the text of the reply_to_message to text_prompt
    if 'reply_to_message' in message:

        # Check if there's image in reply_to_message, return
        # if 'photo' in message['reply_to_message']: return

        reply_to_message = message['reply_to_message'].get('text', None)
        if not reply_to_message: return send_msg(random.choice(HAPPY_EMOJI), from_id)

        if text_prompt.lower() in ['email', 'gmail', 'mail', 'backup']: return send_to_gmail_main(reply_to_message)

        # check if there's an email address in the text_prompt
        email_address = re.findall(EMAIL_ADDRESS_REGEX, text_prompt)
        if email_address: 
            for to_address in email_address: 
                send_email(f"FROM TELEGRAM: @{TELEGRAM_OWNER_USERNAME}", f"Sent from python code, DO NOT reply!\n\n{reply_to_message}\n\n{USER_TELEGRAM_LINK}", to_address)
            send_msg(f"Email sent to {email_address} successfully.", from_id)
            return
        
        text_prompt += f"\n\n{reply_to_message}"

    image_url = None

    # check if the message is a photo
    if 'photo' in message:
        # if from_id != TG_BOT_OWNER_ID: return

        '''file_id='AgACAgUAAxkBAAIVx2Vx-uODMrGVAAEL5Q9U1d9w2ECsLAAC5rgxG5oKkFc2W-bswf4s-gEAAwIAA3gAAzME' file_unique_id='AQAD5rgxG5oKkFd9' width=800 height=620 file_size=117042'''
        '''File path: photos/file_53.jpg'''
        '''File url: https://api.telegram.org/file/bot6134874649:AAG6QrYOOD5tvU-3q1sKOBcyfW9LRnx7ZDQ/photos/file_53.jpg'''

        caption = message.get('caption', '')

        file_id = message.get('photo')[-1]['file_id']  # get file_id from message

        # get File object from file_id
        file_info = tg_get_file_path(file_id)
        file_path = file_info.get('file_path', '')
        image_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"  # construct file url
        text_prompt = f"{caption}\n{text_prompt}" if caption else NO_IMAGE_CAPTION_DEFAULT

    if not text_prompt: return send_msg(random.choice(HAPPY_EMOJI), from_id)

    if text_prompt in IGNORE_WORDS: send_msg(random.choice(UNHAPPY_EMOJI), from_id)
    
    if len(text_prompt) <3 or text_prompt in EMOJI_REPLY: return send_msg(random.choice(HAPPY_EMOJI), from_id)

    if text_prompt.lower() in ['help', '/help', 'start', '/start']: return send_msg(BOT_HELP, from_id)

    # Extract the first word from the message, check if it's in COMMAND_LIST
    first_word = text_prompt.split()[0].lower()
    rest_word = text_prompt.split()[1:]

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

    elif not is_command and not rest_word:

        if first_word.startswith('http'): return summarize_the_url(first_word, from_id)

        if first_word.startswith('0x') and len(first_word) == 42: return check_address_balance_return_str(first_word, from_id)

        if len(first_word) < 20:
            r = find_words_for_bot_user(first_word, from_id)
            if not r and len(first_word) <= 5 and len(first_word) >= 3: 
                try: get_token_info(first_word, from_id)
                except: pass
                try: get_stock_info(first_word, from_id)
                except: pass
        return
    
    elif is_command: 
        if first_word.startswith('approve_white_list_'):
            user_from_id = first_word.split('_')[-1]
            if set_white_list_users_status_true(user_from_id): 
                send_msg(f"You've got approved to use this bot by @{TELEGRAM_OWNER_USERNAME}, how can I help you?", user_from_id)
                return send_msg(f"Dear @{TELEGRAM_OWNER_USERNAME}, /{user_from_id} is approved to use this bot.", from_id)
            else: return send_msg(f"Dear @{TELEGRAM_OWNER_USERNAME}, failed to approve /{user_from_id} to use this bot.", from_id)
    
        if check_if_from_id_in_telegram_messages_table(first_word):
            user_from_id = first_word
            forward_msg = ' '.join(rest_word)
            return send_msg(forward_msg, int(user_from_id))
        
        return


    rest_word_joined = ' '.join(rest_word)
    new_prompt = f"{first_word} {rest_word_joined}"

    if new_prompt.split()[0].lower() in ['translate', 'refine', 'revise', 'concisely', 'summarize']: return ask_gpt(new_prompt, from_id)

    try: update_text_for_a_given_message_id(message_id, new_prompt, from_id)
    except: pass

    try: run_conversation_with_functions(chat_id=from_id, model=DEFAULT_MODEL, image_url=image_url, prompt = new_prompt, message_id=message_id)
    except Exception as e: send_msg(f"Failed...\n\n{e}", from_id)


# def a function to handle non-owner messages, input is update
def handel_telegram_message_from_webhook_non_owner(message):

    from_id = message['from']['id']
    text_prompt = message.get('text', None)

    if not text_prompt: return send_msg(random.choice(HAPPY_EMOJI), from_id)

    if text_prompt.lower() in ['who am i', 'whoami', 'who am i?', 'whoami?', 'who_am_i', 'who', 'woshishui', '我是谁', 'fromid', 'chatid', 'username', 'name', 'id', 'me', 'wo', '谁', 'from', 'chat']: 
        return send_msg(f"from_id: {from_id}\nuser_name: {message['from'].get('username', 'unknow')}\nfirst_name: {message['from'].get('first_name', 'unknow')}\nlast_name: {message['from'].get('last_name', 'unknow')}", from_id)

    if text_prompt in IGNORE_WORDS: send_msg(random.choice(UNHAPPY_EMOJI), from_id)
    
    if len(text_prompt) <3 or text_prompt in EMOJI_REPLY: return send_msg(random.choice(HAPPY_EMOJI), from_id)

    if text_prompt.lower() in ['help', '/help', 'start', '/start']: 
        user_name = message['from'].get('username')
        if not user_name: return send_msg(f"Sorry, before you can use this bot, please set your telegram username first.", from_id)

        reply_msg = f'''Hello, please click below command to aply for whitelist to use this bot.\n\n/Apply_White_List'''
        return send_msg(reply_msg, from_id)
    
    if text_prompt.startswith('/Apply_White_List'):
        user_name = message['from'].get('username')
        if not user_name: return send_msg(f"Sorry, before you can use this bot, please set your telegram username first.", from_id)
        
        first_name = message['from'].get('first_name', None)
        last_name = message['from'].get('last_name', None)

        try: r = insert_white_list_users(from_id, user_name, first_name, last_name, status=False)
        except: r = False

        msg_to_bot_owner = f'''Dear @{TELEGRAM_OWNER_USERNAME}, \n\n@{user_name} /{from_id} is applying for whitelist, click below command to approve.\n\n/Approve_White_List_{from_id}'''
        send_msg(msg_to_bot_owner, TG_BOT_OWNER_ID)

        msg_to_user = r if r else f'''Dear @{user_name}, your application is submitted, please wait for approval.\n\n@{TELEGRAM_OWNER_USERNAME}'''

        return send_msg(msg_to_user, from_id)
    

    text_prompt = text_prompt.replace('/', '')

    COMMANDS_LIST_TOTAL = list(NONE_PARAMETER_COMMAND_LIST.keys()) + list(ONE_PARAMETER_COMMAND_LIST.keys()) + list(TWO_PARAMETER_COMMAND_LIST.keys()) + list(THREE_PARAMETER_COMMAND_LIST.keys()) + list(FOUR_PARAMETER_COMMAND_LIST.keys()) + list(SENTENCE_AS_PARAMETER_COMMAND_LIST.keys())

    command_word = text_prompt.lower().split()[0].lower()

    if command_word in COMMANDS_LIST_TOTAL: 
        if str(from_id) in ['5106438350', '5177152210', '1699390662', '2130497801']:
            if command_word in ['get_otp']: 
                app_name = text_prompt.lower().split()[1] if len(text_prompt.lower().split()) > 1 else 'carta'
                return get_otp(app_name, from_id)

        return send_msg(f"Sorry, you are not allowed to use /{command_word} command.", from_id)


    if not check_white_list_users(from_id): 
        message_to_owner = f"/{from_id} Said:\n\n{text_prompt}"
        send_msg(message_to_owner, TG_BOT_OWNER_ID)
        return
    

    return gemini_gpt(text_prompt, from_id)



if __name__ == '__main__':
    print('Running Bot_message.py...')
    update = {
        "update_id": 686490310,
        "message": {
            "message_id": 7684,
            "from": {
            "id": 2118900665,
            "is_bot": False,
            "first_name": "Old_Bro_Leo",
            "username": "laogege6",
            "language_code": "zh-hans",
            "is_premium": True
            },
            "chat": {
            "id": 2118900665,
            "first_name": "Old_Bro_Leo",
            "username": "laogege6",
            "type": "private"
            },
            "date": 1702697072,
            "text": "hs i love you"
        }
        }
    message = update['message']
    handel_telegram_message_from_webhook(message)