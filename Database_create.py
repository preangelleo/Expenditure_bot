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


# create a funciton to drop current trading_parameters table
def drop_trading_parameters_table():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Drop table
    cursor.execute(f"DROP TABLE IF EXISTS trading_parameters")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Table 'trading_parameters' dropped successfully!")
    return True


def create_trading_parameters_table():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create a new table 'trading_parameters'
    cursor.execute("CREATE TABLE IF NOT EXISTS trading_parameters (ID INTEGER PRIMARY KEY AUTO_INCREMENT, trading_bot_status TINYINT, initial_fund_spot INTEGER, initial_funding_fund INTEGER, check_size INTEGER, position_limit_spot INTEGER, target_profit_usdt INTEGER, target_profit_percentage FLOAT, daily_target_profit INTEGER, daily_new_positions_limit INTEGER, bot_starting_date DATE, trading_volume_limit INTEGER, fully_diluted_market_cap_up_limit BIGINT, market_cap_down_limit BIGINT, circulation_ratio FLOAT)")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print("Table 'trading_parameters' created successfully!")
    return True


# Create a function to initialize the trading parameters table
def set_trading_parameters_default():
    drop_trading_parameters_table()
    create_trading_parameters_table()
    TRADING_VOLUME_LIMIT = int(os.getenv('TRADING_VOLUME_LIMIT', 50_000_000))
    INITIAL_FUND = int(os.getenv('INITIAL_FUND', 100_000))
    CHECK_SIZE = int(os.getenv('CHECK_SIZE', 10_000))
    POSITIONS_LIMIT = int(INITIAL_FUND / CHECK_SIZE)
    FULLLY_DILUTED_MARKET_CAP_UP_LIMIT=int(os.getenv('FULLLY_DILUTED_MARKET_CAP_UP_LIMIT', 50_000_000_000))
    MARKET_CAP_DOWN_LIMIT=int(os.getenv('MARKET_CAP_DOWN_LIMIT', 50_000_000))
    CIRCULATION_RATIO=float(os.getenv('CIRCULATION_RATIO', 0.3))
    TARGET_PROFIT_PERCENTAGE = float(os.getenv('TARGET_PROFIT', 0.05))
    TARGET_PROFIT_USDT = int(TARGET_PROFIT_PERCENTAGE * CHECK_SIZE)
    DAILY_TARGET_PROFIT = 1000
    DAILY_NEW_POSITIONS_LIMIT = 2

    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Insert trading parameters into table 'trading_parameters'
    cursor.execute(f"INSERT INTO trading_parameters (trading_bot_status, initial_fund_spot, initial_funding_fund, check_size, position_limit_spot, target_profit_usdt, target_profit_percentage, daily_target_profit, daily_new_positions_limit, bot_starting_date, trading_volume_limit, fully_diluted_market_cap_up_limit, market_cap_down_limit, circulation_ratio) VALUES (1, {INITIAL_FUND}, {INITIAL_FUND}, {CHECK_SIZE}, {POSITIONS_LIMIT}, {TARGET_PROFIT_USDT}, {TARGET_PROFIT_PERCENTAGE}, {DAILY_TARGET_PROFIT}, {DAILY_NEW_POSITIONS_LIMIT}, CURDATE(), {TRADING_VOLUME_LIMIT}, {FULLLY_DILUTED_MARKET_CAP_UP_LIMIT}, {MARKET_CAP_DOWN_LIMIT}, {CIRCULATION_RATIO})")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Trading parameters inserted successfully!")
    return True


def set_daily_new_positions_limit(daily_new_positions_limit = 2):
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # change daily_new_positions_limit in trading_parameters table to given value
    cursor.execute(f"UPDATE trading_parameters SET daily_new_positions_limit = {daily_new_positions_limit}")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print(f"daily_new_positions_limit = {daily_new_positions_limit} inserted successfully!")
    return True


def reset_bot_starting_date(bot_starting_date = '2023-12-12'):
    # convert bot_starting_date to date format
    bot_starting_date = datetime.strptime(bot_starting_date, '%Y-%m-%d').date()
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # change bot_starting_date in trading_parameters table to given value
    cursor.execute(f"UPDATE trading_parameters SET bot_starting_date = '{bot_starting_date}'")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print(f"bot_starting_date = {bot_starting_date} inserted successfully!")
    return True


