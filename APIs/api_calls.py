import requests

def get_user_principals(token):
    resource = 'https://api.tdameritrade.com/v1/userprincipals'
    header = {'Authorization': f'Bearer {token}'}
    payload = {'fields' : 'streamerSubscriptionKeys, streamerConnectionInfo'}
    return requests.get(resource, headers = header, params = payload)

def get_accounts(token):
    resource = f"https://api.tdameritrade.com/v1/accounts"
    header = {'Authorization': f'Bearer {token}'}
    return requests.get(resource, headers = header)