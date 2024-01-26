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
import yfinance as yf
import numpy as np
from bs4 import BeautifulSoup
from mplfinance.original_flavor import candlestick_ohlc
import pyotp
import smtplib
from email.mime.text import MIMEText
import imaplib
import email


# Load environment variables
load_dotenv()

# Create database engine
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',  pool_size=10, max_overflow=20)

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
DEBANK_API = os.getenv('DEBANK_API')

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

COINBASE_API_KEY = os.getenv('COINBASE_API_KEY')
COINBASE_API_SECRET = os.getenv('COINBASE_API_SECRET')

INFURA_KEY = os.getenv('INFURA_KEY')
INFURA_URL = os.getenv('INFURA_URL')
INFURA = INFURA_URL + INFURA_KEY
web3 = Web3(Web3.HTTPProvider(INFURA))
w3 = web3

# USER_TELEGRAM_LINK = os.getenv("USER_TELEGRAM_LINK")
# TELEGRAM_USERNAME = USER_TELEGRAM_LINK.split('/')[-1]

ETH_REGEX = r'0x[a-fA-F0-9]{40}'
TRX_REGEX = r'T[1-9A-HJ-NP-Za-km-z]{33}'
EMAIL_ADDRESS_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

USDT_ERC20 = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
USDT_ERC20_DECIMALS = 6

USDC_ERC20 = '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
USDC_ERC20_DECIMALS = 6

GMAIL_ADDRESS_MAIN = os.getenv('GMAIL_ADDRESS_MAIN')
GMAIL_ADDRESS = os.getenv('GMAIL_ADDRESS')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')

BINANCE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'X-MBX-APIKEY': BINANCE_API,
    "Content-Type": "application/json"
    }

# read trading parameters from table 'trading_parameters' and return a dict
def read_trading_parameters():
    with engine.connect() as connection: df_trading_parameters = pd.DataFrame(connection.execute(text("SELECT * FROM trading_parameters ORDER BY ID DESC LIMIT 1")).fetchall())
    if not df_trading_parameters.empty: return df_trading_parameters.to_dict(orient='records')[0]
    return {}

# from "CREATE TABLE IF NOT EXISTS target_profit (ID INTEGER PRIMARY KEY AUTO_INCREMENT, Date DATE, TargetProfit FLOAT)" table read the target profit
def read_target_profit_default(from_id=None):
    with engine.connect() as connection: df_target_profit = pd.DataFrame(connection.execute(text("SELECT target_profit_percentage FROM trading_parameters ORDER BY ID DESC LIMIT 1")).fetchall())
    target_profit = float(df_target_profit['target_profit_percentage'].values[0]) if not df_target_profit.empty else 0.05
    if from_id: send_msg(f"Current target profit: {target_profit*100}%", from_id)
    return target_profit


def reset_initial_funding_amount(initial_funding_fund = 100000, from_id = TG_BOT_OWNER_ID):
    try: int(initial_funding_fund)
    except: return send_msg(f"Initial funding fund has to be an integer, your input is {initial_funding_fund}", from_id)
    if set_initial_funding_fund(initial_funding_fund): return send_msg(f"Initial funding fund has been set to {initial_funding_fund} usd!", from_id)
    return send_msg("Failed to set initial funding fund! Make sure your input format is like: /set_initial_funding_fund 100000", from_id)


def reset_daily_new_positions_limit(daily_new_positions_limit = 2, from_id = TG_BOT_OWNER_ID):
    try: daily_new_positions_limit = int(daily_new_positions_limit)
    except: return send_msg(f"Daily new positions limit has to be an integer, your input is {daily_new_positions_limit}", from_id)
    return set_daily_new_positions_limit(daily_new_positions_limit)


def get_daily_new_positions_limit(from_id = TG_BOT_OWNER_ID):
    return send_msg(f"Current daily new positions limit: {read_daily_new_positions_limit()}", from_id)


# Define a function to make a dict to dataframe and create or append to a given table name
def data_to_table(data, table_name, if_exists='append'):
    if type(data) != dict: return
    df = pd.DataFrame(data, index=[0])
    if df.empty: return
    try: 
        with engine.connect() as connection: df.to_sql(table_name, connection, if_exists=if_exists, index=False)
        return True
    except Exception as e: print(f"An error occurred while calling data_to_table(): \n\n{e}\n\nTable_name: {table_name}\nData:\n\n{data}")
    return


def initial_kdj_parameter(coin, d=None, w=None, m=None, from_id=TG_BOT_OWNER_ID):
    data = {
        'coin': coin.upper(),
        'd': 1 if d else 0,
        'w': 1 if w else 0,
        'm': 1 if m else 0,
        'date_string': datetime.now().strftime("%Y-%m-%d")
    }
    if from_id: send_msg(f"Initialized KDJ parameter for {coin.upper()}: \nday: {d}, week: {w}, month: {m}\n{data.get('date_string')}", from_id)
    return data_to_table(data, 'kdj_parameter')


