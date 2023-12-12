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
    for symbol in INITIAL_IGNORE_LIST: 
        # Check if the symbol is already in the table
        cursor.execute(f"SELECT * FROM ignore_coin_list WHERE symbol = '{symbol}'")
        result = cursor.fetchall()
        if len(result) == 0: cursor.execute(f"INSERT INTO ignore_coin_list (symbol) VALUES ('{symbol}')")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print("Initial ignore list inserted successfully!")
    return True


# Create a table 'net_profit_daily_record' to record the net profit, net profit sum of each day
def create_net_profit_daily_record_table():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create a new table 'net_profit_daily_record'
    cursor.execute("CREATE TABLE IF NOT EXISTS net_profit_daily_record (ID INTEGER PRIMARY KEY AUTO_INCREMENT, Date DATE, NetProfit FLOAT)")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print("Table 'net_profit_daily_record' created successfully!")
    return True

# Create a table 'target_profit' to set the target profit, overwirte the .env figure
def create_target_profit_table():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create a new table 'target_profit'
    cursor.execute("CREATE TABLE IF NOT EXISTS target_profit (ID INTEGER PRIMARY KEY AUTO_INCREMENT, Date DATE, TargetProfit FLOAT)")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print("Table 'target_profit' created successfully!")
    return True


# insert TARGET_PROFIT = float(os.getenv('TARGET_PROFIT', 0.05)) into table 'target_profit'
def set_target_profit_default(target_profit = float(os.getenv('TARGET_PROFIT', 0.05))):
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Insert TARGET_PROFIT = float(os.getenv('TARGET_PROFIT', 0.05)) into table 'target_profit'
    cursor.execute(f"INSERT INTO target_profit (Date, TargetProfit) VALUES (CURDATE(), {target_profit})")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print(f"TARGET_PROFIT = {target_profit} inserted successfully!")
    return True

# Creat a table 'position_limit' to set the position limit, integer
def create_position_limit_table():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create a new table 'position_limit'
    cursor.execute("CREATE TABLE IF NOT EXISTS position_limit (ID INTEGER PRIMARY KEY AUTO_INCREMENT, Date DATE, PositionLimit INTEGER)")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print("Table 'position_limit' created successfully!")
    return True

'''
INITIAL_FUND = int(os.getenv('INITIAL_FUND', 100_000))
CHECK_SIZE = int(os.getenv('CHECK_SIZE', 10_000))
POSITIONS_LIMIT = int(INITIAL_FUND / CHECK_SIZE)
'''
# insert POSITIONS_LIMIT = int(INITIAL_FUND / CHECK_SIZE) into table 'position_limit'
def set_position_limit_default(position_limit=None):
    if position_limit is None: 
        try:
            INITIAL_FUND = int(os.getenv('INITIAL_FUND', 100_000))
            CHECK_SIZE = int(os.getenv('CHECK_SIZE', 10_000))
            position_limit = int(INITIAL_FUND / CHECK_SIZE)
        except: return False
    else:
        try: position_limit = int(float(position_limit))
        except: return False

    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Insert POSITIONS_LIMIT = int(INITIAL_FUND / CHECK_SIZE) into table 'position_limit'
    cursor.execute(f"INSERT INTO position_limit (Date, PositionLimit) VALUES (CURDATE(), {position_limit})")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print(f"POSITIONS_LIMIT = {position_limit} inserted successfully!")
    return True

# read the latest record from table 'position_limit', return the PositionLimit
def get_position_limit():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Read the latest record from table 'position_limit', return the PositionLimit
    cursor.execute("SELECT PositionLimit FROM position_limit ORDER BY ID DESC LIMIT 1")
    result = cursor.fetchall()
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    return result[0][0]

# Create a table "trading_bot_switch" to record the trading bot switch status
def create_trading_bot_switch_table():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create a new table 'trading_bot_switch', with ID (key), Date, SwitchStatus (boolean)
    cursor.execute("CREATE TABLE IF NOT EXISTS trading_bot_switch (ID INTEGER PRIMARY KEY AUTO_INCREMENT, Date DATE, SwitchStatus BOOLEAN)")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print("Table 'trading_bot_switch' created successfully!")
    return True


# Insert a new record into table "trading_bot_switch", make SwitchStatus = True
def trading_bot_switch_on():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Insert a new record into table "trading_bot_switch", make SwitchStatus = True
    cursor.execute("INSERT INTO trading_bot_switch (Date, SwitchStatus) VALUES (CURDATE(), True)")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print("Trading bot switch is ON!")
    return True

# Insert a new record into table "trading_bot_switch", make SwitchStatus = False
def trading_bot_switch_off():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Insert a new record into table "trading_bot_switch", make SwitchStatus = False
    cursor.execute("INSERT INTO trading_bot_switch (Date, SwitchStatus) VALUES (CURDATE(), False)")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print("Trading bot switch is OFF!")
    return True

# Read the latest record from table "trading_bot_switch", return the SwitchStatus
def trading_bot_switch_status():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Read the latest record from table "trading_bot_switch", return the SwitchStatus
    cursor.execute("SELECT SwitchStatus FROM trading_bot_switch ORDER BY ID DESC LIMIT 1")
    result = cursor.fetchall()
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    return result[0][0]

# define a function to drop table by input table name
def drop_table(table_name):
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Drop table
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Table '{table_name}' dropped successfully!")
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

    # Initial Step 5: Create net_profit_daily_record tables
    create_net_profit_daily_record_table()

    # Initial Step 6: Create trading_bot_switch tables
    create_trading_bot_switch_table()

    # Initial Step 7: Insert a new record into table "trading_bot_switch", make SwitchStatus = True
    create_target_profit_table()
    set_target_profit_default(target_profit = float(os.getenv('TARGET_PROFIT', 0.05)))

    # Initial Step 8: Create position_limit tables
    create_position_limit_table()

    # Initial Step 9: Insert a new record into table "position_limit", make PositionLimit = int(INITIAL_FUND / CHECK_SIZE)
    set_position_limit_default()

    # Initial Step 10: Insert a new record into table "trading_bot_switch", make SwitchStatus = True
    trading_bot_switch_on()

    trading_bot_status = trading_bot_switch_status()
    if not trading_bot_status: print("Trading bot is OFF!")
    else: print("Trading bot is ACTIVE!")

    print("All tables created successfully!")

