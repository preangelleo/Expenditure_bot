from Top_functions import *

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

'''
cursor.execute("CREATE TABLE IF NOT EXISTS user_expenditures_record (ID INTEGER PRIMARY KEY AUTO_INCREMENT, From_id VARCHAR(255), Date DATE, Time TIME, Spent FLOAT, Category VARCHAR(255), PaymentMethod VARCHAR(255), Merchant VARCHAR(255), ItemName VARCHAR(255), Price FLOAT, Card_Number INTEGER, Tax FLOAT, Tips FLOAT, Address VARCHAR(255), Receipt_Image_URL VARCHAR(255))")
'''

# Adding a new page 'table' to display the records in "user_expenditures_record", add lines for sum of total spend, total tax, total tips; user can choose to display records by merchant, month, year or category; user can also choose to sort the records by date, spent; defaultly sorted by ID with descending order.

@app.route('/table')
def table():
    df = pd.read_sql_query("SELECT * FROM user_expenditures_record", con=engine)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Time'] = pd.to_datetime(df['Time'])
    df['Spent'] = pd.to_numeric(df['Spent'])
    df['Price'] = pd.to_numeric(df['Price'])
    df['Tax'] = pd.to_numeric(df['Tax'])
    df['Tips'] = pd.to_numeric(df['Tips'])
    df['Card_Number'] = pd.to_numeric(df['Card_Number'])
    df['Receipt_Image_URL'] = df['Receipt_Image_URL'].astype(str)
    df['From_id'] = df['From_id'].astype(str)
    df['Category'] = df['Category'].astype(str)
    df['PaymentMethod'] = df['PaymentMethod'].astype(str)
    df['Merchant'] = df['Merchant'].astype(str)
    df['ItemName'] = df['ItemName'].astype(str)
    df['Address'] = df['Address'].astype(str)
    df['ID'] = pd.to_numeric(df['ID'])
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    df['Day'] = df['Date'].dt.day
    
    sum_spend = df['Spent'].sum()
    sum_tax = df['Tax'].sum()
    sum_tips = df['Tips'].sum()

    # display table with html
    return render_template('view.html', tables=[df.to_html(classes='data', index=False)], titles=df.columns.values, sum_spend=sum_spend, sum_tax=sum_tax, sum_tips=sum_tips)


# Adding the resource to API
api.add_resource(ExpenditureList, '/expenditures')

@app.errorhandler(400)
def bad_request_error(error):
    # 在这里添加你的日志记录代码
    app.logger.error(error)
    return make_response(jsonify({'error': 'Bad request'}), 400)

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
