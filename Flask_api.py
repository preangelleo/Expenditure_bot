from Database_api import *

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
        total_unit_price = sum(float(row['unit_price']) for row in records)
        total_tips = sum(float(row['tips']) for row in records)
        return """
        <html>
        <head>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid black;
                    padding: 5px;
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <h1 style="text-align: center;">Expenditure Table</h1>
            <table>
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
                "\n".join(["<tr><td>" + "</td><td>".join([str(row[col]) for col in ['item', 'category', 'unit_price', 'units', 'date', 'time', 'currency', 'tax', 'tips']]) + "</td></tr>" for row in records]) + \
                """
                <tr>
                    <td colspan="2">Summarize</td>
                    <td>""" + str(total_unit_price) + """</td>
                    <td colspan="5"></td>
                    <td>""" + str(total_tips) + """</td>
                </tr>
            </table>
        </body>
        </html>
        """
    except Error as e:
        return {'error': str(e)}, 500

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
