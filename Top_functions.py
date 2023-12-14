import os, re, json, base64, hashlib, math, string, time, uuid, time, urllib, imaplib, email, random, requests, chardet, subprocess, xlrd, pytz, hmac
from datetime import datetime, timedelta, date
from langdetect import detect
import pandas as pd
from eth_account import Account
from mnemonic import Mnemonic
from web3 import Web3, EthereumTesterProvider
# from moralis import evm_api
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
from Database_create import *
from sqlalchemy.exc import SQLAlchemyError
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import ccxt

import numpy as np

from mplfinance.original_flavor import candlestick_ohlc


# Load environment variables
load_dotenv()

# Create database engine
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

PRIVKEY = os.getenv('PRIVKEY')
FULLCHAIN = os.getenv('FULLCHAIN')

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_OWNER_FIRST_NAME = os.getenv('TELEGRAM_OWNER_FIRST_NAME')
TELEGRAM_OWNER_USERNAME = os.getenv('TELEGRAM_OWNER_USERNAME')

TRADINGVIEW_WEBHOOK = os.getenv('TRADINGVIEW_WEBHOOK')
TRADINGVIEW_WEBHOOK_TOKEN = os.getenv('TRADINGVIEW_WEBHOOK_TOKEN')

BINANCE_API = os.getenv('BINANCE_LTD_API_KEY')
BINANCE_SECRET = os.getenv('BINANCE_LTD_API_SECRET')
BINANCE_BASE_URL = os.getenv('BINANCE_BASE_URL')
BINANCE_TICKER_URL = os.getenv('BINANCE_TICKER_URL')
# BINANCE_DEPOSIT_ADDRESS_FOR_ERC20 = os.getenv('BINANCE_DEPOSIT_ADDRESS_FOR_ERC20')

FULLLY_DILUTED_MARKET_CAP_UP_LIMIT = int(os.getenv('FULLLY_DILUTED_MARKET_CAP_UP_LIMIT'))
MARKET_CAP_DOWN_LIMIT = int(os.getenv('MARKET_CAP_DOWN_LIMIT'))
CIRCULATION_RATIO = float(os.getenv('CIRCULATION_RATIO'))

ETH_NULL_ADDRESS = '0x0000000000000000000000000000000000000000'
ETH_ADDRESS = "0x0000000000000000000000000000000000000000"
ETH_ADDRESS_STD = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

ETH_REGEX = r'0x[a-fA-F0-9]{40}'
TRX_REGEX = r'T[1-9A-HJ-NP-Za-km-z]{33}'
BTC_REGEX = r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$|^[bc1q|bc1p][0-9A-Za-z]{37,62}$'
EMAIL_ADDRESS_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

TG_BOT_OWNER_ID = int(os.getenv('TG_BOT_OWNER_ID'))
# BOTCREATER_CHAT_ID = os.getenv('BOTCREATER_CHAT_ID')
CMC_PA_API = os.getenv('CMC_PA_API')

# BOTCREATER_TELEGRAM_HANDLE = os.getenv('BOTCREATER_TELEGRAM_HANDLE')
# DEBANK_API = os.getenv('DEBANK_API')

# MORALIS_API = os.getenv('MORALIS_API')
# ETHERSCAN_API = os.getenv('ETHERSCAN_API')
# ELEVEN_API_KEY = os.getenv('ELEVEN_API_KEY')
# USER_AVATAR_NAME = os.getenv('USER_AVATAR_NAME')
# BOT_USERNAME = os.getenv('BOT_USERNAME')
# BING_SEARCH_API_KEY = os.getenv("BING_SEARCH_API")
# STABILITY_URL = f"https://api.stability.ai/v1/"

ETHERSCAN_WALLET_URL_PREFIX = 'https://etherscan.io/address/'
ETHERSCAN_TX_URL_PREFIX = 'https://etherscan.io/tx/'
ETHERSCAN_TOKEN_URL_PREFIX = 'https://etherscan.io/token/'


INFURA_KEY = os.getenv('INFURA_KEY')
INFURA_URL = os.getenv('INFURA_URL')
INFURA = INFURA_URL + INFURA_KEY
web3 = Web3(Web3.HTTPProvider(INFURA))

