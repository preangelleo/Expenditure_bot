import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from Prompt_template import *

# Load environment variables
load_dotenv()

# Database connection parameters
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')


# Define a function to CREATE DATABASE IF NOT EXISTS db_name: expenditure_records
def create_database():
    try:
        # Connect to the MySQL Server (without specifying a database)
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            port=db_port
        )

        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            cursor.close()
            conn.close()

    except Error as e: print(f"Error connecting to MySQL: {e}")

    finally:
        if conn.is_connected():
            conn.close()
            print("MySQL connection is closed")

# Database connection function
def get_db_connection():
    conn = mysql.connector.connect(host=db_host, port=db_port, user=db_user, password=db_password, database=db_name)
    return conn

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
    print("Table 'user_expenditures_record' created successfully!")
    return True


'''binance_position_buy | CREATE TABLE `binance_position_buy` (
  `symbol` text,
  `orderId` bigint DEFAULT NULL,
  `orderListId` bigint DEFAULT NULL,
  `clientOrderId` text,
  `transactTime` bigint DEFAULT NULL,
  `price` double DEFAULT NULL,
  `origQty` text,
  `executedQty` text,
  `cummulativeQuoteQty` text,
  `status` text,
  `timeInForce` text,
  `type` text,
  `side` text,
  `workingTime` bigint DEFAULT NULL,
  `selfTradePreventionMode` text,
  `coin` text,
  `buy_cost_bnb` double DEFAULT NULL,
  `buy_bnb_price` double DEFAULT NULL,
  `update_id` bigint DEFAULT NULL,
  `is_closed` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci |
'''
# def create_binance_position_buy_table():
#     # Create a new session
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     # Create a new table 'binance_position_buy'
#     cursor.execute("CREATE TABLE IF NOT EXISTS binance_position_buy (symbol TEXT, orderId BIGINT, orderListId BIGINT, clientOrderId TEXT, transactTime BIGINT, price DOUBLE, origQty TEXT, executedQty TEXT, cummulativeQuoteQty TEXT, status TEXT, timeInForce TEXT, type TEXT, side TEXT, workingTime BIGINT, selfTradePreventionMode TEXT, coin TEXT, buy_cost_bnb DOUBLE, buy_bnb_price DOUBLE, update_id BIGINT, is_closed BIGINT)")
#     # Commit the session
#     conn.commit()
#     cursor.close()
#     conn.close()
#     print("Table 'binance_position_buy' created successfully!")
#     return True


'''binance_position_sell | CREATE TABLE `binance_position_sell` (
  `symbol` text,
  `orderId` bigint DEFAULT NULL,
  `orderListId` bigint DEFAULT NULL,
  `clientOrderId` text,
  `transactTime` bigint DEFAULT NULL,
  `price` double DEFAULT NULL,
  `origQty` text,
  `executedQty` text,
  `cummulativeQuoteQty` text,
  `status` text,
  `timeInForce` text,
  `type` text,
  `side` text,
  `workingTime` bigint DEFAULT NULL,
  `selfTradePreventionMode` text,
  `update_id` bigint DEFAULT NULL,
  `sell_cost_bnb` double DEFAULT NULL,
  `sell_bnb_price` double DEFAULT NULL,
  `total_bnb_cost_value` double DEFAULT NULL,
  `profit` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci |
'''
# def create_binance_position_sell_table():
#     # Create a new session
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     # Create a new table 'binance_position_sell'
#     cursor.execute("CREATE TABLE IF NOT EXISTS binance_position_sell (symbol TEXT, orderId BIGINT, orderListId BIGINT, clientOrderId TEXT, transactTime BIGINT, price DOUBLE, origQty TEXT, executedQty TEXT, cummulativeQuoteQty TEXT, status TEXT, timeInForce TEXT, type TEXT, side TEXT, workingTime BIGINT, selfTradePreventionMode TEXT, update_id BIGINT, sell_cost_bnb DOUBLE, sell_bnb_price DOUBLE, total_bnb_cost_value DOUBLE, profit DOUBLE)")
#     # Commit the session
#     conn.commit()
#     cursor.close()
#     conn.close()
#     print("Table 'binance_position_sell' created successfully!")
#     return True


'''ignore_coin_list | CREATE TABLE `ignore_coin_list` (
  `id` int NOT NULL AUTO_INCREMENT,
  `symbol` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=221 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci |
'''
def create_ignore_coin_list_table():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create a new table 'ignore_coin_list'
    cursor.execute("CREATE TABLE IF NOT EXISTS ignore_coin_list (id INT NOT NULL AUTO_INCREMENT, symbol VARCHAR(20) DEFAULT NULL, PRIMARY KEY (id))")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print("Table 'ignore_coin_list' created successfully!")
    return True


def insert_initial_ignore_list():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Insert initial ignore list
    for symbol in INITIAL_IGNORE_LIST: cursor.execute(f"INSERT INTO ignore_coin_list (symbol) VALUES ('{symbol}')")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print("Initial ignore list inserted successfully!")
    return True



if __name__ == '__main__':
    print("Create database and tables...")
    # Initial Step 1: Create database
    create_database()

    # Initial Step 2: Create user_expenditures_record tables
    create_expenditure_record_table()

    # Initial Step 3: Create ignore_coin_list tables
    create_ignore_coin_list_table()

    # Initial Step 4: Insert initial ignore list
    insert_initial_ignore_list()

