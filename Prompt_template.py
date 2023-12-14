from datetime import datetime

USDT_NETWORK_LIST = ['BSC', 'EOS', 'NEAR', 'AVAXC', 'ARBITRUM', 'STATEMINT', 'BNB', 'ETH', 'OPTIMISM', 'MATIC', 'SOL', 'XTZ', 'TRX', 'OPBNB']
USDT_ETH_COMPATIBLE_NETWORK_LIST = ['ETH', 'BSC', 'MATIC', 'AVAXC', 'ARBITRUM', 'OPTIMISM', 'OPBNB']


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


https://leowang.net/bot-help
'''

BOT_HELP = '''https://leowang.net/bot-help'''


NOT_OWNER_ALERT = "Sorry, This bot is only for the owner.\n\nLEOWANG.net"

CATEGORIES = ['Groceries', 'Dining Out', 'Transportation', 'Utilities', 'Rent Mortgage', 'Entertainment', 'Healthcare', 'Clothing', 'Education', 'Travel', 'Personal Care', 'Home Maintenance', 'Gifts Donations', 'Savings Investments', 'Electronics', 'Kids', 'Pets', 'Fitness', 'Insurance', 'Others']

COMMANDS = [
    {'command': 'start', 'description': 'Get started'},
    {'command': 'help', 'description': 'Get help information'},
    {'command': 'reboot_the_bot', 'description': 'Reboot only the trading bot (fast)'},
    {'command': 'reboot_the_system', 'description': 'Reboot / restart / reload the system (slow)'},
    {'command': 'btc_rsi_chart', 'description': 'Get the BTC 1M, 1w or 1d chart with RSI'},
    {'command': 'get_last_msg', 'description': 'Get the last message from the telegram_messages table'},
    {'command': 'cancel_all_orders', 'description': 'Cancel all orders in Binance'},
    {'command': 'open_orders_list', 'description': 'Get the open orders list in Binance'},
    {'command': 'add_ignore_coin', 'description': 'Add a coin to the ignore list'},
    {'command': 'get_coin_info', 'description': 'Get the information of a given coin'},
    {'command': 'get_ignore_list', 'description': 'Get the ignore list'},
    {'command': 'get_expenditure_now', 'description': 'Get the total spend of this year and this month'},
    {'command': 'get_expenditure_info', 'description': 'Get the total spend of any given year and month'},
    {'command': 'alter_expenditure_record', 'description': 'Alter the expenditure record'},
    {'command': 'hot_coins_check', 'description': 'Check hot coins of today'},
    {'command': 'funding_main_transfer', 'description': 'Transfer all USDT from Funding to Main account'},
    {'command': 'get_wallet_balance', 'description': 'Get the balance of all coins in the wallet'},
    {'command': 'binance_position_check', 'description': 'Check the positions & profits in Binance'},
    {'command': 'position_coin_check', 'description': 'Check the positions & profits of a given coin in Binance'},
    {'command': 'binance_market_sell', 'description': 'Do market sell of a given coin in Binance'},
    {'command': 'binance_market_buy', 'description': 'Do market buy of a given coin in Binance'},
    {'command': 'coin_deposit_address', 'description': 'Get the deposit address of a given coin and network in Binance'},
    {'command': 'close_all_positions', 'description': 'Close all positions in Binance'},
    {'command': 'switch_on_bot', 'description': 'Switch on the trading bot (start to buy hot coins))'},
    {'command': 'switch_off_bot', 'description': 'Switch off the trading bot (sell only)'},
    {'command': 'read_bot_status', 'description': 'Read the status of the trading bot'},
    {'command': 'close_postive_positions', 'description': 'Close all postive positions in Binance'},
    {'command': 'set_target_profit', 'description': 'Set the target profit of the trading bot'},
    {'command': 'set_position_limit', 'description': 'Set the position limit of the trading bot'},
    {'command': 'remove_ignore_coin', 'description': 'Remove a coin from the ignore list'},
    {'command': 'read_target_profit', 'description': 'Read current target profit setting of the trading bot'},
    {'command': 'set_limit_sell', 'description': 'Set limit sell order for a target profit pencentage'},
    ]



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
                    "category": {"type": "string", "description": f"The category of the expenditure record, chose from: Groceries, Dining Out, Transportation, Utilities, Rent Mortgage, Entertainment, Healthcare, Clothing, Education, Travel, Personal Care, Home Maintenance, Gifts Donations, Savings Investments, Electronics, Kids, Pets, Fitness, Insurance, Others"},
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
- insert_new_expenditure_record: Insert a spending record from a receipt into the table 'user_expenditures_record'
- get_total_spend_of_any_year_any_month: Get the total spend of given year and given month
- add_coin_to_ignore_list: Add a coin to the ignore_coin_list table
- get_ignore_list: Read out ignore_list table and return a list of ignored coins
- funding_main_transfer_all_usdt: Transfer all USDT from funding account to main account
- get_btc_data_with_rsi: Get BTC weeky, daily, or monthly data chart with RSI
'''

IMAGE_INPUT = '''
Your task is to determine if the input image is a receipt. If it's not a receipt, and there's no specific prompt from the user, then respond just: Nice picture. 
If it is a receipt, read and extract the information follow the guidlines.'''

SYSTEM_PROMPT_TEXT_INPUT = f'''You are a multifunctional GPT with many functions ready to be called. Determine which function below you could call based on the user input. 

