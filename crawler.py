import oauth2 as oauth
import urlparse
from plurk_oauth import PlurkAPI


OAUTH_REQUEST_TOKEN = 'https://www.plurk.com/OAuth/request_token'
OAUTH_kCCESS_TOKEN = 'https://www.plurk.com/OAuth/access_token'
key = "TYt8Fv77oT5p"
secret = "3lzEavllllxZokBVgaEoBtcJfgZXaG3p"
token = "5Lacy8zM8F3k"
token_secret = "c8UjUr20XuandOzp5gIXMV1AGfc9mPsx" 

def get_request_token(app_key, app_secret):
	consumer = oauth.Consumer(app_key, app_secret)
	client = oauth.Client(consumer)
	response = client.request(OAUTH_REQUEST_TOKEN, method='GET')
	return response

def getPublicProfile(app_key, app_secret, oauth_token, oauth_token_secret):
	apiUrl = 'https://www.plurk.com/APP/Profile/getPublicProfile'
	consumer = oauth.Consumer(app_key, app_secret)
	token = oauth.Token(oauth_token, oauth_token_secret)
	client = oauth.Client(consumer, token)
	response = client.request(apiUrl, method='GET')
	return response

plurk = PlurkAPI(key, secret)
plurk.authorize(token, token_secret)
print(plurk.callAPI('/APP/Timeline/getPlurk', options={'plurk_id': 1394946241}))

# print(get_request_token(key, secret))
# s = get_request_token(key, secret)[1].split("&")
# token = s[0].split("=")[1]
# token_secret = s[1].split("=")[1]
