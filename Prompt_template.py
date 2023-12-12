from time import strftime, localtime

INITIAL_IGNORE_LIST = ['BTC', 'ETH', 'XRP', 'AMB', 'LTC', 'ARB', 'BTS', 'SOL', 'JST', 'ADA', 'TRX', 'LUNA', 'LUNC', 'BCH', 'USTC', 'EOS', 'XMR', 'XLM', 'XEM', 'DOGE', 'AVAX', 'OP', 'MATIC', 'APT', 'COCOS', 'BTT', 'BTTT', 'BTTB', 'EUR', 'SUI', 'QTUM', 'DASH', 'ZEC', 'ZEN', 'ZIL', 'ZRX', 'NEO', 'CELO', 'ANKR', 'BNB', 'OMG', 'TUSDT', 'ETC', 'ACA', 'STORJ', 'FTM', 'LQTY', 'OGN', 'RSR', 'VGX', 'MBL', 'COIN98', 'BLZ', 'MC', 'GAS']

# Telegram
WELCOME_FROM_TELEGRAM_BOT = '''You could ask me anything or send your receipt.

Aside from the usual chatbot capabilities, this bot can also help you manage your finances and cryptocurrency investments efficiently. Here's what I can do for you:

- Track Your Expenses: Easily insert any spending details into your expenditure record.

- Monthly Spend Analysis: Get a quick summary of your total spending for any specific year and month.

- Cryptocurrency Management: Add any coin to your ignore list, keeping your focus on preferred investments.

- Review Ignored Coins: Retrieve and review your list of ignored coins whenever you need.

- Funds Transfer: Conveniently transfer all your USDT from the funding account to the main account.

- Bitcoin Data & Analysis: Get detailed Bitcoin data with RSI indicators for various timeframes, helping you make informed decisions.


This GPT Assistant is developed by
LEOWANG.net'''

NOT_OWNER_ALERT = "Sorry, This bot is only for the owner.\n\nLEOWANG.net"

CATEGORIES = ['Groceries', 'Dining Out', 'Transportation', 'Utilities', 'Rent Mortgage', 'Entertainment', 'Healthcare', 'Clothing', 'Education', 'Travel', 'Personal Care', 'Home Maintenance', 'Gifts Donations', 'Savings Investments', 'Electronics', 'Kids', 'Pets', 'Fitness', 'Insurance', 'Others']

FUNCTIONS_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "insert_new_expenditure_record",
            "description": "Insert a item spending record into the table 'user_expenditures_record'",
            "parameters": {
                "type": "object",
                "properties": {
                    "from_id": {"type": "string", "description": "The user's telegram id"},
                    "date": {"type": "string", "description": "The date of the expenditure record in format 'YYYY-MM-DD'"},
                    "time": {"type": "string", "description": "The time of the expenditure record in format 'HH:MM'"},
                    "spent": {"type": "number", "description": "The total amount of the expenditure record"},
                    "category": {"type": "string", "description": "The category of the expenditure record"},
                    "payment_method": {"type": "string", "description": "The payment method of the expenditure record"},
                    "merchant": {"type": "string", "description": "The merchant of the expenditure record"},
                    "item_name": {"type": "string", "description": "The item name of the expenditure record"},
                    "price": {"type": "number", "description": "The price of the expenditure record"},
                    "card_number": {"type": "number", "description": "The last 4 digi of credit / debit card number"},
                    "tax": {"type": "number", "description": "The tax of the expenditure record"},
                    "tips": {"type": "number", "description": "The tips of the expenditure record"},
                    "address": {"type": "string", "description": "The address of the merchant record"},
                    "receipt_image_url": {"type": "string", "description": "The receipt image url of the expenditure record"}
                },
                "required": ["from_id", "date", "time", "spent", "category", "payment_method", "merchant", "item_name", "price", "card_number", "tax", "tips", "address", "receipt_image_url"]
            }
        }
    }, {
        "type": "function",
        "function": {
            "name": "get_total_spend_of_any_year_any_month",
            "description": "Get the total spend of given year and given month",
            "parameters": {
                "type": "object",
                "properties": {
                    "from_id": {"type": "string", "description": "The user's telegram from_id"},
                    "year": {"type": "string", "description": "The year to query, for example: 2022"},
                    "month": {"type": "string", "description": "The month to query, for example: 12"},
                },
                "required": ["from_id", "year", 'month']
            }
        }
    }, {
        "type": "function",
        "function": {
            "name": "add_coin_to_ignore_list",
            "description": "Add a coin to the ignore_coin_list table",
            "parameters": {
                "type": "object",
                "properties": {
                    "coin": {"type": "string", "description": "The upper case coin symbol to be added to the ignore_coin_list table"},
                    "from_id": {"type": "string", "description": "The user's telegram id"}
                },
                "required": ["coin", "from_id"]
            }
        }
    }, {
        "type": "function",
        "function": {
            "name": "get_ignore_list",
            "description": "Read out ignore_list table and return a list of ignored coins",
            "parameters": {
                "type": "object",
                "properties": {
                    "from_id": {"type": "string", "description": "The user's telegram id"}
                },
                "required": ["from_id"]
            }
        }
    }, {
        "type": "function",
        "function": {
            "name": "funding_main_transfer_all_usdt",
            "description": "Transfer all USDT from funding account to main account",
            "parameters": {
                "type": "object",
                "properties": {
                    "from_id": {"type": "string", "description": "The user's telegram id"}
                },
                "required": ["from_id"] 
            }
        }
    }, {
        "type": "function",
        "function": {
            "name": "get_btc_data_with_rsi",
            "description": "Get BTC weeky, daily, or monthly data chart with RSI",
            "parameters": {
                "type": "object",
                "properties": {
                    "timeframe": {"type": "string", "description": "The timeframe of the chart, '1d' for daily, '1w' for weekly, '1M' for monthly"},
                    "from_id": {"type": "string", "description": "The user's telegram id"}                    
                },
                "required": ["timeframe", "from_id"]
            }
        }
    }
     
]

