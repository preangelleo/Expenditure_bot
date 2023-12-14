from Tradingview_handler import *

app = Flask(__name__)
JUST_STARTED = True

@app.route("/")
def hello_world():

    # Show a hyperlink of LEOWANG.NET to the website
    return '<a href="https://leowang.net">LEOWANG.NET</a>'

# Create a webhook to receive messages from Tradingview
@app.route(f'/{TRADINGVIEW_WEBHOOK}', methods=['POST'])
def tv_webhook():
    try:
        data = request.json
        if data['token'] == TRADINGVIEW_WEBHOOK_TOKEN: tradingview_webhook_handler(data)

    except: pass

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
                        if chat_id != TG_BOT_OWNER_ID: 
                            send_msg(f'THIS BOT IS OWNER ONLY.\n\nLEOWANG.net', chat_id)
                            return jsonify({'status': 'success'})
                        
                        if message['from']['first_name'] != TELEGRAM_OWNER_FIRST_NAME: return jsonify({'status': 'success'})
                        if message['from']['username'] != TELEGRAM_OWNER_USERNAME: return jsonify({'status': 'success'})

                        try: handel_telegram_message_from_webhook(message)
                        except: pass

                        JUST_STARTED = False

    except: pass

    return jsonify({'status': 'success'})



# Run the application
if __name__ == '__main__':
    app.run()
