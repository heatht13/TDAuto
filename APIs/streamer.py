from api_calls import get_user_principals
from generate_tokens import generate_access_token_from_refresh
from credentials import refresh_token, consumer_key, path
from accesstoken import access_token
from urllib import parse

#LOOK INTO 'qoslevel' parameter to change quality of stream
#can be changed within connection using 'QOS' command in '5.6 QOS Request' TD API
#could be potential function argument/added feature in future

def streamer(access_token):
    user_principals = get_user_principals(access_token)
    user_principals_text = user_principals.text
    user_principals_json = user_principals.json()
    #print(user_principals_text)

    streamer_login(user_principals_json)
    #do things
    streamer_logout(user_principals_json)
    return

def streamer_login(principals):
    '''streamer function to open streamer connection and start data stream.
            Arguments: a user_principals object returned from "get_user_principals" API call
    '''
    credentials = {
        "userid": principals['accounts'][0]['accountId'],
        "company": principals['accounts'][0]['company'],
        "segment": principals['accounts'][0]['segment'],
        "cddomain": principals['accounts'][0]['accountCdDomainId'],
        "usergroup": principals['streamerInfo']['userGroup'],
        "accesslevel": principals['streamerInfo']['accessLevel'],
        "authorized": "Y",
        "acl": principals['streamerInfo']['acl'],
        #"timestamp": tokenTimeStampAsMs, ##NEEDS DONE
        "appid": principals['streamerInfo']['appId'],
    }

    request = {
        "requests": [
                {
                    "service": "ADMIN",
                    "command": "LOGIN",
                    #"requestid": 0,
                    "parameters": {
                        "account": principals['accounts'][0]['accountId'],
                        "source": principals['streamerInfo']['appId'],
                        "token": principals['streamerInfo']['token'],
                        "version": "1.0",
                        "credential": parse.quote(credentials),
                        "qoslevel": 2
                    }
                }
        ]
    }

    #socket.send(request)
    return

def streamer_logout(principals):
    '''streamer function to close streamer connection and end data stream.
            Arguments: a user_principals object returned from "get_user_principals" API call
    '''
    {
        "requests": [
            {
                "service": "ADMIN", 
                "requestid": "1", 
                "command": "LOGOUT", 
                "account": principals['accounts'][0]['accountId'], 
                "source": principals['streamerInfo']['appId'], 
                "parameters": { }
            }
        ]
    }
    return