LIST_OF_FUNCTIONS_WITH_DISCRIPTION = '''
List of available_functions:
- insert_new_expenditure_record: Insert a item spending record into the table 'user_expenditures_record'
- get_total_spend_of_any_year_any_month: Get the total spend of given year and given month
- add_coin_to_ignore_list: Add a coin to the ignore_coin_list table
- get_ignore_list: Read out ignore_list table and return a list of ignored coins
- funding_main_transfer_all_usdt: Transfer all USDT from funding account to main account
- get_btc_data_with_rsi: Get BTC weeky, daily, or monthly data chart with RSI
'''

IMAGE_INPUT = '''
Your task is to determine if the input image is a receipt. If it's not a receipt, respond with only quoted words: "Nice picture." 
If it is a receipt, read and extract the information as mush as possible.'''

SYSTEM_PROMPT_TEXT_INPUT = f'''You are a multifunctional GPT with many functions ready to be called. Determine which function to call based on the user input. If user prompt is not related with any function, then just follow the prompt and respond to the user. 

{LIST_OF_FUNCTIONS_WITH_DISCRIPTION}'''


ADITIONAL_INFO = '''
- If user is asking for the price of a token, call function `get_token_price_from_coinmarketcap_and_send_msg`.
- If user is asking for the total spend of a year or a month, call function `get_total_spend_of_any_year_any_month`.
- If it is a receipt, read and extract the information and create parameters for function `insert_new_expenditure_record` to insert each item as a new row in the table. You could ignore the items that spend lower than 5 dollars if the list is too long, but make sure including other items comprehensively. Do not need to record total amount into the table. When you prepare the parameters, for each function call.'''

RECEIPT_GUIDELINES = f'''Follow these guidelines to polish the receipt information:

1. Use the provided `from_id` in the user prompt. If it's not provided, default to `9999999999`.
2. If the receipt lacks a date and time, use the current date and time in the format `{strftime('%Y-%m-%d', localtime())}` and `{strftime('%H:%M', localtime())}` respectively.
3. If category info is not provided, then you can chose the closest one from list: ['Groceries', 'Dining Out', 'Transportation', 'Utilities', 'Rent Mortgage', 'Entertainment', 'Healthcare', 'Clothing', 'Education', 'Travel', 'Personal Care', 'Home Maintenance', 'Gifts Donations', 'Savings Investments', 'Electronics', 'Kids', 'Pets', 'Fitness', 'Insurance', 'Others'].
4. If 'spent' is not specified, use the 'price' as the 'spent' value.
5. Default to 'Credit Card' if `payment_method` is unspecified.
6. If the `merchant` is not mentioned, use 'Unknown'.
7. Use 'Unclear' for unspecified `item_name`.
8. Default `card_number` to '0000' if it's missing.
9. Use 0 for `tax` if it's not provided.
10. Default `tips` to 0 if absent.
11. If the `address` is missing, use 'Unknown Address'.
12. Use 'Unknown' if the `receipt_image_url` is not provided.
13. Ignore the record if both 'spent' and 'price' are missing.'''

SYSTEM_PROMPT_WITH_IMAGE_INPUT = f'''
{IMAGE_INPUT}
{RECEIPT_GUIDELINES}
'''

