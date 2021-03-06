import requests
from urllib.parse import urlencode
import websockets
import asyncio
import json

def get_user_principals(token):
    resource = 'https://api.tdameritrade.com/v1/userprincipals'
    header = {'Authorization': f'Bearer {token}'}
    payload = {'fields' : "streamerSubscriptionKeys,streamerConnectionInfo"}
    response = requests.get(resource, headers = header, params = payload)
    return response.json()

def get_accounts(token):
    resource = f"https://api.tdameritrade.com/v1/accounts"
    header = {'Authorization': f'Bearer {token}'}
    return requests.get(resource, headers = header)

def generate_access_token_from_refresh(token, consumer):
        """Generates an access token using a refresh token (used most often)
            Arguments:
                refresh_token: A valid, non-expired refresh token. If not possessed, please generate one using generate_from_auth_code()"""
        import requests
        from datetime import datetime, timezone
        resource = r"https://api.tdameritrade.com/v1/oauth2/token"
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        payload = {
            'grant_type':'refresh_token',
            'refresh_token': token,
            'client_id': consumer,
        }
        request = requests.post(resource, headers = headers, data = payload)
        json = request.json()
        file = open('./access.py', 'w')
        file.write(f"access_token = '{json['access_token']}'\n")
        file.write(f"expiration = '{datetime.utcfromtimestamp(datetime.replace(datetime.now(),tzinfo=timezone.utc).timestamp() + int(json['expires_in']))}'")
        file.close()
        return json['access_token']

async def socket(users, login):
    uri = 'wss://' + users['streamerInfo']['streamerSocketUrl'] + '/ws'
    websocket = await websockets.connect(uri)
    try:
        await websocket.send(json.dumps(login))
        response = await websocket.recv()
        print(response)
    except websockets.exceptions.ConnectionClosed:
        print("closed")
    return response
    
def streamer_login(users, socket):
    '''streamer function to open streamer connection and start data stream.
            Arguments: a user_principals object returned from "get_user_principals" API call
    '''
    from datetime import datetime
    from urllib.parse import urlencode
    import websockets
    import asyncio
    import json

    credential = {
        "userid": users['accounts'][0]['accountId'],
        "token": users['streamerInfo']['token'],
        "company": users['accounts'][0]['company'],
        "segment": users['accounts'][0]['segment'],
        "cddomain": users['accounts'][0]['accountCdDomainId'],
        "usergroup": users['streamerInfo']['userGroup'],
        "accesslevel": users['streamerInfo']['accessLevel'],
        "authorized": "Y",
        "timestamp": str(datetime.strptime(users['streamerInfo']['tokenTimestamp'], "%Y-%m-%dT%H:%M:%S%z").timestamp()*1000),
        "appid": users['streamerInfo']['appId'],
        "acl": users['streamerInfo']['acl']
    }

    login = {
        "requests": [
            {
                "service": "ADMIN",
                "requestid": "1",
                "command": "LOGIN",
                "account": users['accounts'][0]['accountId'],
                "source": users['streamerInfo']['appId'],
                "parameters": {
                    "credential": urlencode(credential),
                    "token": users['streamerInfo']['token'],
                    "version": "1.0"
                }
            }
        ]
    }
    
    actives = {
        "requests": [
            {
                "service": "ACTIVES_NASDAQ", 
                "requestid": "3", 
                "command": "SUBS", 
                "account": users['accounts'][0]['accountId'], 
                "source": users['streamerInfo']['appId'], 
                "parameters": {
                    "keys": "NASDAQ-60", 
                    "fields": "0,1"
                }
            }
        ]
    }

    asyncio.run(socket(users, login))
    return