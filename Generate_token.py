import secrets

def generate_token():
    return secrets.token_urlsafe(16)  # Generates a 16-byte (128-bit) token

if __name__ == "__main__":
    token = generate_token()
    print("Your token is:", token)
