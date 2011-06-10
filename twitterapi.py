import tweepy
import settings

def get_authenticated_api(consumer_token, consumer_secret, access_token, access_token_secret):
	''' Return an authenticated API '''
	auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)
	return api