NO_IMAGE_CAPTION_DEFAULT = '''Extract receipt information from this image and follow your system prompt instruction.'''


HAPPY_EMOJI = ['🤨', '😆', '😙', '🤫', '😅', '😚', '😋', '😗', '😃', '😍', '🙂', '🤪', '😄', '🤩', '🤔', '😁', '😉', '😊', '😎', '🤭', '😘', '🤗', '😂', '🙈']

UNHAPPY_EMOJI = ['😳', '😢', '😕', '😨', '😦', '😧', '😤', '😥', '😰', '😟', '😬', '😣', '😩', '😱', '😓', '🤪', '😠', '😔', '😡', '😞', '🤬', '😵', '😖', '😒', '🤯']

IGNORE_WORDS = ['傻屄', '傻b', '傻x', '傻吊', '傻逼', '傻屌', '傻比', '傻狍子', '脱衣服', '脱了', '妈逼', '妈比', '妈的', '狗日', '狗屁', '狗屎', '狗娘', '做爱', '嘿咻', '啪啪', '插入', '艹', '草泥', '日逼', '奴仆', '奴隶']

EMOJI_REPLY = ['ding', 'hello', 'lol', 'hi', '你好', '你好啊', 'chatgpt', 'gpt', '机器人', 'openai', 'ai', 'nice', 'ok', 'great', 'cool', '你好呀', '你在干嘛', '嘛呢', '亲', '在吗', '睡了吗', '呵呵', '哈哈']

BOT_COMMAND_DICT = {
    'aic': 'add_ignore_coin',
    'add_ignore': 'add_ignore_coin',
    'add_coin': 'add_ignore_coin',
    'ric': 'remove_ignore_coin',
    'remove_ignore': 'remove_ignore_coin',
    'remove_coin': 'remove_ignore_coin',
    'gci': 'get_coin_info',
    'get_coin': 'get_coin_info',
    'get_info': 'get_coin_info',
    'cmc': 'get_coin_info',
    'gil': 'get_ignore_list',
    'get_ignore': 'get_ignore_list',
    'gei': 'get_expenditure_info',
    'get_expenditure': 'get_expenditure_info',
    'hcc': 'hot_coins_check',
    'hot_coins': 'hot_coins_check',
    'fmt': 'funding_main_transfer',
    'funding_transfer': 'funding_main_transfer',
    'funding_main': 'funding_main_transfer',
    'gwb': 'get_wallet_balance',
    'get_wallet': 'get_wallet_balance',
    'get_balance': 'get_wallet_balance',
    'bpc': 'binance_position_check',
    'binance_position': 'binance_position_check',
    'binance_check': 'binance_position_check',
    'pcc': 'position_coin_check',
    'position_coin': 'position_coin_check',
    'position_check': 'position_coin_check',
    'bms': 'binance_market_sell',
    'market_sell': 'binance_market_sell',
    'bmb': 'binance_market_buy',
    'market_buy': 'binance_market_buy',
    'cda': 'coin_deposit_address',
    'deposit_address': 'coin_deposit_address',
    'coin_address': 'coin_deposit_address',
    'coin_deposit': 'coin_deposit_address',
    'cap': 'close_all_positions',
    'close_all': 'close_all_positions',
    'son': 'switch_on_bot',
    'switch_on': 'switch_on_bot',
    'sof': 'switch_off_bot',
    'switch_off': 'switch_off_bot',
    'rbs': 'read_bot_status',
    'read_status': 'read_bot_status',
    'cpp': 'close_postive_positions',
    'close_positive': 'close_postive_positions',
    'stp': 'set_target_profit',
    'set_target': 'set_target_profit',
    'set_profit': 'set_target_profit',
    'rtp': 'read_target_profit',
    'read_target': 'read_target_profit',
    'read_profit': 'read_target_profit',
    'rtb': 'reboot_the_bot',
    'reload': 'reboot_the_bot',
    'restart': 'reboot_the_bot',
    'reboot': 'reboot_the_system',
    'sls': 'set_limit_sell',
    'cao': 'cancel_all_orders',
    'cancel_all': 'cancel_all_orders',
    'ool': 'open_orders_list',
    'orders_list': 'open_orders_list',
    'open_orders': 'open_orders_list',
    'gbw': 'get_btc_weekly',
    'brc': 'btc_rsi_chart',
    'btc_chart': 'btc_rsi_chart',
    'rsi_chart': 'btc_rsi_chart',
    'rsi': 'btc_rsi_chart',
    'spl': 'set_position_limit',
    'set_position': 'set_position_limit',
    'set_limit': 'set_position_limit',
    'position_limit': 'set_position_limit',
    }