# USER_TELEGRAM_LINK = os.getenv("USER_TELEGRAM_LINK")
# TELEGRAM_USERNAME = USER_TELEGRAM_LINK.split('/')[-1]

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

# 从 Coinmarketcap 给定 token 的价格等数据, 返回一个字典
def get_token_info_from_coinmarketcap(token_symbol):
    # print current time string format and the function is running
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} get_token_info_from_coinmarketcap({token_symbol}) is running ...')

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

# Get the turnover ratio of eth from coinmarketcap
def get_turnover_ratio_from_coinmarketcap(coin='ETH'):
    token_info = get_token_info_from_coinmarketcap(coin.upper())
    if not token_info: return 0
    turnover_ratio = token_info['quote']['USD']['volume_24h'] / token_info['quote']['USD']['market_cap']
    turnover_ratio = round(turnover_ratio, 2)
    return turnover_ratio


def get_token_price_from_coinmarketcap_and_send_msg(coin: str, from_id=TG_BOT_OWNER_ID):
    # print current time string format and the function is running
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} get_token_price_from_coinmarketcap_and_send_msg() is running ...')

    token_info = get_token_info_from_coinmarketcap(coin.upper())
    if not token_info: return 

    CMC_LINK = f"https://coinmarketcap.com/currencies/{token_info['slug']}"
    title = f"[{coin}]({CMC_LINK}) | Rank {token_info['cmc_rank']}"
    send_msg_markdown(title, from_id)

    output_dict = {
        'Token_Name': token_info['name'],
        'Market_Cap': f"{format_number(token_info['quote']['USD']['market_cap'])} usd | {token_info['circulating_supply'] / token_info['total_supply'] * 100:.1f}%",
        'Total_Supply': f"{format_number(token_info['total_supply'])} {coin.lower()}",
        'Current_Price': f"{format_number(token_info['quote']['USD']['price'])} usd/{coin.lower()}",
        'FD_Market_Cap': f"{format_number(token_info['quote']['USD']['fully_diluted_market_cap'])} usd",
        'Trading_Volume': f"{format_number(token_info['quote']['USD']['volume_24h'])} usd",
        '24H_Fluctuation': f"{token_info['quote']['USD']['percent_change_24h']:.2f}%",
        'Current_Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    # 用 '\n' join k: v
    output_dict_str = '\n'.join([f"{k}: {v}" for k, v in output_dict.items()])

    if from_id: send_msg(output_dict_str, from_id)

    return True


def tg_get_file_path(file_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getFile"
    payload = { "file_id": file_id}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200: return
        return response.json()['result']
    except Exception as e: return print(f"ERROR: tg_get_file_path() failed: \n{e}")
    

# difine a function to send telegram message to a chat_id using requests + telegram bot api
def send_msg(message, chat_id=TG_BOT_OWNER_ID):
    # print(f"Sending message to chat_id: {chat_id}")
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message
        }
        requests.post(url, data=data)
        return 
    except: return 
    
# define a function to send telegram message to a chat_id using requests + telegram bot api in markdown format
def send_msg_markdown(message, chat_id=TG_BOT_OWNER_ID, parse_mode='Markdown'):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "text": message,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True,
        "disable_notification": True,
        "chat_id": chat_id
    }
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    try: requests.post(url, json=payload, headers=headers)
    except Exception as e: return print(f"ERROR: send_msg_markdown() failed for:\n{e}\n\nOriginal message:\n{message}")

    return True

# Define a test function to test send_msg_markedown(), send a text with markdown format, a URL with a link to the owner
def test_send_msg_markdown(chat_id=TG_BOT_OWNER_ID):
    USER_TELEGRAM_LINK = 'https://leowang.net'
    message = f"Hello, this is a test message with markdown format, [click here]({USER_TELEGRAM_LINK}) to contact the owner."
    return send_msg_markdown(message, chat_id)
    

