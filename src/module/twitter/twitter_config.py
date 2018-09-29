from requests_oauthlib import OAuth1Session

CONSUMER_KEY = "change_it"
CONSUMER_SECRET = "change_it"
ACCESS_TOKEN = "change_it"
ACCESS_TOKEN_SECRET = "change_it"

twitter_api = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
