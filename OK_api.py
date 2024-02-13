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


def ok_market_buy(coin, usdt_amount):
    print(f"OKX market buy {usdt_amount} usdt worth of {coin} ...")
    coin = coin.upper()
    timestamp = str(datetime.utcnow().isoformat("T", "milliseconds")) + "Z"
    method = 'POST'
    request_path = '/api/v5/trade/order'
    # Prepare the body with market order parameters
    body = json.dumps({
        'instId': f"{coin}-USDT",  # Instrument ID, e.g., BTC-USDT
        'tdMode': 'cash',  # Trading mode, assuming cash here for simplicity
        'side': 'buy',  # Order side
        'ordType': 'market',  # Order type
        'sz': usdt_amount,  # Size in quote currency (USDT) for market buy
        'ccy': 'USDT',  # Specify the currency to use for the market buy
    })
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
    print(response.json())
    return response.json()


def ok_market_sell(coin, amount):
    print(f"OKX market sell {amount} {coin} ...")
    timestamp = str(datetime.utcnow().isoformat("T", "milliseconds")) + "Z"
    method = 'POST'
    request_path = '/api/v5/trade/order'
    # Prepare the body with market order parameters for selling
    body = json.dumps({
        'instId': f"{coin}-USDT",  # Instrument ID, e.g., BTC-USDT
        'tdMode': 'cash',  # Trading mode, assuming cash here for simplicity
        'side': 'sell',  # Order side for selling
        'ordType': 'market',  # Order type as market
        'sz': amount,  # Amount of the coin to sell
    })
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
    print(response.json())
    return response.json()


def ok_limit_sell(coin, amount, price):
    print(f"OKX limit sell {amount} {coin} at price {price} ...")
    timestamp = str(datetime.utcnow().isoformat("T", "milliseconds")) + "Z"
    method = 'POST'
    request_path = '/api/v5/trade/order'
    # Prepare the body with limit order parameters for selling
    body = json.dumps({
        'instId': f"{coin}-USDT",  # Instrument ID, e.g., BTC-USDT
        'tdMode': 'cash',  # Trading mode, assuming cash here for simplicity
        'side': 'sell',  # Order side for selling
        'ordType': 'limit',  # Order type as limit
        'sz': amount,  # Amount of the coin to sell
        'px': price,  # The limit price at which to sell
    })
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
    print(response.json())
    return response.json()


def ok_limit_buy(api_key, secret_key, passphrase, coin, amount, price):
    print(f"OKX limit buy {amount} {coin} at price {price} ...")
    timestamp = str(datetime.utcnow().isoformat("T", "milliseconds")) + "Z"
    method = 'POST'
    request_path = '/api/v5/trade/order'
    # Prepare the body with limit order parameters for buying
    body = json.dumps({
        'instId': f"{coin}-USDT",  # Instrument ID, e.g., BTC-USDT
        'tdMode': 'cash',  # Trading mode, assuming cash here for simplicity
        'side': 'buy',  # Order side for buying
        'ordType': 'limit',  # Order type as limit
        'sz': amount,  # Amount of the coin to buy
        'px': price,  # The limit price at which to buy
    })
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
    print(response.json())
    return response.json()



if __name__ == '__main__':
    print('OK_api.py is running...')

