from Tradingview_handler import *

app = Flask(__name__)
JUST_STARTED = True
UPDATE_ID = int(os.getenv('UPDATE_ID'))

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
    global UPDATE_ID

    try:
        # Get the message from Telegram
        update = request.get_json()

        if update:
            print(json.dumps(update, indent=2))
            update_id = update['update_id']

            if 'message' in update:

                if not (JUST_STARTED or update_id == UPDATE_ID + 1): 
                    latest_message_dict = get_latest_message_from_telegram_messages_table()

                    if not update_id == latest_message_dict['update_id'] + 1: return jsonify({'status': 'success'})

                UPDATE_ID = update_id
                JUST_STARTED = False

                try: r = insert_telegram_message_from_webhook(update)
                except: pass

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

                    

    except: pass

    return jsonify({'status': 'success'})



# Run the application
if __name__ == '__main__':
    app.run()
