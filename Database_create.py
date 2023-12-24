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


# DELETE coin from ignore_coin_list where symbol = 'coin'
def remove_from_ignore_coin_table(coin):
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM ignore_coin_list WHERE symbol = '{coin}'")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print(f"{coin} removed from ignore_coin_list successfully!")
    return True


def remove_from_white_list_table(coin):
    # Create a new session
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM white_list WHERE symbol = '{coin}'")
    # Commit the session
    conn.commit()
    cursor.close()
    conn.close()
    print(f"{coin} removed from white_list successfully!")
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

    # Initial Step 11: Create trivial_records tables
    create_trivial_records_table()

    # Initial Step 12: Create white_list tables
    create_white_list_table()

    # Initial Step 13: Create white_list_users tables
    create_white_list_users_table()

    # Initial Step 14: Create one_time_passcode tables
    create_one_time_passcode_table()
    
    trading_bot_status = trading_bot_switch_status()
    if not trading_bot_status: print("Trading bot is OFF!")
    else: print("Trading bot is ACTIVE!")

    # save_table_structures()

    print("All tables created successfully!")

