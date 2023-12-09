import os, re, json, base64, hashlib, math, string, time, uuid, time, urllib, imaplib, email, random, requests, chardet, subprocess, xlrd, pytz, hmac
from datetime import datetime, timedelta, date
from langdetect import detect
import pandas as pd
from eth_account import Account
from mnemonic import Mnemonic
from web3 import Web3, EthereumTesterProvider
from moralis import evm_api
from sqlalchemy import create_engine, text
from sqlalchemy.sql import text
from urllib.parse import urlencode
from urllib.parse import urljoin
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_httpauth import HTTPTokenAuth
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from flask import make_response
from Prompt_template import *
from flask import render_template


# Load environment variables
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

BINANCE_API = os.getenv('BINANCE_LTD_API_KEY')
BINANCE_SECRET = os.getenv('BINANCE_LTD_API_SECRET')

BINANCE_BASE_URL = 'https://api.binance.com'
BINANCE_TICKER_URL = 'https://api.binance.com/api/v3/ticker/24hr'
BINANCE_DEPOSIT_ADDRESS_FOR_ERC20 = '0x34B940120AEB9cadbCc4131fB034aD3B83B0367d'

ETH_NULL_ADDRESS = '0x0000000000000000000000000000000000000000'
ETH_ADDRESS = "0x0000000000000000000000000000000000000000"
ETH_ADDRESS_STD = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

ETH_REGEX = r'0x[a-fA-F0-9]{40}'
TRX_REGEX = r'T[1-9A-HJ-NP-Za-km-z]{33}'
BTC_REGEX = r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$|^[bc1q|bc1p][0-9A-Za-z]{37,62}$'
EMAIL_ADDRESS_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

# 获取环境变量
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Database connection function
def get_db_connection():
    conn = mysql.connector.connect(host=db_host, port=db_port, user=db_user, password=db_password, database=db_name)
    return conn

# 创建数据库引擎
# 格式：dialect+driver://username:password@host:port/database
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
# print(f"DEBUG: engine: {engine}")

INFURA_KEY = os.getenv('INFURA_KEY')
DEBANK_API = os.getenv('DEBANK_API')
CMC_PA_API = os.getenv('CMC_PA_API')
MORALIS_API = os.getenv('MORALIS_API')
ETHERSCAN_API = os.getenv('ETHERSCAN_API')
MONTHLY_FEE = float(os.getenv('MONTHLY_FEE'))
BOTOWNER_CHAT_ID = os.getenv('BOTOWNER_CHAT_ID')
BOTCREATER_CHAT_ID = os.getenv('BOTCREATER_CHAT_ID')
ELEVEN_API_KEY = os.getenv('ELEVEN_API_KEY')
USER_AVATAR_NAME = os.getenv('USER_AVATAR_NAME')
BOT_USERNAME = os.getenv('BOT_USERNAME')

BING_SEARCH_API_KEY = os.getenv("BING_SEARCH_API")
STABILITY_URL = f"https://api.stability.ai/v1/"

ETHERSCAN_WALLET_URL_PREFIX = 'https://etherscan.io/address/'
ETHERSCAN_TX_URL_PREFIX = 'https://etherscan.io/tx/'
ETHERSCAN_TOKEN_URL_PREFIX = 'https://etherscan.io/token/'

BOTCREATER_TELEGRAM_HANDLE = '@laogege6'

BOTCREATER_TEST_BOT = ['leowang_bot', 'Leowang_test_bot', '@Leowin_chat_bot']

# initialize ignore coin list
# init_ignore_coin_list_table()

# IGNORE_LIST = get_all_token_symbol_from_ignore_coin_list_table()
# print(f"DEBUG: IGNORE_LIST: {IGNORE_LIST}")


BOT_OWNER_LIST = [BOTOWNER_CHAT_ID, BOTCREATER_CHAT_ID]

INFURA = "https://mainnet.infura.io/v3/" + INFURA_KEY
web3 = Web3(Web3.HTTPProvider(INFURA))

USER_TELEGRAM_LINK = os.getenv("USER_TELEGRAM_LINK")
TELEGRAM_USERNAME = USER_TELEGRAM_LINK.split('/')[-1]

ETH_REGEX = r'0x[a-fA-F0-9]{40}'
TRX_REGEX = r'T[1-9A-HJ-NP-Za-km-z]{33}'
EMAIL_ADDRESS_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

USDT_ERC20 = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
USDT_ERC20_DECIMALS = 6

USDC_ERC20 = '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
USDC_ERC20_DECIMALS = 6

BINANCE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'X-MBX-APIKEY': BINANCE_API,
    "Content-Type": "application/json"
    }

