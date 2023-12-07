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
db_name = os.getenv('DB_NAME')

try:
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password,
        port=db_port
    )

    if conn.is_connected():
        cursor = conn.cursor()

        # SQL query to create a new table
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

        # Execute the query
        cursor.execute(create_table_query)
        conn.commit()
        print("Table 'expenditure_table' created successfully.")

except Error as e:
    print(f"Error connecting to MySQL: {e}")

finally:
    if conn and conn.is_connected():
        conn.close()
        print("MySQL connection is closed")

