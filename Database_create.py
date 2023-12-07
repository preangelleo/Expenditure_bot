import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database connection parameters
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_port = os.getenv('DB_PORT')

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
        cursor.execute("CREATE DATABASE IF NOT EXISTS expenditure_records")
        cursor.close()
        conn.close()

        # Connect to the newly created database
        conn = mysql.connector.connect(
            host=db_host,
            database='expenditure_records',
            user=db_user,
            password=db_password,
            port=db_port
        )

        # Create a new table
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS expenditure_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            item VARCHAR(255),
            category VARCHAR(255),
            unit_price DECIMAL(10, 2),
            units INT,
            date DATE,
            time TIME,
            currency VARCHAR(50),
            tax DECIMAL(10, 2),
            tips DECIMAL(10, 2)
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()

except Error as e:
    print(f"Error connecting to MySQL: {e}")

finally:
    if conn.is_connected():
        conn.close()
        print("MySQL connection is closed")