def read_daily_new_positions_limit():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Read the latest record from table 'daily_new_positions_limit', return the daily_new_positions_limit
    cursor.execute("SELECT daily_new_positions_limit FROM trading_parameters ORDER BY ID DESC LIMIT 1")
    result = cursor.fetchall()
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    return result[0][0]

def set_initial_funding_fund(initial_funding_fund = 10_0000):
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # change initial_funding_fund in trading_parameters table to given value
    cursor.execute(f"UPDATE trading_parameters SET initial_funding_fund = {initial_funding_fund}")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print(f"initial_funding_fund = {initial_funding_fund} inserted successfully!")
    return True

def read_initial_funding_fund():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Read the latest record from table 'initial_funding_fund', return the initial_funding_fund
    cursor.execute("SELECT initial_funding_fund FROM trading_parameters ORDER BY ID DESC LIMIT 1")
    result = cursor.fetchall()
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    return result[0][0]

# insert TARGET_PROFIT = float(os.getenv('TARGET_PROFIT', 0.05)) into table 'target_profit'
def set_target_profit_default(target_profit = float(os.getenv('TARGET_PROFIT', 0.05))):
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # change target_profit_percentage in trading_parameters table to given value
    cursor.execute(f"UPDATE trading_parameters SET target_profit_percentage = {target_profit}")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print(f"TARGET_PROFIT = {target_profit} inserted successfully!")
    return True


def set_position_limit_default(position_limit=10):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE trading_parameters SET position_limit_spot = {position_limit}")
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
    cursor.execute("SELECT position_limit_spot FROM trading_parameters ORDER BY ID DESC LIMIT 1")
    result = cursor.fetchall()
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    return result[0][0]


# Insert a new record into table "trading_bot_switch", make SwitchStatus = True
def trading_bot_switch_on():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # When switch trading bot on, update target_profit_percentage to 0.13, and daily_target_profit to 2000, and daily_new_positions_limit to 4， target_profit_usdt to 1300， trading_bot_status to 1
    cursor.execute("UPDATE trading_parameters SET trading_bot_status = 1, target_profit_percentage = 0.13, daily_target_profit = 2000, daily_new_positions_limit = 4, target_profit_usdt = 1300")
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
    # When switch trading bot off, update daily_target_profit to 1000, and daily_new_positions_limit to 2, trading_bot_status to 0
    cursor.execute("UPDATE trading_parameters SET trading_bot_status = 0, daily_target_profit = 1000, daily_new_positions_limit = 2")
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
    cursor.execute("SELECT trading_bot_status FROM trading_parameters ORDER BY ID DESC LIMIT 1")
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


# define a function to create a 'trivial_records' table to save the trivial save records, only two columns: ID as a Key auto increment, Info as TEXT
def create_trivial_records_table():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create a new table 'trivial_records'
    cursor.execute("CREATE TABLE IF NOT EXISTS trivial_records (ID INTEGER PRIMARY KEY AUTO_INCREMENT, Info TEXT)")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print("Table 'trivial_records' created successfully!")
    return True

'''("CREATE TABLE IF NOT EXISTS white_list (id INT NOT NULL AUTO_INCREMENT, symbol VARCHAR(20) DEFAULT NULL, PRIMARY KEY (id))")'''
# Define a function to create a white_list table to save the white list
def create_white_list_table():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create a new table 'white_list'
    cursor.execute("CREATE TABLE IF NOT EXISTS white_list (id INT NOT NULL AUTO_INCREMENT, symbol VARCHAR(20) DEFAULT NULL, PRIMARY KEY (id))")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print("Table 'white_list' created successfully!")
    return True


# Define a function to create a white_list table to save the white list
def create_holding_list_table():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create a new table 'white_list'
    cursor.execute("CREATE TABLE IF NOT EXISTS holding_list (id INT NOT NULL AUTO_INCREMENT, coin VARCHAR(20) DEFAULT NULL, PRIMARY KEY (id))")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print("Table 'holding_list' created successfully!")
    return True


# define a function to insert a new coin into holding_list table, check if the coin is already in the table, if yes, return 2, if not, insert the coin and return 1, if error, return 0
def insert_coin_into_holding_list(coin):
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check if the coin is already in the table
    cursor.execute(f"SELECT * FROM holding_list WHERE coin = '{coin}'")
    result = cursor.fetchall()
    if len(result) == 0: 
        # Insert a new coin into holding_list table
        cursor.execute(f"INSERT INTO holding_list (coin) VALUES ('{coin}')")
        # Commit the session
        conn.commit()
        cursor.close()
        conn.close()
        print(f"{coin} inserted successfully!")
        return 1
    else: 
        cursor.close()
        conn.close()
        print(f"{coin} already in the list!")
        return 2
    