def format_number(num):
    if not num:
        return 0
    if type(num) is dict:
        print(num)
        return 0
    if type(num) is not str and not float and not int:
        return num
    if type(num) is str:
        try:
            num = float(num)
        except Exception as e:
            return num
    positive = 1 if num >= 0 else -1
    num = abs(num)
    if num >= 1000:
        num = int(num)
        num = num * positive
        num = format(num, ',')
        return num
    if num >= 100:
        num = int(num)
        return num * positive
    if num >= 1:
        num = round(num, 2)
        return num * positive
    if num < 0.0001:
        return num * positive
    if num < 1:
        after_0_num = str(num).split('.')[-1]
        list_number = list(after_0_num)
        for i in range(len(list_number)):
            if int(list_number[i]) != 0:
                zero_num = i
                break
        num = round(num, zero_num + 3)
        return num * positive
    
def hash_md5(content):
    hashed_content = hashlib.md5(str(content).encode('utf-8')).hexdigest()
    return hashed_content

def hash_sha256(content):
    hashed_content = hashlib.sha256(str(content).encode('utf-8')).hexdigest()
    return hashed_content

def markdown_wallet_address(wallet_address):
    markdown_address = f'[{wallet_address[:6]}...{wallet_address[-7:]}]({ETHERSCAN_WALLET_URL_PREFIX}{wallet_address})'
    return markdown_address

def markdown_transaction_hash(hash_tx):
    markdown_tx = f'[{hash_tx[:6]}......{hash_tx[-7:]}]({ETHERSCAN_TX_URL_PREFIX}{hash_tx})'
    return markdown_tx

def markdown_token_address(token_address):
    markdown_token = f'[{token_address[:6]}...{token_address[-7:]}]({ETHERSCAN_TOKEN_URL_PREFIX}{token_address})'
    return markdown_token

def markdown_tokentnxs(address):
    markdown_token = f'[{address[:6]}...{address[-7:]}]({ETHERSCAN_TOKEN_URL_PREFIX}{address}#tokentxns)'
    return markdown_token

# 从 ignore_coin_list 表里面获取所有的 token symbol，返回一个 list
'''
def get_all_token_symbol_from_ignore_coin_list_table():
    if debug: print(f"DEBUG: get_all_token_symbol_from_ignore_coin_list_table()")
    # Create a new session
    with Session() as session:
        # Query the table 'ignore_coin_list' to get all the token_symbol
        all_token_symbol = session.query(IgnoreList.symbol).all()
        # Commit the session
        session.commit()

    # Convert the list of tuple to list
    all_token_symbol = [i[0] for i in all_token_symbol]
    
    return all_token_symbol
'''
def get_all_token_symbol_from_ignore_coin_list_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    # 从 ignore_coin_list 表里面获取所有的 token symbol，返回一个 list
    cursor.execute("SELECT symbol FROM ignore_coin_list")
    all_token_symbol = cursor.fetchall()
    cursor.close()
    conn.close()
    # Convert the list of tuple to list
    all_token_symbol = [i[0] for i in all_token_symbol]
    return all_token_symbol

# 从 Coinmarketcap 给定 token 的价格等数据, 返回一个字典
def get_token_info_from_coinmarketcap(token_symbol):
    # CoinMarketCap API endpoint
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={token_symbol}'

    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': CMC_PA_API}

    response = requests.get(url, headers=headers)
    data = response.json()

    if 'data' in data:
        token_data = data['data']
        token_info = token_data[token_symbol]
        return token_info
    return

# 从 get_token_info_from_coinmarketcap(token_symbol) 读出 token_symbol 的 market_cap 以及 fully_diluted_market_cap
def get_token_market_cap_and_ratio(token_symbol):
    try:
        token_info = get_token_info_from_coinmarketcap(token_symbol)
        if token_info:
            # print(json.dumps(token_info, indent=2))

            market_cap = token_info['quote']['USD']['market_cap']
            fully_diluted_market_cap = token_info['quote']['USD']['fully_diluted_market_cap']
            if fully_diluted_market_cap < 5_000_000_000 and market_cap / fully_diluted_market_cap > 0.5: return {'market_cap': market_cap, 'fully_diluted_market_cap': fully_diluted_market_cap, 'ratio': market_cap / fully_diluted_market_cap}
    except: return 


# difine a function to send telegram message to a chat_id using requests + telegram bot api
def send_msg(message, chat_id=os.getenv('TG_BOT_OWNER_ID')):
    # print(f"Sending message to chat_id: {chat_id}")
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message
        }
        response = requests.post(url, data=data)
        return response.json()
    except Error as e: return {'error': str(e)}, 500
    

'''
Designing a database table structure for an expenditure record:

ID (INTEGER, Primary Key): A unique identifier for each user.
From_id (VARCHAR): The Telegram From_ID of the user who send the receipt image.
Date (DATE): The date of the transaction.
Time (TIME, format HH:MM): The time of the transaction.
Spent (FLOAT): The total amount spent in the transaction.
Category (VARCHAR): The category of the expenditure (e.g., Food, Transport, Bills).
PaymentMethod (VARCHAR): How the payment was made (e.g., Cash, Credit Card, Online Payment).
Merchant (VARCHAR): The name of the merchant or provider.
ItemName (VARCHAR): The name of the item or service purchased.
Price (FLOAT): The price of the individual item or service.
Card_Number (INTEGER): The last four digits of the card used for the transaction.
Tax (FLOAT): The tax amount on the transaction.
Tips (FLOAT): The tips amount, if any.
Address (VARCHAR): The address where the transaction occurred or the address of the merchant.
Receipt_Image_URL (VARCHAR): URL link to the image of the receipt.
'''

