class TD_API: 
    """A library to target TD Ameritrade's APIs. This library uses OAuth 2.0 Authentication to provide user account information, near real-time market data streaming, and place trades. A TD Ameritrade account is required for the usage of this library."""

    __instance_id = 0

    @classmethod
    def get_instance_id(cls):
        return cls.__instance_id

    def __init__(self, user_id = None, consumer_key = None, refresh_token = None, refresh_token_exp = None) :
        """An instance of the TD_API class
                - Arguments:
                    - user_id: Account number to execute trades with
                    - consumer_key: Consumer Key associated with TD app used to target TD Ameritrade's APIs
                    - refresh_token: Token used to generate access token for use in API fetching.
                    - refresh_token_exp: Date in 'YYYY-MM-DD HH:MM:SS' format indicating refresh token's expiration"""
        
        from datetime import datetime
        import credentials
        if(user_id):
            self.user_id = user_id
        else:
            self.user_id = credentials.user_id
        if(consumer_key):
            self.consumer_key = consumer_key
        else:
            self.consumer_key = credentials.consumer_key
        if(refresh_token):
            self.refresh_token = refresh_token
            self.refresh_token = datetime.strptime(refresh_token_exp, "%y-%m-%d H:M:S")
        else:
            self.refresh_token = credentials.refresh_token
            self.refresh_token_expiration = datetime.utcfromtimestamp(1664051000)
        self.access_token = ''
        self.access_token_expiration = datetime.utcfromtimestamp(0)
        self.token_type = ''
        self.scope = ''
        TD_API.__instance_id += 1
        self.id = TD_API.__instance_id
    
    def __str__(self) :
        return f"User ID: {self.user_id} Consumer Key: {self.consumer_key} Refresh Exp: {self.refresh_token_expiration}"
    
    def print_credentials(self):
        print(self.__str__())

    def generate_from_auth_code(self, auth_code, path='/refresh_token.txt'):
        """Generates both refresh and access tokens using an authorization code (one time, shouldn't be used ever again for lvl1 app)
                - Arguments: 
                    - auth_code: Authorization Code produced when authenticating for the first time. Use td_authorization script
                    - path: Path to store refresh token for future token generation. Default is current open directory"""
        import requests
        from datetime import datetime, timezone
        resource = r"https://api.tdameritrade.com/v1/oauth2/token"
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        payload = {
            'grant_type':'authorization_code',
            'access_type':'offline',
            'code': auth_code,
            'client_id': self.consumer_key,
            'redirect_uri': "http://localhost"
        }
        request = requests.post(resource, headers = headers, data = payload)
        json = request.json()
        self.access_token = json['access_token']
        self.refresh_token = json['refresh_token']
        self.access_token_expiration = datetime.replace(datetime.now(),tzinfo=timezone.utc).timestamp() + int(json['expires_in'])
        self.refresh_token_expiration = datetime.replace(datetime.now(),tzinfo=timezone.utc).timestamp() + int(json['refresh_token_expires_in'])
        self.token_type = json['token_type']
        self.scope = json['scope']
        file = open(path, 'w')
        file.write(f"refresh_token:'{self.refresh_token}'")
        file.write(f"expiration: {self.refresh_token_expiration}")
        file.close()
        return self.access_token

    def generate_access_token_from_refresh(self, refresh_token = None):
        """Generates an access token using a refresh token (used most often)
            Arguments:
                refresh_token: A valid, non-expired refresh token. If not possessed, please generate one using generate_from_auth_code()"""
        import requests
        from datetime import datetime, timezone
        if(refresh_token):
            refresh = refresh_token
        else:
            refresh = self.refresh_token
        resource = r"https://api.tdameritrade.com/v1/oauth2/token"
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        payload = {
            'grant_type':'refresh_token',
            'refresh_token': refresh,
            'client_id': self.consumer_key,
        }
        request = requests.post(resource, headers = headers, data = payload)
        json = request.json()
        self.access_token = json['access_token']
        self.access_token_expiration = datetime.replace(datetime.now(),tzinfo=timezone.utc).timestamp() + int(json['expires_in'])
        return self.access_token

    def generate_refresh_token(self, path='/refresh_token.txt', refresh_token = None):
        """Generates both refresh and access tokens using an old, nonexpired refresh token (used to renew refresh token every 90 days)
            ***HAS NOT BEEN USED YET***
            - Arguments:
                - path: Path to store new refresh token. Default to current opne directory.
                - refresh_token: A valid, non-expired refresh token. If not possessed please generate one using generate_from_auth_code()"""
        import requests
        from datetime import datetime, timezone
        if(refresh_token):
            refresh = refresh_token
        else:
            refresh = self.refresh_token
        resource = r"https://api.tdameritrade.com/v1/oauth2/token"
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        payload = {
            'grant_type':'refresh_token',
            'refresh_token': refresh,
            'access_type':'offline',
            'client_id': self.consumer_key,
        }
        request = requests.post(resource, headers = headers, data = payload)
        json = request.json()
        self.access_token = json['access_token']
        self.refresh_token = json['refresh_token']
        self.access_token_expiration = datetime.replace(datetime.now(),tzinfo=timezone.utc).timestamp() + int(json['expires_in'])
        self.refresh_token_expiration = datetime.replace(datetime.now(),tzinfo=timezone.utc).timestamp() + int(json['refresh_token_expires_in'])
        self.token_type = json['token_type']
        self.scope = json['scope']
        file = open(path, 'w')
        file.write(f"refresh_token:'{self.refresh_token}'")
        file.write(f"expiration: {self.refresh_token_expiration}")
        file.close()
        return self.access_token