# define a function to remove a coin from holding_list table, check if the coin is already in the table, if yes, remove the coin and return 1, if not, return 2, if error, return 0
def remove_coin_from_holding_list(coin):
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check if the coin is already in the table
    cursor.execute(f"SELECT * FROM holding_list WHERE coin = '{coin}'")
    result = cursor.fetchall()
    if len(result) > 0: 
        # Remove a coin from holding_list table
        cursor.execute(f"DELETE FROM holding_list WHERE coin = '{coin}'")
        # Commit the session
        conn.commit()
        cursor.close()
        conn.close()
        print(f"{coin} removed successfully!")
        return 1
    else: 
        cursor.close()
        conn.close()
        print(f"{coin} not in the list!")
        return 2


# define a function to get all coins from holding_list table, return a list of coins
def read_holding_list():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Get all coins from holding_list table
    cursor.execute(f"SELECT coin FROM holding_list")
    result = cursor.fetchall()
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    return [item[0] for item in result]


# Define a function to create a table for white_list_users, with ID (key), Status (bolean), From_id (string, not none), Username (string, not none), First_name (default none), Last_name (default none), Date (date)
def create_white_list_users_table():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create a new table 'white_list_users'
    cursor.execute("CREATE TABLE IF NOT EXISTS white_list_users (ID INTEGER PRIMARY KEY AUTO_INCREMENT, Status BOOLEAN, From_id VARCHAR(255) NOT NULL, Username VARCHAR(255) NOT NULL, First_name VARCHAR(255), Last_name VARCHAR(255), Date DATE)")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print("Table 'white_list_users' created successfully!")
    return True


# Define a function to insert a new record into table "white_list_users", make Status = True, first step convert input from_id to string
def insert_white_list_users(from_id, username, first_name=None, last_name=None, status=False):
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the from_id is already in the table, if yes, just set the Status to status
    cursor.execute(f"SELECT * FROM white_list_users WHERE From_id = '{from_id}'")
    result = cursor.fetchall()
    if len(result) > 0:
        previous_status = result[0][1]
        if status:
            if previous_status: return f"/{from_id} is already in the white list!"
            else: 
                cursor.execute(f"UPDATE white_list_users SET Status = {status} WHERE From_id = '{from_id}'")
                conn.commit()
                cursor.close()
                conn.close()
                return f"/{from_id} added to white list successfully!"
        if not status:
            if not previous_status: return f"/{from_id} has already applied previously, please be patient!"
            else: 
                cursor.execute(f"UPDATE white_list_users SET Status = {status} WHERE From_id = '{from_id}'")
                conn.commit()
                cursor.close()
                conn.close()
                return f"/{from_id} removed from white list successfully!"
    else:
        # Insert a new record into table "white_list_users", make Status = True
        cursor.execute(f"INSERT INTO white_list_users (Status, From_id, Username, First_name, Last_name, Date) VALUES ({status}, '{from_id}', '{username}', '{first_name}', '{last_name}', CURDATE())")
        # Commit the session
        conn.commit()
        cursor.close()
        conn.close()
        if not status: return f"/{from_id} aplying for white list, submitted successfully! Please wait for the approval!"
        else: return f"/{from_id} added to white list successfully!"


# Define a function to set a from_id status to True
def set_white_list_users_status_true(from_id):
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Set a from_id status to True
    cursor.execute(f"UPDATE white_list_users SET Status = True WHERE From_id = '{from_id}'")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print(f"/{from_id} status set to True successfully!")
    return True


# Define a function to set a from_id status to False
def set_white_list_users_status_false(from_id):
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Set a from_id status to False
    cursor.execute(f"UPDATE white_list_users SET Status = False WHERE From_id = '{from_id}'")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print(f"/{from_id} status set to False successfully!")
    return True


# set white list by username
def set_white_list_by_username(username, status=True):
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Set white list by username
    cursor.execute(f"UPDATE white_list_users SET Status = {status} WHERE Username = '{username}'")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print(f"@{username} status set to {status} successfully!")
    return True


# remove white list by username
def remove_white_list_by_username(username):
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Remove white list by username
    cursor.execute(f"DELETE FROM white_list_users WHERE Username = '{username}'")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print(f"@{username} removed from white list successfully!")
    return True


