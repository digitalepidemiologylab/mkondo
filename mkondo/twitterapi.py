import tweepy
from tweepy.parsers import RawParser
import settings
import time

def get_authenticated_api(consumer_token, consumer_secret, access_token, access_token_secret):
	''' Return an authenticated API '''
	auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)
	return api

def get_authenticated_api_raw(consumer_token, consumer_secret, access_token, access_token_secret):
	''' Return an authenticated API '''
	auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth, parser=RawParser)
	return api


class ContinualFetcher():
	def __init__(self, application_log):
		self.error_counter = 0
		self.applog = application_log

	def wait_for_api_capacity(self, api, num_hits):
		''' Wait until the reset time if num_hits is more than the 
		remaining allowable hits.'''

		limit = api.rate_limit_status()

		hits_required = min(limit['hourly_limit'], num_hits)

		if not limit['remaining_hits'] >= hits_required:
			sleep_time = int(limit['reset_time_in_seconds']) - int(time.time()) + 10
			time.sleep(sleep_time)

			#Check once more
			new_limit = api.rate_limit_status()
			if not new_limit['remaining_hits'] >= hits_required:
				self.wait_for_api_capacity(api, num_hits)

	def handle_error_delay(self):
		''' Back off exponentially when an error is encountered. But if 5 or more 
		errors are encountered in a row, raise and exception'''
		BASE_TIME = 60 #seconds

		if self.error_counter >= 5:
			msg = 'Too many errors in a row encountered'
			raise Exception(msg)
		else:
			sleep_time = BASE_TIME * (2.0 ** error_counter)
			time.sleep(sleep_time)

	def handle_rest_errors(self, data_id, exception):
		#If Twitter didn't return quite so many errors, this code wouldn't be ugly
		if exception.response:
			status = exception.response.status
			if status == 404:
				self.applog.info("%s|does_not_exist" % data_id)
				self.applog.info("Tweeter %s does not exist" % data_id)
				return status
			elif status == 401:
				self.applog.info("%s|unauthorized" % data_id)
				return status
			elif status == 500:
				self.applog.exception('error_code:500 Internal server error: something is wrong at Twitter.')
				return status
			elif status == 502:
				self.applog.warning('error_code:502 Twitter is down or being upgraded. Backing off. ')
				self.error_counter += 1
				self.handle_error_delay()
			elif status == 503:
				self.applog.warning('error_code:503 Twitter servers are up, but overloaded. Backing off. ')
				self.error_counter += 1
				self.handle_error_delay()
			elif status == 420:
				self.applog.warning('error_code:420 Rate limited. ')
				time.sleep(1800)
			else:
				self.applog.error('Unanticipated response code received: %d' % status)
				return status
		elif 'nodename nor servname provided' in exception.reason:
			self.applog.warning('DNS reason: %s' % exception.reason)
			self.applog.warning('DNS error received. Looping to try again. ')
		elif '[Errno 54]' in exception.reason:
			self.applog.error('error_code:54 Connection reset by peer')
			self.error_counter += 1
			self.handle_error_delay()
		elif '[Errno 60]' in exception.reason:
			self.applog.error('error_code:60 Connection reset by peer')
			self.error_counter += 1
			self.handle_error_delay()
		elif 'Failed to parse JSON' in exception.reason:
			self.applog.error('Failed to parse JSON for: %s' % data_id)
			self.error_counter += 1
			self.handle_error_delay()
		else:
			self.applog.exception('Unanticipated error. Shutting down.')
			raise exception