def send_file(chat_id, file_path, description=''):
    if not file_path or not chat_id: return
    method = "sendDocument?"
    try: files = {'document': open(file_path, 'rb')}
    except Exception as e: return print(f"ERROR: send_file() failed for:\n{e}\n\nOriginal message:\n{file_path}\n\nCan't open file.")
    URL = 'https://api.telegram.org/bot' + TELEGRAM_TOKEN + '/' + method + "chat_id=" + str(chat_id) + "&caption=" + description
    r = ''
    try: r = requests.post(URL, files=files)
    except Exception as e: print(f"ERROR: send_file() failed : \n{e}")
    return r


def send_img(chat_id, file_path, description=''):
    if not file_path or not chat_id: return
    method = "sendPhoto?"
    try: files = {'photo': open(file_path, 'rb')}
    except Exception as e: return print(f"ERROR: send_img() failed for:\n{e}\n\nOriginal message:\n{file_path}\n\nCan't open file.")
    URL = 'https://api.telegram.org/bot' + TELEGRAM_TOKEN + '/' + method + "chat_id=" + str(chat_id) + "&caption=" + description
    r = ''
    try: r = requests.post(URL, files=files)
    except Exception as e: print(f"ERROR: send_img() failed : \n{e}")
    return r


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

# Define a function to insert a new expenditure record into the table 'user_expenditures_record'
def insert_new_expenditure_record(from_id, date, time, spent, category, payment_method, merchant, item_name, price, card_number, tax, tips, address, receipt_image_url):
    from_id = str(from_id)
    
    # Assuming engine is already created as shown in previous examples
    with engine.connect() as connection:
        try:
            # Define your SQL query using SQLAlchemy's text function
            sql = text("""
                INSERT INTO user_expenditures_record 
                (From_id, Date, Time, Spent, Category, PaymentMethod, Merchant, ItemName, Price, Card_Number, Tax, Tips, Address, Receipt_Image_URL) 
                VALUES 
                (:from_id, :date, :time, :spent, :category, :payment_method, :merchant, :item_name, :price, :card_number, :tax, :tips, :address, :receipt_image_url)
            """)

            # Execute the query with the provided parameters
            result = connection.execute(sql, {
                'from_id': from_id, 
                'date': date, 
                'time': time, 
                'spent': spent, 
                'category': category, 
                'payment_method': payment_method, 
                'merchant': merchant, 
                'item_name': item_name, 
                'price': price, 
                'card_number': card_number, 
                'tax': tax, 
                'tips': tips, 
                'address': address, 
                'receipt_image_url': receipt_image_url
            })

            # Commit the transaction
            connection.commit()

            # Read the ID of the last inserted row
            last_row_id = result.lastrowid

            send_msg(f'''Successfully inserted: \n\nID: {last_row_id}\nName: {item_name}\nDate: {date}\nSpent: {spent}\nCategory: {category}\nMerchant: {merchant}\n\n/alter_record {last_row_id} Spent a_new_number''', from_id)

        except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()

    return 


# Alter the value in user_expenditures_record for a given ID and column name and new value
def alter_expenditure_record(id, column_name, new_value, from_id=TG_BOT_OWNER_ID):
    try: id = int(id)
    except: return send_msg(f"ID has to be an integer, your input is {id}", from_id)

    try: new_value = float(new_value)
    except: return send_msg(f"New value has to be a number, your input is {new_value}", from_id)

    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check if the symbol is already in the table
    try: cursor.execute(f"UPDATE user_expenditures_record SET {column_name} = {new_value} WHERE ID = {id}")
    except Exception as e: return send_msg(f"No column name as {column_name} in the table.\n\n{e}", from_id)

    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    return send_msg(f"Successfully updated {column_name} to {format_number(new_value)} for ID {id}", from_id)


# Define a function to get all the expenditure records from the table 'user_expenditures_record' as a pandas dataframe
def get_all_expenditure_records(from_id):
    query = f"SELECT * FROM user_expenditures_record WHERE From_id = '{str(from_id)}'"
    df = pd.DataFrame(engine.connect().execute(text(query)).fetchall())
    return df


