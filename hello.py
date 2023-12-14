from Bot_messages import *

app = Flask(__name__)
JUST_STARTED = True

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
@app.route(f'/{TELEGRAM_BOT_WEBHOOK_TOKEN}', methods=['POST'])
def tg_webhook():
    global JUST_STARTED

    try:
        # Get the message from Telegram
        update = request.get_json()

        if update:
            print(json.dumps(update, indent=2))
            update_id = update['update_id']
            print(f'update_id = {update_id}')

            if 'message' in update:

                latest_message_dict = get_latest_message_from_telegram_messages_table()

                if update_id == latest_message_dict['update_id'] + 1 or JUST_STARTED: 

                    try: r = insert_telegram_message_from_webhook(update)
                    except: return jsonify({'status': 'success'})

                    if not r: return jsonify({'status': 'success'})

                    message = update['message']
                    chat_id = message['chat']['id']

                    # if it's not private chat, return
                    if message['chat']['type'] == 'private': 
                        if message['from']['id'] != TG_BOT_OWNER_ID: 
                            send_msg(f'THIS BOT IS OWNER ONLY.\n\nLEOWANG.net', chat_id)
                            return jsonify({'status': 'success'})
                        if message['from']['first_name'] != TELEGRAM_OWNER_FIRST_NAME: return jsonify({'status': 'success'})
                        if message['from']['username'] != TELEGRAM_OWNER_USERNAME: return jsonify({'status': 'success'})

                        # print(json.dumps(message, indent=2))

                        try: handel_telegram_message_from_webhook(message)
                        except: pass

                        JUST_STARTED = False
                        print(f'JUST_STARTED = {JUST_STARTED}')

    except: pass

    return jsonify({'status': 'success'})



# Run the application
if __name__ == '__main__':
    # send_msg('Bot started...', TG_BOT_OWNER_ID)

    app.run()
