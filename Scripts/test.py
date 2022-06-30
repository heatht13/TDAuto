from credentials import refresh_token, consumer_key, path
from generate_tokens import generate_refresh_token
from datetime import datetime, timezone
import time
from TD_API import TD_API

##token = generate_refresh_token(refresh_token, consumer_key, path)
##print()
##print(datetime.now())
##print(datetime.utcfromtimestamp(datetime.now()))
##print(datetime.fromtimestamp(time.time()))
##print(datetime.utcfromtimestamp(1664051000))
##print(datetime.replace(datetime.now(),tzinfo=timezone.utc))
##json = {}
##json['expires_in'] = "1800"
##new = datetime.replace(datetime.now(),tzinfo=timezone.utc).timestamp() + 7776000
##new = datetime.utcfromtimestamp(new)
##print(new)
##print(datetime.utcfromtimestamp(0))

#################################
##WORKS!!
##client = TD_API()
##client.print_credentials()
##help(TD_API.generate_access_token_from_refresh)

#####################
