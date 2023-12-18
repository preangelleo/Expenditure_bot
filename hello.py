from Tradingview_handler import *

app = Flask(__name__)

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
        # Get the message from Telegram
        update = request.get_json()

        if update:
            # print(json.dumps(update, indent=2))

            update_id = update['update_id']

            if 'message' in update:

                latest_message_dict = get_latest_message_from_telegram_messages_table()

                if update_id != latest_message_dict['update_id'] + 1: 
                    try: 
                        message_text = update['message']['text'].replace('/', '')
                        if message_text != RESET_TELEGRAM_TOKEN or update['message']['from']['id'] != TG_BOT_OWNER_ID: 
                            user_name = update['message']['from']['username'] if 'username' in update['message']['from'] else update['message']['from']['first_name'] if 'first_name' in update['message']['from'] else update['message']['from']['last_name'] if 'last_name' in update['message']['from'] else 'UNKNOWN'
                            alert_info = f"Someone else is trying to send message to this bot.\n\nUpdate_id: {update_id}\nFrom_id: {update['message']['from']['id']}\nFrom_name: {user_name}\n\nMessage: \n\n{message_text}"
                            if update['message']['from']['id'] != TG_BOT_OWNER_ID: send_msg(alert_info, TG_BOT_OWNER_ID)
                            if message_text != RESET_TELEGRAM_TOKEN: send_msg(f"Update_id unmatch with previous records, please click below token to reset:\n\n/{RESET_TELEGRAM_TOKEN}", TG_BOT_OWNER_ID)
                            return jsonify({'status': 'success'})
                        else:
                            message_id = update['message']['message_id']
                            try: delete_msg(TG_BOT_OWNER_ID, message_id)
                            except: pass 

                            send_msg(f"Telegram bot was reset successfully.", TG_BOT_OWNER_ID)

                    except: return jsonify({'status': 'success'})

                try: insert_telegram_message_from_webhook(update)
                except Exception as e: print(f"ERROR while insert_telegram_message_from_webhook(): \n\n{e}\n\n")

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
