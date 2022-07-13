from datetime import datetime, timezone
##import time
##from TD_API_CLASS.TD_API import TD_API
from os import access
import APIs.api_calls as api
import PersonalTesting.credentials as credentials
from access import access_token
from urllib.parse import urlencode
import websockets
import asyncio
import json
import traceback

##token = generate_refresh_token(refresh_token, consumer_key, path)
##print()
##print(datetime.now())
##print(datetime.utcfromtimestamp(datetime.now()))
##print(datetime.fromtimestamp(time.time()))

#################################
##WORKS!!
##client = TD_API()
##client.print_credentials()
##help(TD_API.generate_access_token_from_refresh)
##client.generate_access_token_from_refresh()
##print(client.get_user_principals())
#####################
##api.generate_access_token_from_refresh(credentials.refresh_token, credentials.consumer_key)


# logout = {
#     "requests": [
#         {
#             "service": "ADMIN",
#             "command": "LOGOUT",
#             "requestid": "2",
#             "account": users['accounts'][0]['accountId'],
#             "source": users['streamerInfo']['appId'],
#             "parameters": {}
#         }
#     ]
# }

# actives = {
#     "requests": [
#         {
#             "service": "ACTIVES_NASDAQ", 
#             "requestid": "3", 
#             "command": "SUBS", 
#             "account": users['accounts'][0]['accountId'], 
#             "source": users['streamerInfo']['appId'], 
#             "parameters": {
#                 "keys": "NASDAQ-60", 
#                 "fields": "0,1"
#             }
#         }
#     ]

# }
async def socket(login, actives):
    uri = 'wss://' + users['streamerInfo']['streamerSocketUrl'] + '/ws'
    websocket = await websockets.connect(uri)
    try:
        await websocket.send(json.dumps(login))
        response = await websocket.recv()
        print(response)
    except websockets.exceptions.ConnectionClosed:
        print("closed")
    return response
        

if __name__ == '__main__':
    ##api.generate_access_token_from_refresh(credentials.refresh_token, credentials.consumer_key)
    users = api.get_user_principals(access_token)
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
    asyncio.run(socket(login, actives))