Functions you could call:
{LIST_OF_FUNCTIONS_WITH_DISCRIPTION}

If among above functions, you don't have any function to call to fulfill user's request, then check below commands list see if any of them might be suitable for the user's request. 

- If any, tell user the command (the command must start with '/' in order to make the command clickable, for example: /btc_rsi_chart ) and don't forget provide a description. 
- If not, then just respond with your own knowledge. You could answer sorry I don't know if you indeed don't know how to answer.

Commands user could use by themselves:
{COMMANDS}'''


RECEIPT_GUIDELINES = f'''Guidelines to polish the receipt information:

1. Read only the total spent or cost of this entire receipt, igore the details of each item.
2. If the receipt lacks a date and time, use: `{datetime.now().strftime('%Y-%m-%d')}` and `{datetime.now().strftime('%H:%M')}` respectively.
3. Chose the closest category from list: 'Groceries', 'Dining Out', 'Transportation', 'Utilities', 'Rent Mortgage', 'Entertainment', 'Healthcare', 'Clothing', 'Education', 'Travel', 'Personal Care', 'Home Maintenance', 'Gifts Donations', 'Savings Investments', 'Electronics', 'Kids', 'Pets', 'Fitness', 'Insurance', 'Others'.
4. If 'spent' is not specified, use the 'price' as the 'spent' value, vice versa.
5. Default to 'Credit Card' if `payment_method` is unspecified.
6. If the `merchant` is not mentioned, use 'Unknown'.
7. Use 'Multiple Items' for multiple items receipt; Use actually item name when there's only one item_name.
8. Default `card_number` to '0000' if it's missing.
9. Use 0 for `tax` if it's not provided.
10. Default `tips` to 0 if absent.
11. If the `address` is missing, use 'Unknown Address'.
12. Use 'Unknown' if the `receipt_image_url` is not provided.
13. Ignore the record if both 'spent' and 'price' are missing.
'''

SYSTEM_PROMPT_WITH_IMAGE_INPUT = f'''
{IMAGE_INPUT}
{RECEIPT_GUIDELINES}
'''

NO_IMAGE_CAPTION_DEFAULT = '''Follow your system prompt instruction and extract needed information from this image.'''

PREFIX_PROMPT_FOR_RECEIPT_PROCESS = 'Extract info from this receipt text and call function insert_new_expenditure_record to save the record in my table.'

HAPPY_EMOJI = ['🤨', '😆', '😙', '🤫', '😅', '😚', '😋', '😗', '😃', '😍', '🙂', '🤪', '😄', '🤩', '🤔', '😁', '😉', '😊', '😎', '🤭', '😘', '🤗', '😂', '🙈']

UNHAPPY_EMOJI = ['😳', '😢', '😕', '😨', '😦', '😧', '😤', '😥', '😰', '😟', '😬', '😣', '😩', '😱', '😓', '🤪', '😠', '😔', '😡', '😞', '🤬', '😵', '😖', '😒', '🤯']

IGNORE_WORDS = ['傻屄', '傻b', '傻x', '傻吊', '傻逼', '傻屌', '傻比', '傻狍子', '脱衣服', '脱了', '妈逼', '妈比', '妈的', '狗日', '狗屁', '狗屎', '狗娘', '做爱', '嘿咻', '啪啪', '插入', '艹', '草泥', '日逼', '奴仆', '奴隶']

EMOJI_REPLY = ['ding', 'hello', 'lol', 'hi', '你好', '你好啊', 'chatgpt', 'gpt', '机器人', 'openai', 'ai', 'nice', 'ok', 'great', 'cool', '你好呀', '你在干嘛', '嘛呢', '亲', '在吗', '睡了吗', '呵呵', '哈哈']

EXPENDITURE_COLUMNS = ["ID", "From_id", "Date", "Time", "Spent", "Category", "PaymentMethod", "Merchant", "ItemName", "Price", "Card_Number", "Tax", "Tips", "Address", "Receipt_Image_URL"]
EXPENDITURE_COLUMNS_STR = ', '.join(EXPENDITURE_COLUMNS)



BOT_COMMAND_DICT = {
    'traderjoe': "Extract the receipt from Trader Joe's and call function: insert_new_expenditure_record to insert the record into the table\n",
    'costco': "Extract the receipt from Costco and call function: insert_new_expenditure_record to insert the record into the table\n",
    'walmart': "Extract the receipt from Walmart and call function: insert_new_expenditure_record to insert the record into the table\n",
    'target': "Extract the receipt from Target and call function: insert_new_expenditure_record to insert the record into the table\n",
    'amazon': "Extract the receipt from Amazon and call function: insert_new_expenditure_record to insert the record into the table\n",
    'wholefoods': "Extract the receipt from Wholefoods and call function: insert_new_expenditure_record to insert the record into the table\n",
    'safeway': "Extract the receipt from Safeway and call function: insert_new_expenditure_record to insert the record into the table\n",
    'bestbuy': "Extract the receipt from Bestbuy and call function: insert_new_expenditure_record to insert the record into the table\n",
    'homedepot': "Extract the receipt from Home Depot and call function: insert_new_expenditure_record to insert the record into the table\n",
    'applestore': "Extract the receipt from Apple Store and call function: insert_new_expenditure_record to insert the record into the table\n",
    'restaurant': "Extract the receipt from a restaurant and call function: insert_new_expenditure_record to insert the record into the table\n",
    'diner': "Extract the receipt from a diner and call function: insert_new_expenditure_record to insert the record into the table\n",
    'lunch': "Extract the receipt from a lunch and call function: insert_new_expenditure_record to insert the record into the table\n",
    'breakfast': "Extract the receipt from a breakfast and call function: insert_new_expenditure_record to insert the record into the table\n",
    'furniture': "Extract the receipt from a furniture store and call function: insert_new_expenditure_record to insert the record into the table\n",
    'grocery': "Extract the receipt from a grocery store and call function: insert_new_expenditure_record to insert the record into the table\n",
    'cvs': "Extract the receipt from CVS and call function: insert_new_expenditure_record to insert the record into the table\n",
    'glm': 'get_last_msg',
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
    'gen': 'get_expenditure_now',
    'hcc': 'hot_coins_check',
    'hot_coins': 'hot_coins_check',
    'fmt': 'funding_main_transfer',
    'funding_transfer': 'funding_main_transfer',
    'funding_main': 'funding_main_transfer',
    'gwb': 'get_wallet_balance',
    'get_wallet': 'get_wallet_balance',
    'bwb': 'get_wallet_balance',
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
    'aer': 'alter_expenditure_record',
    'alter_record': 'alter_expenditure_record',
    'change_expenditure_record': 'alter_expenditure_record',
    'cer': 'alter_expenditure_record',
    'bsc': 'binance_send_coin',
    }