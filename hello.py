from Bot_messages import *

app = Flask(__name__)


@app.route("/")
def hello_world():

    # Show a hyperlink of LEOWANG.NET to the website
    return '<a href="https://leowang.net">LEOWANG.NET</a>'

# Create a webhook to receive messages from Tradingview
@app.route('/tv', methods=['POST'])
def tv():
    # Get the json data
    data = request.json

    print(data)
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


# Create a webhook to receive messages from Telegram
@app.route('/tg', methods=['POST'])
def tg():
    # Get the json data
    data = request.json
    message = data.get('message', None)
    if not message: return {'message': 'Invalid data'}, 200

    print(json.dumps(message, indent=2))

    chat_id = message['message']['chat']['id']

    # Check if the chat_id is valid
    if chat_id != TG_BOT_OWNER_ID: 
        print(f"chat_id: {chat_id}, message: {message}")
        return {'message': 'Owner Only'}, 200

    try: handel_telegram_message_from_webhook(message)
    except: pass

    return {'message': 'Thanks'}, 200


# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
