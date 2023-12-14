from Top_functions import *
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# # Create a webhook to receive messages from Tradingview
# @app.route('/tv', methods=['POST'])
# def tv():
#     # Get the json data
#     data = request.json

#     print(data)
#     '''{"condition": "P", "message": "1234567"}'''

#     try:
#         # Extract the message
#         message = data.get('message', 'None')
#         condition = data.get('condition', 'None').upper()
#     except: return {'message': 'Invalid data'}, 200

#     trading_bot_status = trading_bot_switch_status()

#     if not trading_bot_status and condition == 'P': webhook_switch_on_bot(message, TG_BOT_OWNER_ID)
#     elif trading_bot_status and condition == 'N': webhook_switch_off_bot(message, TG_BOT_OWNER_ID)

#     return {'message': 'Thanks'}, 200


# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