def reset_kdj_parameter(coin, dwm_dict = {}, from_id=None):
    try:
        with engine.connect() as connection: df = pd.DataFrame(connection.execute(text(f"SELECT * FROM kdj_parameter WHERE coin = '{coin.upper()}'")).fetchall())
    except: df = pd.DataFrame()
    if df.empty: d, w, m = 0, 0, 0
    else: d, w, m = df['d'].values[0], df['w'].values[0], df['m'].values[0]
    d = 1 if dwm_dict.get('d', None) else d
    w = 1 if dwm_dict.get('w', None) else w
    m = 1 if dwm_dict.get('m', None) else m
    date_string = datetime.now().strftime("%Y-%m-%d")
    # Update the table
    with engine.connect() as connection: connection.execute(text(f"UPDATE kdj_parameter SET d = {d}, w = {w}, m = {m}, date_string = '{date_string}' WHERE coin = '{coin.upper()}'"))
    condition = 'ON' if d and (w or m) else 'OFF'
    if from_id: send_msg(f"{coin.upper()} condition: {condition}\nLast update: {date_string}", from_id)
    return True if condition == 'ON' else False


def kdj_condition(coin, from_id=None):
    try:
        with engine.connect() as connection: df = pd.DataFrame(connection.execute(text(f"SELECT * FROM kdj_parameter WHERE coin = '{coin.upper()}'")).fetchall())
    except: df = pd.DataFrame()
    if df.empty: return send_msg(f"No kdj parameter for {coin.upper()} in the table.", from_id)
    d, w, m = df['d'].values[0], df['w'].values[0], df['m'].values[0]
    date_string = df['date_string'].values[0]
    condition = 'ON' if d and (w or m) else 'OFF'
    if from_id: send_msg(f"{coin.upper()} condition: {condition}\nLast update: {date_string}", from_id)
    return True if condition == 'ON' else False


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

def hash_md5_bot(content, from_id=TG_BOT_OWNER_ID):
    print(f"CALLING hash_md5_bot() for {content}")
    hashed_content = hashlib.md5(str(content).encode('utf-8')).hexdigest()
    if from_id: send_msg(f"Original Content: \n{content}\n\nMD5 Hashed: \n{hashed_content}", from_id)
    return hashed_content

def hash_sha256_bot(content, from_id=TG_BOT_OWNER_ID):
    print(f"CALLING hash_sha256_bot() for {content}")
    hashed_content = hashlib.sha256(str(content).encode('utf-8')).hexdigest()
    if from_id: send_msg(f"Original Content: \n{content}\n\nSHA256 Hashed: \n{hashed_content}", from_id)
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

def get_initial_funding_amount(from_id = TG_BOT_OWNER_ID):
    initial_funding_fund = read_initial_funding_fund()
    if from_id: send_msg(f"Current initial funding fund: {format_number(initial_funding_fund)} usd", from_id)
    return initial_funding_fund

def send_email(subject, message, to_addr):

    # Create MIMEText object
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = GMAIL_ADDRESS
    msg['To'] = to_addr

    # Connect to Gmail's SMTP server and send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()  # Start TLS encryption
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, to_addr, msg.as_string())

def send_to_gmail_main(message, subject = 'From Python Bot'):
    send_email(subject, message, GMAIL_ADDRESS_MAIN)
    send_msg(f"Message sent to {GMAIL_ADDRESS_MAIN} successfully.")
    return

# 从 Coinmarketcap 给定 token 的价格等数据, 返回一个字典
def get_token_info_from_coinmarketcap(token_symbol):
    # print(f"CALLING get_token_info_from_coinmarketcap() for {token_symbol}")
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


def get_token_info(coin: str, from_id=TG_BOT_OWNER_ID):
    # print current time string format and the function is running
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} get_token_info() is running ...')

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
        'Turnover_Ratio': 'N/A',
        '24H_Fluctuation': f"{token_info['quote']['USD']['percent_change_24h']:.2f}%",
        'Current_Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ail': f"/ignore_{coin.upper()}",
        'awl': f"/white_{coin.upper()}",
        'ahl': f"/hold_{coin.upper()}",
    }
    try: output_dict['Turnover_Ratio'] = round(float(token_info['quote']['USD']['volume_24h']) / float(token_info['quote']['USD']['market_cap']), 2)
    except: pass
    # 用 '\n' join k: v
    output_dict_str = '\n'.join([f"{k}: {v}" for k, v in output_dict.items()])

    if from_id: send_msg(output_dict_str, from_id)

    return True


