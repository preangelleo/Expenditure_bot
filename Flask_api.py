from Top_functions import *

# Flask app and API initialization
app = Flask(__name__)


# Home route
@app.route('/')
def home():
    return """
    <html>
    <body style="text-align: center;">
        <h1>LEOWANG.NET</h1>
    </body>
    </html>
    """


# Create a webhook to receive messages from Tradingview
@app.route('/tv', methods=['POST'])
def tv():
    # Get the json data
    data = request.get_json()
    '''{"condition": "P", "message": "1234567"}'''

    try:
        # Extract the message
        message = data.get('message', 'None')
        condition = data.get('condition', 'None').upper()
    except: return {'message': 'Invalid data'}, 200

    trading_bot_status = trading_bot_switch_status()

    if not trading_bot_status and condition == 'P': webhook_switch_on_bot(message, TG_BOT_OWNER_ID)
    elif trading_bot_status and condition == 'N': webhook_switch_off_bot(message, TG_BOT_OWNER_ID)

    return {'message': 'Thanks'}, 200


# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
