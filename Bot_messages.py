from Trading_bot import *
from Prompt_template import *
from GPT_functions import *
from BTC_weekly import *

# aiogram 3.2.0
# https://docs.aiogram.dev/en/latest/index.html

# Bot token can be obtained via https://t.me/BotFather
TOKEN = os.getenv('TELEGRAM_TOKEN')


TELEGRAM_BOT_WEBHOOK_TOKEN = os.getenv('TELEGRAM_BOT_WEBHOOK_TOKEN')

TELEGRAM_BASE_URL = f'https://api.telegram.org/bot{TOKEN}/'

# All handlers should be attached to the Router (or Dispatcher)
# dp = Dispatcher()

# Function to set the bot commands
def set_commands():
    url = TELEGRAM_BASE_URL + 'setMyCommands'
    response = requests.post(url, json={'commands': COMMANDS})
    if response.status_code == 200: send_msg('Trading bot started...', TG_BOT_OWNER_ID)
    else: send_msg(f'Failed to set commands...\n\n{response.text}', TG_BOT_OWNER_ID)

set_commands()

NONE_PARAMETER_COMMAND_LIST = {
    'get_ignore_list': get_ignore_list, 
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
    'reboot_the_bot': reboot_bot,
    'reboot_the_system': reboot_system,
    }

ONE_PARAMETER_COMMAND_LIST = {
    'add_ignore_coin': {'function': add_coin_to_ignore_list, 'description': 'You need to input a coin symbol after this command, for example: /add_ignore_coin BTC'},
    'get_coin_info': {'function': get_token_price_from_coinmarketcap_and_send_msg, 'description': 'You need to input a coin symbol after this command, for example: /get_coin_info BTC'},
    'position_coin_check': {'function': bot_call_binance_position_check_coin, 'description': 'You need to input a coin symbol after this command, for example: /position_coin_check BTC'},
    'binance_market_sell': {'function': force_do_market_sell, 'description': 'You need to input a coin symbol after this command, for example: /binance_market_sell FTT'},
    'binance_market_buy': {'function': do_market_buy_one_unit, 'description': 'You need to input a coin symbol after this command, for example: /binance_market_buy CAKE'},
    'close_all_positions': {'function': close_all_positions, 'description': 'You need to input CONFIRM after this command, for example: /close_all_positions CONFIRM'},
    'set_target_profit': {'function': set_new_target_profit, 'description': 'You need to input a target profit after this command, for example: /set_target_profit 0.07'},
    'remove_ignore_coin': {'function': remove_from_ignore_coin_list, 'description': 'You need to input a coin symbol after this command, for example: /remove_ignore_coin BTC'},
    'set_limit_sell': {'function': binance_position_set_limit_sell, 'description': 'You need to input target profit after this command, for example: /set_limit_sell 0.01'},
    'btc_rsi_chart': {'function': get_btc_data_with_rsi, 'description': 'You need to input a timeframe (1d, 1w, 1M) after this command, for example: /btc_rsi_chart 1d'},
    'set_position_limit': {'function': set_position_limit_by_user, 'description': 'You need to input a coin symbol and a position limit after this command, for example: /set_position_limit 5'},
    }

TWO_PARAMETER_COMMAND_LIST = {
    'coin_deposit_address': {'function': get_coin_deposit_address, 'description': 'You need to input a coin symbol and network name after this command, for example: /coin_deposit_address USDT TRX'},
    'get_expenditure_info': {'function': get_total_spend_of_given_year_and_month, 'description': 'You need to input a year and a month after this command, for example: /get_expenditure_info 2023 12'},
    }

THREE_PARAMETER_COMMAND_LIST = {
    'alter_expenditure_record': {'function': alter_expenditure_record, 'description': f'You need to input id column_name new_value after this command, for example: \n/alter_record 103 Spent 47000\n\nColumn Names:\n{EXPENDITURE_COLUMNS_STR}'},
    }

FOUR_PARAMETER_COMMAND_LIST = {
    'binance_send_coin': {'function': binance_send_coin, 'description': '/binance_send_coin 100 BSC USDT 0xb411B974c0ac75C88E5039ea0bf63a84aa7B5377'},
    }


# Define a handler for telegram messages from webhook
def handel_telegram_message_from_webhook(message):

    # If sender's chat_id is not TG_BOT_OWNER_ID, then ignore the message
    from_id = message['from']['id']
    message_id = message['message_id']
    text_prompt = message.get('text', None)
    # print(f"from_id: {from_id}, text_prompt: {text_prompt}")

    # send_msg(f"from_id: {from_id}, text_prompt: {text_prompt}", from_id)

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

    if text_prompt.lower() in ['help', '/help']: return send_msg(BOT_HELP, from_id)

    # Extract the first word from the message, check if it's in COMMAND_LIST
    first_word = text_prompt.split()[0].lower()
    rest_word = text_prompt.split()[1:]
    # the type of rest_word is list

    # Remove '/' from the first word
    first_word = first_word.replace('/', '')

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
    
    rest_word = ' '.join(rest_word)
    new_prompt = f"{first_word} {rest_word}"

    try: update_text_for_a_given_message_id(message_id, new_prompt, from_id)
    except: pass

    try: run_conversation_with_functions(chat_id=from_id, model=DEFAULT_MODEL, image_url=image_url, prompt = new_prompt, message_id=message_id)
    except Exception as e: send_msg(f"Failed...\n\n{e}", from_id)


if __name__ == '__main__':
    print('Running Bot_message.py...')