def create_expenditure_record_table():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create a new table 'user_expenditures_record'
    cursor.execute("CREATE TABLE IF NOT EXISTS user_expenditures_record (ID INTEGER PRIMARY KEY AUTO_INCREMENT, From_id VARCHAR(255), Date DATE, Time VARCHAR(20), Spent FLOAT, Category VARCHAR(255), PaymentMethod VARCHAR(255), Merchant VARCHAR(255), ItemName TEXT, Price FLOAT, Card_Number INTEGER, Tax FLOAT, Tips FLOAT, Address TEXT, Receipt_Image_URL TEXT)")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    return True

# Define a function to insert a new expenditure record into the table 'user_expenditures_record'
def insert_new_expenditure_record(from_id, date, time, spent, category, payment_method, merchant, item_name, price, card_number, tax, tips, address, receipt_image_url):
    from_id = str(from_id)
    
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()

    # # Delete current user_expenditures_record table
    # cursor.execute("DROP TABLE IF EXISTS user_expenditures_record")
    # # Commit the session
    # conn.commit()

    # Check if the table 'user_expenditures_record' exists
    cursor.execute("SHOW TABLES LIKE 'user_expenditures_record'")
    table_exists = cursor.fetchone()
    if not table_exists: create_expenditure_record_table()
    
    # Insert a new record into the table 'user_expenditures_record'
    cursor.execute("INSERT INTO user_expenditures_record (From_id, Date, Time, Spent, Category, PaymentMethod, Merchant, ItemName, Price, Card_Number, Tax, Tips, Address, Receipt_Image_URL) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s)", (from_id, date, time, spent, category, payment_method, merchant, item_name, price, card_number, tax, tips, address, receipt_image_url))
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    send_msg(f'''Successfully inserted: \n"{item_name} | {spent} usd"''', from_id)
    return 


# Define a function to get all the expenditure records from the table 'user_expenditures_record' as a pandas dataframe
def get_all_expenditure_records(from_id):
    query = f"SELECT * FROM user_expenditures_record WHERE From_id = '{str(from_id)}'"
    df = pd.DataFrame(engine.connect().execute(text(query)).fetchall())
    return df


if __name__ == '__main__':
    # token_symbol = 'RSR'
    # r = get_token_market_cap_and_ratio(token_symbol)
    # print(r)
    # '''{
    # "id": 3964,
    # "name": "Reserve Rights",
    # "symbol": "RSR",
    # "slug": "reserve-rights",
    # "num_market_pairs": 179,
    # "date_added": "2019-05-24T00:00:00.000Z",
    # "tags": [
    #     "store-of-value",
    #     "defi",
    #     "coinbase-ventures-portfolio",
    #     "dcg-portfolio",
    #     "real-world-assets"
    # ],
    # "max_supply": 100000000000,
    # "circulating_supply": 50600000000,
    # "total_supply": 100000000000,
    # "platform": {
    #     "id": 1027,
    #     "name": "Ethereum",
    #     "symbol": "ETH",
    #     "slug": "ethereum",
    #     "token_address": "0x320623b8e4ff03373931769a31fc52a4e78b5d70"
    # },
    # "is_active": 1,
    # "infinite_supply": false,
    # "cmc_rank": 255,
    # "is_fiat": 0,
    # "self_reported_circulating_supply": null,
    # "self_reported_market_cap": null,
    # "tvl_ratio": null,
    # "last_updated": "2023-12-08T04:57:00.000Z",
    # "quote": {
    #     "USD": {
    #     "price": 0.003022959829617387,
    #     "volume_24h": 9627813.39949622,
    #     "volume_change_24h": -10.9172,
    #     "percent_change_1h": -0.3184558,
    #     "percent_change_24h": 1.89929244,
    #     "percent_change_7d": 7.74822681,
    #     "percent_change_30d": 23.45831876,
    #     "percent_change_60d": 67.36675515,
    #     "percent_change_90d": 63.50005519,
    #     "market_cap": 152961767.3786398,
    #     "market_cap_dominance": 0.0095,
    #     "fully_diluted_market_cap": 302295982.96,
    #     "tvl": null,
    #     "last_updated": "2023-12-08T04:57:00.000Z"
    #     }
    # }
    # }
    # {'market_cap': 152961767.3786398, 'fully_diluted_market_cap': 302295982.96, 'ratio': 0.5060000000029103}
    # '''

    from_id = BOTOWNER_CHAT_ID
    df = get_all_expenditure_records(from_id)
    print(df)