# Define a function to pull all of the expdenditure records of given year and month, calculate the total spend of that month and that year
def get_total_spend_of_given_year_and_month(year=str(datetime.now().year), month=str(datetime.now().month), from_id=TG_BOT_OWNER_ID):
    df = get_all_expenditure_records(from_id)
    # Convert the 'date' column to datetime type
    df['Date'] = pd.to_datetime(df['Date'])

    # sort the dataframe by date
    df = df.sort_values(by='Date')

    # save the dataframe to csv file
    df.to_csv('net_profit_daily_record/expenditure_records.csv', index=False)

    try: send_file(from_id, 'net_profit_daily_record/expenditure_records.csv', description='Expenditure records')
    except: pass

    # Convert year and month to int
    try: year = int(year)
    except: return send_msg(f"Year has to be an integer, your input is {year}", from_id)

    try: month = int(month)
    except: return send_msg(f"Month has to be an integer, your input is {month}", from_id)

    # Calculate the total spent of this year (sum the spent of this year)
    total_spend_this_year = df[df['Date'].dt.year == year]['Spent'].sum()

    # Calculate the total spent of this month in this year (sum the spent of this month)
    total_spend_this_month = df[(df['Date'].dt.year == year) & (df['Date'].dt.month == month)]['Spent'].sum()

    # round the total spend of this year and this month, only show inter.
    total_spend_this_year = format_number(total_spend_this_year)
    total_spend_this_month = format_number(total_spend_this_month)

    # Inform user the total spent of this year and this month
    send_msg(f"Total spent of year {year}: {total_spend_this_year} usd\nTotal spent of month {month}: {total_spend_this_month} usd", from_id)

    return

# Define a function to pull all of the expdenditure records of given year and month, calculate the total spend of that month and that year for a given category and merchant
def get_total_spend_of_given_year_and_month_for_a_given_category_and_merchant(year=str(datetime.now().year), month=str(datetime.now().month), category='ALL', merchant='ALL', from_id=TG_BOT_OWNER_ID):
    '''Groceries, Dining Out, Transportation, Utilities, Rent Mortgage, Entertainment, Healthcare, Clothing, Education, Travel, Personal Care, Home Maintenance, Gifts Donations, Savings Investments, Electronics, Kids, Pets, Fitness, Insurance, Others'''

    # Check if the input category upper case is 'ALL'
    if category.upper() == 'ALL' or merchant.upper() == 'ALL': return get_total_spend_of_given_year_and_month(year, month, from_id)

    # Make a unique list of the current category value, and make a unique list of the current merchant value
    df = get_all_expenditure_records(from_id)
    category_list = df['Category'].unique().tolist()
    merchant_list = df['Merchant'].unique().tolist()

    # add 'ALL' to the category list and merchant list
    category_list.append('ALL') 
    merchant_list.append('ALL')

    # Make a dic, key is lower case of category, value is the original category
    category_dic = {k.lower(): k for k in category_list}
    # Make a dic, key is lower case of merchant, value is the original merchant
    merchant_dic = {k.lower(): k for k in merchant_list}

    print(f"{json.dumps(category_dic, indent=4)}\n\n{json.dumps(merchant_dic, indent=4)}")

    category = category.lower()
    merchant = merchant.lower()

    # Check if the input category and merchant are in the list
    if category not in category_dic: return send_msg(f"Category has to be one of the following:\n{category_list}", from_id)
    if merchant not in merchant_dic: return send_msg(f"Merchant has to be one of the following:\n{merchant_list}", from_id)

    # Translate the category and merchant to the original category and merchant
    category_correct = category_dic[category]
    merchant_correct = merchant_dic[merchant]

    query = f"SELECT * FROM user_expenditures_record WHERE From_id = '{str(from_id)}' AND Category = '{category}' AND Merchant = '{merchant}' AND Date LIKE '{year}-{month}%'" if category_correct != 'ALL' and merchant_correct != 'ALL' else f"SELECT * FROM user_expenditures_record WHERE From_id = '{str(from_id)}' AND Merchant = '{merchant}' AND Date LIKE '{year}-{month}%'" if category_correct == 'ALL' and merchant_correct != 'ALL' else f"SELECT * FROM user_expenditures_record WHERE From_id = '{str(from_id)}' AND Category = '{category}' AND Date LIKE '{year}-{month}%'" if category_correct != 'ALL' and merchant_correct == 'ALL' else None

    if not query: return send_msg("Something wrong with the query, please check the code", from_id)

    df = pd.DataFrame(engine.connect().execute(text(query)).fetchall())

    print(df)




