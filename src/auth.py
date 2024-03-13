import json
from google.auth.transport.requests import Request
from google.oauth2 import service_account

def authenticate(credentials_path):
    try:
        with open(credentials_path, 'r') as file:
            credentials_data = json.load(file)
            credentials = service_account.Credentials.from_service_account_info(
                credentials_data,
                scopes=['https://www.googleapis.com/auth/analytics']
            )
        credentials.refresh(Request())
        return credentials
    except FileNotFoundError:
        print(f"Error: File not found at {credentials_path}")
