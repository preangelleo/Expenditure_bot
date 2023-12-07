from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_httpauth import HTTPTokenAuth
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

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

# Home route
@app.route('/')
def home():
    return """
    <html>
    <body style="text-align: center;">
        <h1>Hello world</h1>
    </body>
    </html>
    """

# Adding a new page 'table' to display the records in "expenditure_table"
@app.route('/table')
def table():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM expenditure_table")
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return """
        <html>
        <body style="text-align: center;">
            <h1>Expenditure Table</h1>
            <table style="margin: auto;">
                <tr>
                    <th>Item</th>
                    <th>Category</th>
                    <th>Unit Price</th>
                    <th>Units</th>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Currency</th>
                    <th>Tax</th>
                    <th>Tips</th>
                </tr>
                """ + \
                "\n".join(["<tr><td>" + "</td><td>".join([str(col) for col in row]) + "</td></tr>" for row in records]) + \
                """
            </table>
        </body>
        </html>
        """
    except Error as e:
        return {'error': str(e)}, 500

# Adding the resource to API
api.add_resource(ExpenditureList, '/expenditures')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
