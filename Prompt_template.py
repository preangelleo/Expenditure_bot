from datetime import datetime

USDT_NETWORK_LIST = ['BSC', 'EOS', 'NEAR', 'AVAXC', 'ARBITRUM', 'STATEMINT', 'BNB', 'ETH', 'OPTIMISM', 'MATIC', 'SOL', 'XTZ', 'TRX', 'OPBNB']
USDT_ETH_COMPATIBLE_NETWORK_LIST = ['ETH', 'BSC', 'MATIC', 'AVAXC', 'ARBITRUM', 'OPTIMISM', 'OPBNB']


INITIAL_IGNORE_LIST = ['BTC', 'ETH', 'XRP', 'AMB', 'LTC', 'ARB', 'BTS', 'SOL', 'JST', 'ADA', 'TRX', 'LUNA', 'LUNC', 'BCH', 'USTC', 'EOS', 'XMR', 'XLM', 'XEM', 'DOGE', 'AVAX', 'OP', 'MATIC', 'APT', 'COCOS', 'BTT', 'BTTT', 'BTTB', 'EUR', 'SUI', 'QTUM', 'DASH', 'ZEC', 'ZEN', 'ZIL', 'ZRX', 'NEO', 'CELO', 'ANKR', 'BNB', 'OMG', 'TUSDT', 'ETC', 'ACA', 'STORJ', 'FTM', 'LQTY', 'OGN', 'RSR', 'VGX', 'MBL', 'COIN98', 'BLZ', 'MC', 'GAS']

ENGLISH_SYSTEM_PROMPT='''Act as an English teacher and dictionary for Chinese students, providing explanations of words, phrases, as well as grammar rules, use case sentences in both English and Chinese, and other relevant information if needed. Indicators : 释义、同义词、例句、笔记 always in Chinese. 笔记 is optional. But if you include it, please make sure put a Chinese translation after. If user send a word with typo, please correct it and reply with the correct word. But if you don't know the correct word, please reply with : Sorry, I don't know this word. If user prompt is a technical term or abbreviation or jargon or terminology or lingo, please reply what it stands for and the meaning in both English and Chinese. '''

ENGLISH_USER_PROMPT = '''ostentatious'''