# get token price info from coinmarketcap
def get_token_price_info(coin: str):
    # print current time string format and the function is running
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} get_token_info() is running ...')

    token_info = get_token_info_from_coinmarketcap(coin.upper())
    if not token_info: return 

    current_price = token_info['quote']['USD']['price']
    current_price = float(current_price)
    return current_price


# Calculate the valuation of a give coin for a given amount
def calculate_coin_valuation(coin, amount = 146652243, from_id=TG_BOT_OWNER_ID):
    try: amount = float(amount)
    except: return send_msg(f"Amount has to be a number, your input is {amount}", from_id)
    current_price = get_token_price_info(coin.upper())
    if not current_price: return 0
    valuation = current_price * amount
    if from_id: send_msg(f"{amount} {coin.upper()} = {format_number(valuation)} usd", from_id)
    return valuation


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
def send_msg(message, chat_id=None):
    # print(f"Sending message to chat_id: {chat_id}")

    if not chat_id: print(f"No chat_id, just print the message:\n\n{message}\n\n")

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

# Define a function to delete a given message_id from a given chat_id
def delete_msg(chat_id, message_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/deleteMessage"

    payload = {
        "chat_id": chat_id,
        "message_id": message_id
    }
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    try: requests.post(url, json=payload, headers=headers)
    except Exception as e: return print(f"ERROR: delete_msg() failed for:\n{e}\n\n")

    return True


# TELEGRAM BROADCAST BOT
TG_BROADCAST_BOT_TOKEN= os.getenv('TG_BROADCAST_BOT_TOKEN')
TG_BROADCAST_BOT_BASE_URL = f"https://api.telegram.org/bot{TG_BROADCAST_BOT_TOKEN}/"
TG_BROADCAST_BOT_HANDLER = os.getenv('TG_BROADCAST_BOT_HANDLER')

# TELEGRAM CHANNEL
TG_BROADCAST_CHANNEL_CHAT_ID = int(os.getenv('TG_BROADCAST_CHANNEL_CHAT_ID'))
TG_BROADCAST_CHANNEL_TITLE = os.getenv('TG_BROADCAST_CHANNEL_TITLE')
TG_BROADCAST_CHANNEL_USERNAME = os.getenv('TG_BROADCAST_CHANNEL_USERNAME')
TG_BROADCAST_CHANNEL_LINK = os.getenv('TG_BROADCAST_CHANNEL_LINK')

# define a function to use TG_BROADCAST_BOT_BASE_URL send broadcast message to the TG_BROADCAST_CHANNEL_CHAT_ID
def broadcast_markdown(message):
    url = f"https://api.telegram.org/bot{TG_BROADCAST_BOT_TOKEN}/sendMessage"

    payload = {
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
        "disable_notification": True,
        "chat_id": TG_BROADCAST_CHANNEL_CHAT_ID
    }
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    try: requests.post(url, json=payload, headers=headers)
    except Exception as e: return print(f"ERROR: send_broadcast_msg_markdown() failed for:\n{e}\n\nOriginal message:\n{message}")

    return True

def broadcast_text(message):
    url = TG_BROADCAST_BOT_BASE_URL + "sendMessage"

    payload = {
        "text": message,
        "disable_web_page_preview": True,
        "disable_notification": True,
        "chat_id": TG_BROADCAST_CHANNEL_CHAT_ID
    }
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    try: requests.post(url, json=payload, headers=headers)
    except Exception as e: return print(f"ERROR: send_broadcast_msg_markdown() failed for:\n{e}\n\nOriginal message:\n{message}")

    return True


# Define a test function to test send_msg_markedown(), send a text with markdown format, a URL with a link to the owner
def test_send_msg_markdown():
    USER_TELEGRAM_LINK = 'https://leowang.net'
    message = f"Hello, this is a test message with markdown format, [click here]({USER_TELEGRAM_LINK}) to contact the owner."
    return broadcast_text(message)
    

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
def get_all_expenditure_records(from_id = TG_BOT_OWNER_ID):
    query = f"SELECT * FROM user_expenditures_record WHERE From_id = '{str(from_id)}'"
    with engine.connect() as connection: df = pd.DataFrame(connection.execute(text(query)).fetchall())
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

    with engine.connect() as connection: df = pd.DataFrame(connection.execute(text(query)).fetchall())

    print(df)

    # Calculate the sum of the spent column
    total_spend = df['Spent'].sum()
    send_msg(f"Total spent of year {year} and month {month} for category {category_correct} and merchant {merchant_correct} is {format_number(total_spend)} usd", from_id)
    return True


# define a function to switch on the trading bot and send a message to the user
def  switch_on_bot(from_id):
    if trading_bot_switch_on(): return send_msg(f"Trading bot has been switched ON!", from_id)
    return send_msg("Failed to switch on trading bot!", from_id)

# define a function to switch off the trading bot and send a message to the user
def switch_off_bot(from_id):
    if trading_bot_switch_off(): return send_msg("Trading bot has been switched OFF!", from_id)
    return send_msg("Failed to switch off trading bot!", from_id)


# define a function to read the trading bot switch status from the database
def read_trading_bot_status(from_id=TG_BOT_OWNER_ID):
    status = trading_bot_switch_status()
    if status: return send_msg("Trading bot is ON! (Ignorelist active)", from_id)
    return send_msg("Trading bot is OFF (Whitelist only)!", from_id)


# Set position_limit from bot import and send a message to the user
def set_position_limit_by_user(position_limit, from_id):
    try: position_limit = int(position_limit)
    except: return send_msg(f"Position limit has to be an integer, your input is {position_limit}", from_id)
    if set_position_limit_default(position_limit): return send_msg(f"Position limit has been set to {get_position_limit()}!", from_id)
    return send_msg("Failed to set position limit! Make sure your input format is like: /set_position_limit 5", from_id)


# define a function to take command from the user and reboot the bot, send a message to the user before rebooting
def reboot_bot(from_id):
    send_msg("Reloading the trading_bot...", from_id)
    os.system("sudo systemctl restart gunicorn")
    return


# define a function to take command from the user and reboot the bot, send a message to the user before rebooting
def reboot_system(from_id):
    send_msg("Rebooting the system...", from_id)
    # os.system("sudo reboot")
    os.system("sudo systemctl restart gunicorn")
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
    with engine.connect() as connection: df.to_sql('telegram_messages', connection, if_exists='append', index=False)
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
    except: pass

    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    return True

# Check if a given from_id is in telegram_messages table
def check_if_from_id_in_telegram_messages_table(from_id):
    try: from_id = int(from_id)
    except: return False

    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check if the symbol is already in the table
    cursor.execute(f"SELECT * FROM telegram_messages WHERE from_id = {from_id}")
    result = cursor.fetchall()
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    if len(result) == 0: return False
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

    try: 
        with engine.connect() as connection: df = pd.DataFrame(connection.execute(text('SELECT * FROM telegram_messages ORDER BY update_id DESC LIMIT 2')).fetchall())
    except: return latest_message_dict

    # Convert the 2 row dataframe to a dictionary
    latest_message_dict = df.to_dict(orient='records')[1]
    if from_id: send_msg(f"Latest message from user:\nUpdate_id: {latest_message_dict.get('update_id')}\n\n{latest_message_dict.get('text')}", from_id)
    
    latest_message_dict = df.to_dict(orient='records')[0]
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


# Define a function to connect to the remote database and return the connection
def get_remote_db_connection():
    # Define the database connection parameters
    db_host = os.getenv('UBUNTU_SERVER_JP_DB_HOST')
    db_port = os.getenv('UBUNTU_SERVER_JP_DB_PORT')
    db_user = os.getenv('UBUNTU_SERVER_JP_DB_USER')
    db_password = os.getenv('UBUNTU_SERVER_JP_DB_PASSWORD')
    db_name = os.getenv('UBUNTU_SERVER_JP_DB_NAME')

    # Create the connection
    remote_engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    return remote_engine


def get_stock_info(symbol = None, from_id = None):
    if not symbol: return

    symbol = symbol.upper()

    # Fetch data for the given symbol
    stock = yf.Ticker(symbol)
    
    # Get stock info
    info = stock.info
    ''' info
    {'address1': 'One Apple Park Way', 'city': 'Cupertino', 'state': 'CA', 'zip': '95014', 'country': 'United States', 'phone': '408 996 1010', 'website': 'https://www.apple.com', 'industry': 'Consumer Electronics', 'industryKey': 'consumer-electronics', 'industryDisp': 'Consumer Electronics', 'sector': 'Technology', 'sectorKey': 'technology', 'sectorDisp': 'Technology', 'longBusinessSummary': 'Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. The company offers iPhone, a line of smartphones; Mac, a line of personal computers; iPad, a line of multi-purpose tablets; and wearables, home, and accessories comprising AirPods, Apple TV, Apple Watch, Beats products, and HomePod. It also provides AppleCare support and cloud services; and operates various platforms, including the App Store that allow customers to discover and download applications and digital content, such as books, music, video, games, and podcasts. In addition, the company offers various services, such as Apple Arcade, a game subscription service; Apple Fitness+, a personalized fitness service; Apple Music, which offers users a curated listening experience with on-demand radio stations; Apple News+, a subscription news and magazine service; Apple TV+, which offers exclusive original content; Apple Card, a co-branded credit card; and Apple Pay, a cashless payment service, as well as licenses its intellectual property. The company serves consumers, and small and mid-sized businesses; and the education, enterprise, and government markets. It distributes third-party applications for its products through the App Store. The company also sells its products through its retail and online stores, and direct sales force; and third-party cellular network carriers, wholesalers, retailers, and resellers. Apple Inc. was founded in 1976 and is headquartered in Cupertino, California.', 'fullTimeEmployees': 161000, 'companyOfficers': [{'maxAge': 1, 'name': 'Mr. Timothy D. Cook', 'age': 61, 'title': 'CEO & Director', 'yearBorn': 1961, 'fiscalYear': 2022, 'totalPay': 16425933, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Luca  Maestri', 'age': 59, 'title': 'CFO & Senior VP', 'yearBorn': 1963, 'fiscalYear': 2022, 'totalPay': 5019783, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Jeffrey E. Williams', 'age': 58, 'title': 'Chief Operating Officer', 'yearBorn': 1964, 'fiscalYear': 2022, 'totalPay': 5018337, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Ms. Katherine L. Adams', 'age': 58, 'title': 'Senior VP, General Counsel & Secretary', 'yearBorn': 1964, 'fiscalYear': 2022, 'totalPay': 5015208, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': "Ms. Deirdre  O'Brien", 'age': 55, 'title': 'Senior Vice President of Retail', 'yearBorn': 1967, 'fiscalYear': 2022, 'totalPay': 5019783, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Chris  Kondo', 'title': 'Senior Director of Corporate Accounting', 'fiscalYear': 2022, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. James  Wilson', 'title': 'Chief Technology Officer', 'fiscalYear': 2022, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Ms. Mary  Demby', 'title': 'Chief Information Officer', 'fiscalYear': 2022, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Suhasini  Chandramouli', 'title': 'Director of Investor Relations', 'fiscalYear': 2022, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Greg  Joswiak', 'title': 'Senior Vice President of Worldwide Marketing', 'fiscalYear': 2022, 'exercisedValue': 0, 'unexercisedValue': 0}], 'auditRisk': 4, 'boardRisk': 1, 'compensationRisk': 6, 'shareHolderRightsRisk': 1, 'overallRisk': 1, 'governanceEpochDate': 1701388800, 'compensationAsOfEpochDate': 1672444800, 'maxAge': 86400, 'priceHint': 2, 'previousClose': 198.11, 'open': 197.53, 'dayLow': 197.02, 'dayHigh': 198.3999, 'regularMarketPreviousClose': 198.11, 'regularMarketOpen': 197.53, 'regularMarketDayLow': 197.02, 'regularMarketDayHigh': 198.3999, 'dividendRate': 0.96, 'dividendYield': 0.0047999998, 'exDividendDate': 1699574400, 'payoutRatio': 0.1533, 'fiveYearAvgDividendYield': 0.82, 'beta': 1.308, 'trailingPE': 32.28268, 'forwardPE': 27.632168, 'volume': 114815314, 'regularMarketVolume': 114815314, 'averageVolume': 54029619, 'averageVolume10days': 54847430, 'averageDailyVolume10Day': 54847430, 'bid': 197.42, 'ask': 197.46, 'bidSize': 1000, 'askSize': 800, 'marketCap': 3072766771200, 'fiftyTwoWeekLow': 124.17, 'fiftyTwoWeekHigh': 199.62, 'priceToSalesTrailing12Months': 8.016924, 'fiftyDayAverage': 183.3344, 'twoHundredDayAverage': 177.3107, 'trailingAnnualDividendRate': 0.94, 'trailingAnnualDividendYield': 0.004744839, 'currency': 'USD', 'enterpriseValue': 3143530708992, 'profitMargins': 0.25305998, 'floatShares': 15535488445, 'sharesOutstanding': 15552799744, 'sharesShort': 110653413, 'sharesShortPriorMonth': 98190963, 'sharesShortPreviousMonthDate': 1698710400, 'dateShortInterest': 1701302400, 'sharesPercentSharesOut': 0.0070999996, 'heldPercentInsiders': 0.00074, 'heldPercentInstitutions': 0.61662996, 'shortRatio': 2.13, 'shortPercentOfFloat': 0.0070999996, 'impliedSharesOutstanding': 15552799744, 'bookValue': 3.997, 'priceToBook': 49.429573, 'lastFiscalYearEnd': 1696032000, 'nextFiscalYearEnd': 1727654400, 'mostRecentQuarter': 1696032000, 'earningsQuarterlyGrowth': 0.108, 'netIncomeToCommon': 96995000320, 'trailingEps': 6.12, 'forwardEps': 7.15, 'pegRatio': 4.91, 'lastSplitFactor': '4:1', 'lastSplitDate': 1598832000, 'enterpriseToRevenue': 8.202, 'enterpriseToEbitda': 24.984, '52WeekChange': 0.47282732, 'SandP52WeekChange': 0.22510612, 'lastDividendValue': 0.24, 'lastDividendDate': 1699574400, 'exchange': 'NMS', 'quoteType': 'EQUITY', 'symbol': 'AAPL', 'underlyingSymbol': 'AAPL', 'shortName': 'Apple Inc.', 'longName': 'Apple Inc.', 'firstTradeDateEpochUtc': 345479400, 'timeZoneFullName': 'America/New_York', 'timeZoneShortName': 'EST', 'uuid': '8b10e4ae-9eeb-3684-921a-9ab27e4d87aa', 'messageBoardId': 'finmb_24937', 'gmtOffSetMilliseconds': -18000000, 'currentPrice': 197.57, 'targetHighPrice': 250.0, 'targetLowPrice': 159.0, 'targetMeanPrice': 198.52, 'targetMedianPrice': 200.0, 'recommendationMean': 2.1, 'recommendationKey': 'buy', 'numberOfAnalystOpinions': 39, 'totalCash': 61554999296, 'totalCashPerShare': 3.958, 'ebitda': 125820002304, 'totalDebt': 123930001408, 'quickRatio': 0.843, 'currentRatio': 0.988, 'totalRevenue': 383285002240, 'debtToEquity': 199.418, 'revenuePerShare': 24.344, 'returnOnAssets': 0.20256001, 'returnOnEquity': 1.7195, 'grossProfits': 170782000000, 'freeCashflow': 82179997696, 'operatingCashflow': 110543003648, 'earningsGrowth': 0.135, 'revenueGrowth': -0.007, 'grossMargins': 0.44131002, 'ebitdaMargins': 0.32827, 'operatingMargins': 0.30134, 'financialCurrency': 'USD', 'trailingPegRatio': 2.3747}'''

    # Extract the key information from the info dictionary and make a dictionary
    info = {
        'Symbol': info['symbol'],
        'Price': f"{format_number(info['currentPrice'])} {info['currency']}",
        'Market Cap': format_number(info['marketCap']),
        'Volume': format_number(info['volume']),
        'Sector': info['sector'],
        'Industry': info['industry'],
        'Full Name': info['longName'],
        'Current Time': datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    # make a string of the info dictionary
    info_str = '\n'.join([f"{k}: {v}" for k, v in info.items()])
    if from_id: return send_msg(info_str, from_id)
    else: return info_str


# check eth balance of a given address and convert the balance from wei to eth
def check_eth_balance(address):
    # get the balance of the address
    balance = w3.eth.get_balance(address)
    # convert the balance from wei to eth
    return balance / 10**18


# check erc20 token balance of a given address and convert the balance from wei to token
def check_address_token_balance(address, token_address, chain='eth'):
    base_url = "https://pro-openapi.debank.com"

    headers = {"AccessKey": DEBANK_API, "content-type": "application/json"}

    method = "GET"
    path = "/v1/user/token"
    _params = {
        "id": address,
        'token_id': token_address,
        'chain_id': chain
        }
    params = urlencode(_params)
    URL = base_url + path + "?" + params
    r = requests.request(method, URL, headers=headers)

    return 0 if r.status_code != 200 else r.json().get('amount', 0)


def check_address_balance(address):
    # convert the balance from wei to eth
    eth_balance = check_eth_balance(address)

    # get the USDT balance of the address
    usdt_balance = check_address_token_balance(address, USDT_ERC20, chain='eth')

    # get the USDC balance of the address
    usdc_balance = check_address_token_balance(address, USDC_ERC20, chain='eth')

    return {'ETH': eth_balance, 'USDT': usdt_balance, 'USDC': usdc_balance}


def check_address_balance_return_str(address, from_id=TG_BOT_OWNER_ID):
    # convert address to checksum address
    try: address = w3.to_checksum_address(address)
    except: return send_msg(f"Your address {address} is not a valid address!", from_id)

    balance_dic = check_address_balance(address)
    balance_str = '\n'.join([f"{k}: {format_number(v)}" for k, v in balance_dic.items()])
    return send_msg(balance_str, from_id)


'''CREATE TABLE IF NOT EXISTS trivial_records (ID INTEGER PRIMARY KEY AUTO_INCREMENT, Info TEXT)'''
# Define a function to insert a new record into the table 'trivial_records'
def save_trivial_record(info, from_id=TG_BOT_OWNER_ID):

    # make sure info is text
    info = str(info)

    # append current into the info
    info = f"{info}\n\n{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

    # Assuming engine is already created as shown in previous examples
    with engine.connect() as connection:
        try:
            # Define your SQL query using SQLAlchemy's text function
            sql = text("""
                INSERT INTO trivial_records (Info) VALUES (:info)
            """)

            # Execute the query with the provided parameters
            result = connection.execute(sql, {'info': info})

            # Commit the transaction
            connection.commit()

            # Read the ID of the last inserted row
            last_row_id = result.lastrowid

            send_msg(f"Successfully inserted: \n\nID: {last_row_id}\nInfo: {info}", from_id)

        except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()

    return


# Define a function to search a key word from the table 'trivial_records', get all of the like results and get a list, then join the list to a string and send to the user
def search_trivial_records(key_word, from_id=TG_BOT_OWNER_ID):
    # Assuming engine is already created as shown in previous examples
    with engine.connect() as connection:
        try:
            # Define your SQL query using SQLAlchemy's text function
            sql = text(f"""
                SELECT * FROM trivial_records WHERE Info LIKE '%{key_word}%'
            """)

            # Execute the query with the provided parameters
            result = connection.execute(sql)

            # Commit the transaction
            connection.commit()

            # Read the ID of the last inserted row
            result_list = result.fetchall()

            # if no result, return
            if not result_list: return send_msg(f"No result for: {key_word}", from_id)

            # convert the result list to a string
            result_str = '\n\n'.join([f"ID: {i[0]}\nInfo: {i[1]}" for i in result_list])

            send_msg(f"Search result for {key_word}:\n\n{result_str}", from_id)

        except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()

    return


def get_binance_coin_list():
    
    df_ticker = pd.read_json(BINANCE_TICKER_URL)

    # pick up the symbol endswith 'USDT'
    df_ticker = df_ticker[df_ticker['symbol'].str.endswith('USDT')]

    df_ticker['coin'] = df_ticker['symbol'].str[:-4]


    # Eliminate the coins with 'USD' in coin name
    df_ticker = df_ticker[~df_ticker['coin'].str.contains('USD')]

    print(df_ticker)

    # make a list
    binance_coin_list = df_ticker['coin'].values.tolist()

    return binance_coin_list


def fetch_text_from_url(url):
    try:
        # Send a request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract and return the text
            return soup.get_text()
        else:
            return f"Error: Unable to access URL (Status Code: {response.status_code})"
    except Exception as e: print(f"An error occurred: {e}")
    return

def calculate_passcode(passcode_key):
    # Convert passcode_key into a base32 format as required by the TOTP standard
    key = base64.b32encode(passcode_key.encode()).decode()

    # Define the time period for OTP. This is typically 30 seconds.
    interval = 30

    # Calculate the number of intervals that have passed since the Unix epoch
    time_counter = int(time.time() / interval)

    # Convert the time counter to byte format
    counter_bytes = time_counter.to_bytes(8, 'big')

    # Decode the key from Base32
    key_bytes = base64.b32decode(key, casefold=True)

    # Create an HMAC-SHA1 hash from the key and counter
    hmac_hash = hmac.new(key_bytes, counter_bytes, hashlib.sha1).digest()

    # Use a dynamic truncation to get a 4-byte string
    offset = hmac_hash[-1] & 0x0F
    truncated_hash = hmac_hash[offset:offset+4]

    # Convert the truncated hash to an integer
    code = int.from_bytes(truncated_hash, 'big')

    # Extract a 6-digit number from the code
    passcode = code % 1000000

    return passcode


'''CREATE TABLE IF NOT EXISTS one_time_passcode (ID INTEGER PRIMARY KEY AUTO_INCREMENT, AppName VARCHAR(255), Passcode_Key VARCHAR(255), Date DATE)'''
# define a function instert user input app_name and passcode_key into one_time_passcode table
def insert_otp(app_name, passcode_key, from_id=TG_BOT_OWNER_ID):
    r = insert_one_time_passcode(app_name, passcode_key)
    if r: passcode = get_otp(app_name, from_id)
    else: send_msg(f"Failed to insert passcode_key for {app_name}", from_id)
    return passcode


'''get_one_time_passcode(app_name)'''
# define a function to get the passcode_key for a given app_name and calculate the passcode digit
def get_otp(app_name, from_id=TG_BOT_OWNER_ID):
    passcode_key = get_one_time_passcode(app_name)
    if not passcode_key: return send_msg(f"App Name {app_name} not found!", from_id)
    totp = pyotp.TOTP(passcode_key)
    passcode = totp.now()
    send_msg(f"Passcode for {app_name} is \n\n{passcode}", from_id)
    return passcode


# Read umfuture_orders_profit and get the sum of profit
def get_umfuture_profit(from_id=None, coin=None):
    profit = 0
    try:
        if not coin: 
            with engine.connect() as connection: df = pd.DataFrame(connection.execute(text('SELECT SUM(profit) FROM umfuture_orders_profit')).fetchall())
        else: 
            with engine.connect() as connection: df = pd.DataFrame(connection.execute(text('SELECT SUM(profit) FROM umfuture_orders_profit WHERE coin = :coin'), {'coin': coin}).fetchall())
        if not df.empty:
            profit = df[0][0]
            profit = format_number(profit)
    except: pass

    if not coin: send_msg(f"UMFUTURE Total profit is {profit}", from_id)
    else: send_msg(f"UMFUTURE Total profit for {coin} is {profit}", from_id)

    return profit


def get_df_from_given_tablename(tablename):
    try: 
        with engine.connect() as connection: df = pd.DataFrame(connection.execute(text(f'SELECT * FROM {tablename}')).fetchall())
    except: df = pd.DataFrame()
    return df


def get_filtered_df(tablename, columns:list = None, filters: dict = None):
    query = f"SELECT "
    if columns and type(columns) is list: query += ", ".join(columns)
    else: query += "*"
    query += f" FROM {tablename}"
    if filters and type(filters) is dict: query += " WHERE " + " AND ".join([f"{k} = :{k}" for k in filters])
    try: 
        with engine.connect() as connection: reply_df = pd.DataFrame(connection.execute(text(query), filters).fetchall())
        return reply_df
    except: return pd.DataFrame()
    

def get_trading_pairs_from_coinbase():
    print("CALLING get_trading_pairs_from_coinbase()")
    # Coinbase Pro API endpoint for trading pairs
    url = 'https://api.pro.coinbase.com/products'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        trading_pairs = []
        for pair in data:
            trading_pairs.append(pair['id'])

        return trading_pairs
    except requests.exceptions.RequestException as e:
        print(f"Error while fetching trading pairs: {e}")
        return []
    

# make trading_pairs = get_trading_pairs_from_coinbase() a list with only the coin name
def get_coin_list_from_trading_pairs():
    trading_pairs = get_trading_pairs_from_coinbase()
    coin_list = []
    for pair in trading_pairs:
        # keep only the USDT pair
        if pair.endswith('-USDT'): coin_list.append(pair.split('-')[0])
    coin_list = list(set(coin_list))
    # Save to table
    with engine.connect() as connection: pd.DataFrame(coin_list).to_sql('coinbase_coin_list', connection, if_exists='replace', index=False)
    return coin_list


# Read coinbase_coin_list and get the coin list
def read_coinbase_coin_list():
    coin_list = []
    try:
        with engine.connect() as connection: df = pd.DataFrame(connection.execute(text('SELECT * FROM coinbase_coin_list')).fetchall())
        if not df.empty: 
            coin_list = df.iloc[:, 0].values.tolist()
            coin_list = list(set(coin_list))
    except: pass
    return coin_list


def get_symbol_list_from_trading_pairs():
    trading_pairs = get_trading_pairs_from_coinbase()
    symbol_list = []
    for pair in trading_pairs:
        # keep only the USDT pair
        if pair.endswith('-USDT'): symbol_list.append(pair)
    return symbol_list


# NOT SUCCESSFUL
def coinbase_market_buy_order(product_id, funds = '10000'):
    """
    Place a market buy order on Coinbase Pro.

    :param api_url: URL of the Coinbase Pro API.
    :param api_key: Your Coinbase Pro API key.
    :param secret_key: Your Coinbase Pro API secret key.
    :param passphrase: Your Coinbase Pro API passphrase.
    :param product_id: The product to buy (e.g., 'BTC-USD').
    :param funds: The amount of funds (in quote currency) to use for the purchase.
    """

    api_url = 'https://api.pro.coinbase.com'
    api_key = os.getenv('COINBASE_API_KEY')
    secret_key = os.getenv('COINBASE_API_SECRET')
    passphrase = os.getenv('COINBASE_API_PASSPHRASE')

    if product_id not in COINBASE_SYMBOL_LIST: 
        coinbase_product_id_list = get_symbol_list_from_trading_pairs()
        if product_id not in coinbase_product_id_list: return f"Product_id {product_id} not in COINBASE_SYMBOL_LIST"

    timestamp = str(time.time())
    method = 'POST'
    path = '/orders'
    body = json.dumps({
        'type': 'market',
        'side': 'buy',
        'product_id': product_id,
        'funds': str(funds)
    })

    # Create a signature
    message = timestamp + method + path + body
    hmac_key = base64.b64decode(secret_key)
    signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
    signature_b64 = base64.b64encode(signature.digest())

    # Define the request headers
    headers = {
        'Content-Type': 'application/json',
        'CB-ACCESS-KEY': api_key,
        'CB-ACCESS-SIGN': signature_b64,
        'CB-ACCESS-TIMESTAMP': timestamp,
        'CB-ACCESS-PASSPHRASE': passphrase
    }

    # Send the request
    response = requests.post(api_url + path, headers=headers, data=body)
    
    if response.status_code == 200: return response.json()
    else: return response.json()  # Contains the error message


if __name__ == '__main__':
    print(f"Top_functions.py is running...")
    reset_bot_starting_date(bot_starting_date = '2023-12-10')
    initial_kdj_parameter('BTC', d=1, w=0, m=1)