# Read out ignore_list table and return a list of ignored coins
def get_ignore_list(from_id = None):
    df = pd.DataFrame(engine.connect().execute(text("SELECT symbol FROM ignore_coin_list")).fetchall())
    ignore_list = df['symbol'].values.tolist()
    if from_id: send_msg(f"Ignore list:\n{', '.join(ignore_list)}", from_id)
    return ignore_list


# define a function to add a given coin to ignore_coin_list table
def add_coin_to_ignore_list(coin: str, from_id = TG_BOT_OWNER_ID):
    coin = coin.upper()
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check if the symbol is already in the table
    cursor.execute(f"SELECT * FROM ignore_coin_list WHERE symbol = '{coin}'")
    result = cursor.fetchall()
    if len(result) == 0: cursor.execute(f"INSERT INTO ignore_coin_list (symbol) VALUES ('{coin}')")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    send_msg(f"Coin {coin} added to ignore list successfully!", from_id)
    return True


# define a function to switch on the trading bot and send a message to the user
def switch_on_bot(from_id):
    if trading_bot_switch_on(): return send_msg("Trading bot has been switched ON!", from_id)
    return send_msg("Failed to switch on trading bot!", from_id)

# define a function to switch off the trading bot and send a message to the user
def switch_off_bot(from_id):
    if trading_bot_switch_off(): return send_msg("Trading bot has been switched OFF!", from_id)
    return send_msg("Failed to switch off trading bot!", from_id)


# define a function to switch on the trading bot and send a message to the user
def webhook_switch_on_bot(msg = 'None', from_id=TG_BOT_OWNER_ID):
    if trading_bot_switch_on(): return send_msg(f"TradingView webhook has switched ON the bot!\n\n{msg}", from_id)
    return send_msg(f"TradingView webhook failed to switch on the bot!\n\n{msg}", from_id)


# define a function to switch off the trading bot and send a message to the user
def webhook_switch_off_bot(msg = 'None', from_id=TG_BOT_OWNER_ID):
    if trading_bot_switch_off(): return send_msg(f"TradingView webhook has switched OFF the bot!\n\n{msg}", from_id)
    return send_msg(f"TradingView webhook failed to switch off the bot!\n\n{msg}", from_id)


# define a function to read the trading bot switch status from the database
def read_trading_bot_status(from_id):
    status = trading_bot_switch_status()
    if status: return send_msg("Trading bot is ON!", from_id)
    return send_msg("Trading bot is OFF (NO more buying)!", from_id)


# Set position_limit from bot import and send a message to the user
def set_position_limit_by_user(position_limit, from_id):
    if set_position_limit_default(position_limit): return send_msg(f"Position limit has been set to {get_position_limit()}!\n\nTo fully apply this new position limit, please click /reboot_the_bot", from_id)
    return send_msg("Failed to set position limit! Make sure your input format is like: /set_position_limit 5", from_id)

# define a function to take command from the user and reboot the bot, send a message to the user before rebooting
def reboot_bot(from_id):
    send_msg("Reloading the trading_bot...", from_id)
    os.system("pm2 restart ep")
    return

# define a function to take command from the user and reboot the bot, send a message to the user before rebooting
def reboot_system(from_id):
    send_msg("Rebooting the system...", from_id)
    # os.system("sudo reboot")
    os.system("pm2 restart ep")
    return

'''
{
  "update_id": 686490333,
  "message": {
    "message_id": 9976,
    "from": {
      "id": 2118900665,
      "is_bot": false,
      "first_name": "Old_Bro_Leo",
      "username": "laogege6",
      "language_code": "en",
      "is_premium": true
    },
    "chat": {
      "id": 2118900665,
      "first_name": "Old_Bro_Leo",
      "username": "laogege6",
      "type": "private"
    },
    "date": 2118900665,
    "text": "how are you today"
  }
}
'''
# Define a function to convert telegram message to df and save to 'telegram_messages' table
def insert_telegram_message_from_webhook(message):
    # print current time string format and the function is running
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} insert_telegram_message_from_webhook() is running ...')

    new_message_dict = {
        "update_id": message['update_id'],
        "message_id": message['message']['message_id'],
        "from_id": message['message']['from']['id'],
        "text": message['message'].get('text', 'None')
    }

    # Convert the message to a dataframe
    df = pd.DataFrame([new_message_dict])

    # Save the dataframe to the table 'telegram_messages'
    df.to_sql('telegram_messages', engine, if_exists='append', index=False)
    return True