ENGLISH_ASSISTANT_PROMPT = '''
Ostentatious [ˌɑːstenˈteɪʃəs] 
(adj.) - 炫耀的, 卖弄的, 招摇的

释义: 
Ostentatious describes something or someone that is showy, pretentious, or seeks to attract attention through an extravagant display of wealth, style, or knowledge.
用来形容某物或某人显眼、矫饰或试图通过展示财富、风格或知识的奢华来吸引注意力。

同义词:
pretentious, pompous, showy, bombastic, grandiloquent

例句:
Her ostentatious dress made her stand out at the party.
她在派对上穿着炫耀的裙子, 非常引人注目。

The billionaire's ostentatious lifestyle was criticized in the media.
那位亿万富翁炫耀的生活方式受到了媒体的批评。

词源：
Ostentatious 源于拉丁语 ostentatiōsus, 该词形容词形式来自 ostentatiō, 意为"炫耀"或者"展示"。在英语中, 它的第一个已知使用是在1590年代, 在17世纪和18世纪, 它在文学作品和日常语言中成为一个更常见的词汇, 并且不断发展成为一个更多样化, 更富文化内涵和 metaphorical 意义的词汇。

笔记:
The word "ostentatious" is often used to describe people, clothing, events, or objects that are excessively showy or attention-seeking. It generally carries a negative connotation, implying that the display is unnecessary or in poor taste.
“炫耀”这个词经常用来形容过分炫耀或寻求关注的人、服装、活动或物品。它通常带有负面含义, 暗示这种展示是不必要的或品味不高。
'''

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
    {'command': 'chatgpt', 'description': 'Chat with GPT, use /gpt for short'},
    {'command': 'set_bot_menu', 'description': "Set the bot's menu"},
    {'command': 'btc_rsi_chart', 'description': 'Get the BTC 1M, 1w or 1d chart with RSI'},
    {'command': 'get_last_msg', 'description': 'Get the last message from the telegram_messages table'},
    {'command': 'cancel_all_orders', 'description': 'Cancel all orders in Binance'},
    {'command': 'open_orders_list', 'description': 'Get the open orders list in Binance'},
    {'command': 'add_ignore_coin', 'description': 'Add a coin to the ignore list'},
    {'command': 'get_coin_info', 'description': 'Get the information of a given coin symbol'},
    {'command': 'get_stock_info', 'description': 'Get the information of a given stock symbol'},
    {'command': 'get_ignore_list', 'description': 'Get the ignore list'},
    {'command': 'get_expenditure_now', 'description': 'Get the total spend of this year and this month'},
    {'command': 'get_expenditure_info', 'description': 'Get the total spend of any given year and month'},
    {'command': 'alter_expenditure_record', 'description': 'Alter the expenditure record'},
    {'command': 'sum_category_merchant', 'description': 'Sum the total spend of a given category and merchant'},
    {'command': 'hot_coins_check', 'description': 'Check hot coins of today'},
    {'command': 'analyze_symbol', 'description': 'Analyze if current time is positive to buy a given coin'},
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
    {'command': 'get_fibonacci_sequence', 'description': 'Get the fibonacci sequence of a given number'},
    {'command': 'calculate_irr', 'description': 'Calculate the IRR of a given return folds and years of investment'},
    {"command": "gemini", "description": "Calling Gemini API of Google to generate the answer"},
    {"command": "hash_sha256", "description": "Hash the input string with sha256"},
    {"command": "hash_md5", "description": "Hash the input string with md5"},
    {"command": "save_trivial_record", "description": "Save some information into the table 'trivial_records'"},
    {"command": "search_trivial_records", "description": "Search the information from the table 'trivial_records' by keywords"},
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
    }, {
        "type": "function",
        "function": {
            "name": "get_stock_info",
            "description": "Get the information of a given stock symbol",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "The symbol of the stock, for example: AAPL, if user input a company name, convert it to symbol"},
                    "from_id": {"type": "string", "description": "The user's telegram id"}                    
                },
                "required": ["symbol", "from_id"]
            }
        }
    }, {
        "type": "function",
        "function": {
            "name": "get_token_info",
            "description": "Get the infomation of a given token from coinmarketcap and send to user, information include marke cap, trading volume, current price, ranking, coinmarketcap url, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "coin": {"type": "string", "description": "The coin symbol, for example: BTC, ETH, SOL, etc."},
                    "from_id": {"type": "string", "description": "The user's telegram id"}                    
                },
                "required": ["coin", "from_id"]
            }
        }
    }, {
        "type": "function",
        "function": {
            "name": "save_trivial_record",
            "description": "Save given information into the table 'trivial_records' (for notes only, not for expenditure records)",
            "parameters": {
                "type": "object",
                "properties": {
                    "info": {"type": "string", "description": "The information to be saved"},
                    "from_id": {"type": "string", "description": "The user's telegram id"}                    
                },
                "required": ["info", "from_id"]
            }
        }
    }, {
        "type": "function",
        "function": {
            "name": "search_trivial_records",
            "description": "Search the information by keywords from the table 'trivial_records' (for notes only, not for expenditure records)",
            "parameters": {
                "type": "object",
                "properties": {
                    "key_word": {"type": "string", "description": "The key word to search"},
                    "from_id": {"type": "string", "description": "The user's telegram id"}                    
                },
                "required": ["key_word", "from_id"]
            }
        }
    }, {
        "type": "function",
        "function": {
            "name": "analyze_symbol_for_user",
            "description": "Analyze if current time is positive to buy a given coin",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "The symbol of the coin, for example: BTC, ETH, SOL, etc."},
                    "from_id": {"type": "string", "description": "The user's telegram id"}                    
                },
                "required": ["symbol", "from_id"]
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
- get_stock_info: Get the information of a given stock symbol from yahoo finance, information include marke cap, trading volume, current price, sector, industry, etc.
- get_token_info: Get the infomation of a given token from coinmarketcap and send to user, information include marke cap, trading volume, current price, ranking, coinmarketcap url, etc.
- save_trivial_record: Save given information into the table 'trivial_records' (for notes only, not for expenditure records)
- search_trivial_records: Search the information by keywords from the table 'trivial_records' (for notes only, not for expenditure records)
- analyze_symbol_for_user: Analyze if current time is positive to buy a given coin
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
    'ts': "Translate the below text from Chinese to English or from English to Chinese\n",
    'translate': "Translate the below text from Chinese to English or from English to Chinese\n",
    'revise': "Revise the below text in same language but in a cincise and delicate way\n",
    'refine': "Refine the below text in same language but in a cincise and delicate way\n",
    'concise': 'Concisely revise the below text in same language in a delicate way\n',
    'summarize': 'Summarize the below text concisely in the same language with bullet points.\n',
    'sum': 'Summarize the below text concisely in the same language with bullet points.\n',
    'save': 'save_trivial_record',
    'find': 'search_trivial_records',
    'search': 'gemini',
    'google': 'gemini',
    'gg': 'gemini',
    'hs': 'hash_sha256',
    'sha': 'hash_sha256',
    'md': 'hash_md5',
    'md5': 'hash_md5',
    'glm': 'get_last_msg',
    'sbm': 'set_bot_menu',
    'aic': 'add_ignore_coin',
    'add_ignore': 'add_ignore_coin',
    'add_coin': 'add_ignore_coin',
    'ric': 'remove_ignore_coin',
    'remove_ignore': 'remove_ignore_coin',
    'remove_coin': 'remove_ignore_coin',
    'gci': 'get_coin_info',
    'get_coin': 'get_coin_info',
    'get_info': 'get_coin_info',
    'coin_info': 'get_coin_info',
    'cmc': 'get_coin_info',
    'token_info': 'get_coin_info',
    'coinmarketcap': 'get_coin_info',
    'coin': 'get_coin_info',
    'crypto': 'get_coin_info',
    'token': 'get_coin_info',
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
    'gfs': 'get_fibonacci_sequence',
    'fibonacci_sequence': 'get_fibonacci_sequence',
    'fibonacci': 'get_fibonacci_sequence',
    'fib': 'get_fibonacci_sequence',
    'cir': 'calculate_irr',
    'irr': 'calculate_irr',
    'scm': 'sum_category_merchant',
    'cms': 'sum_category_merchant',
    'sum_merchant': 'sum_category_merchant',
    'sum_category': 'sum_category_merchant',
    'smc': 'sum_category_merchant',
    'gsi': 'get_stock_info',
    'get_stock': 'get_stock_info',
    'stock_info': 'get_stock_info',
    'stock': 'get_stock_info',
    'as': 'analyze_symbol',
    'ac': 'analyze_symbol',
    'gpt': 'chatgpt',
    }