from Top_functions import *


def create_gateio_signature(secret_key, query_string):
    return hmac.new(secret_key.encode(), query_string.encode(), hashlib.sha512).hexdigest()

def withdraw_gateio(api_key, secret_key, currency, amount, address):
    url = "https://api.gate.io/api2/1/private/withdraw"

    payload = {
        'currency': currency,
        'amount': str(amount),
        'address': address
    }

    # Gate.io uses a nonce for added security
    payload['nonce'] = int(time.time() * 1000)

    # Create the query string
    query_string = '&'.join([f"{key}={value}" for key, value in payload.items()])

    # Create the signature
    signature = create_gateio_signature(secret_key, query_string)

    headers = {
        'KEY': api_key,
        'SIGN': signature,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, headers=headers, data=query_string)

    return response.json()

# Usage example
api_key = 'YOUR_API_KEY'
secret_key = 'YOUR_SECRET'
currency = 'BTC'  # Example: BTC
amount = 0.01  # Example: 0.01 BTC
address = 'YOUR_WALLET_ADDRESS'  # Destination wallet address

if __name__ == '__main__':
    print('Gate_api.py is running...')
    response = withdraw_gateio(api_key, secret_key, currency, amount, address)
    print(response)