# Define a function to check if a from_id is in white_list_users table and the status is True
def check_white_list_users(from_id):
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check if a from_id is in white_list_users table and the status is True
    cursor.execute(f"SELECT * FROM white_list_users WHERE From_id = '{from_id}' AND Status = True")
    result = cursor.fetchall()
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    if len(result) > 0: return True
    else: return False


# Define a function to store and manage one time passcode key and app_name
def create_one_time_passcode_table():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create a new table 'one_time_passcode'
    cursor.execute("CREATE TABLE IF NOT EXISTS one_time_passcode (ID INTEGER PRIMARY KEY AUTO_INCREMENT, AppName VARCHAR(255), Passcode_Key VARCHAR(255), Date DATE)")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print("Table 'one_time_passcode' created successfully!")
    return True


# Define a function to insert a new record into table "one_time_passcode" if the app_name is not in the table, othewise update the key
def insert_one_time_passcode(app_name, Passcode_Key):
    app_name = app_name.lower()

    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check if the app_name is already in the table
    cursor.execute(f"SELECT * FROM one_time_passcode WHERE AppName = '{app_name}'")
    result = cursor.fetchall()
    if len(result) == 0: 
        # Insert a new record into table "one_time_passcode"
        cursor.execute(f"INSERT INTO one_time_passcode (AppName, Passcode_Key, Date) VALUES ('{app_name}', '{Passcode_Key}', CURDATE())")
    else: 
        # Update the key
        cursor.execute(f"UPDATE one_time_passcode SET Passcode_Key = '{Passcode_Key}' WHERE AppName = '{app_name}'")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Passcode_Key inserted successfully for {app_name}!")
    return True


# Define a function to get the key from table "one_time_passcode" by app_name
def get_one_time_passcode(app_name):
    app_name = app_name.lower()

    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check if the app_name is already in the table
    cursor.execute(f"SELECT Passcode_Key FROM one_time_passcode WHERE AppName = '{app_name}'")
    result = cursor.fetchall()
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    if len(result) == 0: return None
    else: return result[0][0]


def remove_white_list_by_username(username):
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Remove white list by username
    cursor.execute(f"DELETE FROM white_list_users WHERE Username = '{username}'")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print(f"@{username} removed from white list successfully!")
    return True



def remove_from_future_profit_table(coin):
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM umfuture_orders_profit WHERE coin = '{coin}'")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print(f"{coin} removed from umfuture_orders_profit successfully!")
    return True


# Function to find all tables in the database
def find_all_tables():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Find all tables in the database
    cursor.execute("SHOW TABLES")
    result = cursor.fetchall()
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    return result


# Function to get table structure and save all of them into a singal file
def save_table_structures():
    result = find_all_tables()
    for table in result:
        # Create a new session
        conn = get_db_connection()
        cursor = conn.cursor()
        # Get table structure and save to a file
        cursor.execute(f"SHOW CREATE TABLE {table[0]}")
        result = cursor.fetchall()
        # Commit the session
        conn.commit()
        cursor.close()
        conn.close()
        with open(f"table_structure.sql", "a") as f:
            f.write(f"{result[0][1]}\n\n")


# Set year and Month of NoN to current year and Month value
def set_year_month():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # Set year column value of binance_funding_profits table to 2044 and Month column value to 1
    cursor.execute(f"UPDATE binance_funding_profits SET year = {datetime.now().year}, Month = {datetime.now().month} WHERE year IS NULL OR Month IS NULL")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Year column value of binance_funding_profits table set to 2004 and Month column value to 1 successfully!")
    return True


# print the structure of binance_funding_profits
def print_binance_funding_profits_structure():
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    # print the structure of binance_funding_profits
    cursor.execute(f"SHOW CREATE TABLE binance_funding_profits")
    result = cursor.fetchall()
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print(result[0][1])
    return True


if __name__ == '__main__':
    print("Create database and tables...")
    # Initial Step 1: Create database
    create_database()

    # Initial Step 2: Create user_expenditures_record tables
    create_expenditure_record_table()

    # # Initial Step 3: Create OTP tables
    create_one_time_passcode_table()

    # Initial Step 4: Create net_profit_daily_record tables
    create_net_profit_daily_record_table()

    # Initial Step 5: Create trading_parameters tables
    set_trading_parameters_default()

    # Initial Step 6: Create trivial_records tables
    create_trivial_records_table()

    # Initial Step 7: Create white_list_users tables
    create_white_list_users_table()

    # Initial Step 8: Create holding_list tables
    create_holding_list_table()

    print("All tables created successfully!")

