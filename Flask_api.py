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
        with engine.connect() as connection:
            try:
                sql = text("SELECT * FROM user_expenditures_record")
                result = connection.execute(sql)
                records = [dict(row) for row in result]
                return {'data': records}, 200
            except SQLAlchemyError as e:
                return {'error': str(e)}, 500

    @auth.login_required
    def post(self):
        try:
            data = request.get_json()
            with engine.connect() as connection:
                sql = text("""
                    INSERT INTO user_expenditures_record 
                    (From_id, Date, Time, Spent, Category, PaymentMethod, Merchant, ItemName, Price, Card_Number, Tax, Tips, Address, Receipt_Image_URL) 
                    VALUES 
                    (:From_id, :Date, :Time, :Spent, :Category, :PaymentMethod, :Merchant, :ItemName, :Price, :Card_Number, :Tax, :Tips, :Address, :Receipt_Image_URL)
                """)

                connection.execute(sql, data)
                connection.commit()

            return {'message': 'Record added successfully'}, 201

        except SQLAlchemyError as e:
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


# Adding a new page 'table' to display the records in "user_expenditures_record", add lines for sum of total spend, total tax, total tips; user can choose to display records by merchant, month, year or category; user can also choose to sort the records by date, spent; defaultly sorted by ID with descending order.

@app.route('/table')
def table():
    query = "SELECT * FROM user_expenditures_record"
    df = pd.DataFrame(engine.connect().execute(text(query)).fetchall())

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
