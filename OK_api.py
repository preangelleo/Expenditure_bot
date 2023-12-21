from Top_functions import *

# Usage
api_key = os.getenv('OKX_API_KEY')
secret_key = os.getenv('OKX_API_SECRET')
passphrase = os.getenv('OKX_API_PASSPHRASE')

def ok_create_signature(timestamp, method, request_path, body, secret_key):
    message = timestamp + method + request_path + body
    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    return base64.b64encode(d).decode()

def ok_withdraw(api_key, secret_key, passphrase, coin, amount, destination):
    timestamp = str(datetime.utcnow().isoformat("T", "milliseconds")) + "Z"
    method = 'POST'
    request_path = '/api/v5/asset/withdrawal'
    body = json.dumps({'ccy': coin, 'amt': amount, 'dest': destination})
    
    # Create the signature
    signature = ok_create_signature(timestamp, method, request_path, body, secret_key)

    # Set the headers
    headers = {
        'OK-ACCESS-KEY': api_key,
        'OK-ACCESS-SIGN': signature,
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': passphrase,
        'Content-Type': 'application/json'
    }

    # Make the request
    response = requests.post("https://www.okx.com" + request_path, headers=headers, data=body)
    
    return response.json()

if __name__ == '__main__':
    print('OK_api.py is running...')
    coin = 'BTC'  # Example: BTC
    amount = '0.0007'  # Example: 0.01 BTC
    destination = '18a9tpwtVZsMUaU5cT2vYffo2vCFhwsop5'  # Destination address

    response = ok_withdraw(api_key, secret_key, passphrase, coin, amount, destination)
    print(response)