# UPDATE text for a given message_id
def update_text_for_a_given_message_id(message_id, text, from_id=TG_BOT_OWNER_ID):
    try: message_id = int(message_id)
    except: return send_msg(f"Message_id has to be an integer, your input is {message_id}", from_id)

    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check if the symbol is already in the table
    try: cursor.execute(f"UPDATE telegram_messages SET text = '{text}' WHERE message_id = {message_id}")
    except Exception as e: return send_msg(f"No message_id as {message_id} in the table.\n\n{e}", from_id)

    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    return True


# Define a function to get the latest message from the table 'telegram_messages'
def get_latest_message_from_telegram_messages_table(from_id=None):
    # print current time string format and the function is running
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} get_latest_message_from_telegram_messages_table() is running ...')

    latest_message_dict = {
        "update_id": 1,
        "message_id": 1,
        "from_id": TG_BOT_OWNER_ID,
        "text": 'This is only for the initial value before the table was created'
    }

    try: df = pd.DataFrame(engine.connect().execute(text('SELECT * FROM telegram_messages ORDER BY update_id DESC LIMIT 2')).fetchall())
    except: return latest_message_dict

    # Convert the 2 row dataframe to a dictionary
    latest_message_dict = df.to_dict(orient='records')[1]
    if from_id: send_msg(f"Latest message from user:\nUpdate_id: {latest_message_dict.get('update_id')}\n\n{latest_message_dict.get('text')}", from_id)
    return latest_message_dict


# drop telegram_messages table
def drop_telegram_messages_table():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check if the symbol is already in the table
    try: cursor.execute(f"DROP TABLE telegram_messages")
    except Exception as e: return print(f"No table telegram_messages in the database.\n\n{e}")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    return True


# Define a function to create the give number of fibonacci numbers, return a list of fibonacci numbers from the first to the given number
def fibonacci(n):
    if n == 0: return [0]
    if n == 1: return [0, 1]
    if n > 1:
        fib_list = [0, 1]
        for i in range(2, n + 1):
            fib_list.append(fib_list[i - 1] + fib_list[i - 2])
        return fib_list

# define a function to respond to the from_id with a fibonacci sequence in string format for the user given number
def fibonacci_sequence(n, from_id):
    try: n = int(n)
    except: return send_msg(f"Your input has to be an integer, your input is {n}", from_id)

    if n < 0: return send_msg(f"Your input has to be a positive integer, your input is {n}", from_id)

    fib_list = fibonacci(n)
    fib_list_str = ', '.join([str(i) for i in fib_list])
    return send_msg(f"Fibonacci sequence for {n}:\n{fib_list_str}", from_id)


# define a function to calculate the IRR for a give return x-fold and a years number, return the IRR as a xx.xx% format
def calculate_irr(x, years, from_id):
    try: x = float(x)
    except: return send_msg(f"Your folds input has to be a float number, like 5.8, however your input is {x}", from_id)

    try: years = int(years)
    except: return send_msg(f"Your years input has to be an integer, however your input is {years}", from_id)

    if x <= 0: return send_msg(f"Your folds input has to be a positive number, like 5.8, however your input is {x}", from_id)
    if years <= 0: return send_msg(f"Your years input has to be a positive integer, however your input is {years}", from_id)

    irr = (x ** (1 / years) - 1) * 100

    return send_msg(f"IRR for {x} folds in {years} years is {irr:.2f}%", from_id)


if __name__ == '__main__':
    print(f"Top_functions.py is running...")


    # webhook_switch_on_bot(msg = 'None', from_id=TG_BOT_OWNER_ID)
    # time.sleep(2)
    # webhook_switch_off_bot(msg = 'None', from_id=TG_BOT_OWNER_ID)
    # print('all done')


