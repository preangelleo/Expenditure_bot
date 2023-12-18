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
    try:
        global JUST_STARTED
        global UPDATE_ID
        print(f"PREVIOUS UPDATE_ID: {UPDATE_ID}, JUST_STARTED: {JUST_STARTED}")
        if JUST_STARTED: send_msg(f"This is the first message after the bot was restarted. \n\nCurrent update_id: {UPDATE_ID}", TG_BOT_OWNER_ID)

        # Get the message from Telegram
        update = request.get_json()

        if update:
            print(json.dumps(update, indent=2))
            
            update_id = update['update_id']
            update_id = int(update_id)

            if 'message' in update:

                if not JUST_STARTED and update_id != UPDATE_ID + 1: 
                    # latest_message_dict = get_latest_message_from_telegram_messages_table()

                    # if update_id != latest_message_dict['update_id'] + 1: 
                    try: 
                        message_text = update['message']['text']
                        if str(message_text) != str(RESET_TELEGRAM_TOKEN): return jsonify({'status': 'success'})
                    except: return jsonify({'status': 'success'})

                UPDATE_ID = update_id
                JUST_STARTED = False

                print(f"CURRENT UPDATE_ID: {UPDATE_ID}, JUST_STARTED: {JUST_STARTED}")

                # try: r = insert_telegram_message_from_webhook(update)
                # except: pass

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
                    except Exception as e: print(f"ERROR while handel_telegram_message_from_webhook(): \n\n{e}\n\n")


    except Exception as e: print(f"ERROR while tg_webhook(): \n\n{e}\n\n")

    return jsonify({'status': 'success'})



# Run the application
if __name__ == '__main__':
    app.run()
