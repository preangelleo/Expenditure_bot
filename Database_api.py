from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_httpauth import HTTPTokenAuth
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os, json, requests
from flask import make_response


# Load environment variables
load_dotenv()

# Database connection function
def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )
    return conn

# Flask app and API initialization
app = Flask(__name__)
api = Api(app)

# Load the admin token from the .env file
admin_token = os.getenv('ADMIN_TOKEN')

# Authentication
auth = HTTPTokenAuth(scheme='Bearer')
tokens = {
    admin_token: "admin"  # You can add more tokens as needed
}

@auth.verify_token
def verify_token(token):
    # print(f"Received token: {token}")
    # print(f"Expected tokens: {tokens}")
    if token in tokens:
        return tokens[token]
    return None

# Expenditure Resource
class ExpenditureList(Resource):
    @auth.login_required
    def get(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM expenditure_table")
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return {'data': records}, 200
        except Error as e:
            return {'error': str(e)}, 500

    @auth.login_required
    def post(self):
        try:
            data = request.get_json()
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
            INSERT INTO expenditure_table 
            (item, category, unit_price, units, date, time, currency, tax, tips) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (data['item'], data['category'], data['unit_price'], data['units'], data['date'], data['time'], data['currency'], data['tax'], data['tips']))
            conn.commit()
            cursor.close()
            conn.close()
            return {'message': 'Record added successfully'}, 201
        except Error as e:
            return {'error': str(e)}, 500
        
# define a function to insert a line of record into the expenditure_table
def insert_expenditure_record(item, category, unit_price, units, date, time, currency, tax, tips):
    print(f"Inserting: item: {item}; category: {category}; unit_price: {unit_price}; units: {units}; date: {date}; time: {time}; currency: {currency}; tax: {tax}; tips: {tips}")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO expenditure_table 
        (item, category, unit_price, units, date, time, currency, tax, tips) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (item, category, unit_price, units, date, time, currency, tax, tips))
        conn.commit()
        cursor.close()
        conn.close()
        return {'message': 'Record added successfully'}, 201
    except Error as e:
        return {'error': str(e)}, 500
    
# difine a function to send telegram message to a chat_id using requests + telegram bot api
def send_telegram_message(message, chat_id=os.getenv('TG_BOT_OWNER_ID')):
    print(f"Sending message to chat_id: {chat_id}")
    try:
        url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message
        }
        response = requests.post(url, data=data)
        return response.json()
    except Error as e:
        return {'error': str(e)}, 500
