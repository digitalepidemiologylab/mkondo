#!/usr/bin/env python 

import tweepy
import logging.handlers
import logging
from tweepy.utils import import_simplejson
json = import_simplejson()

class LoggingConfig:
	""" Configures a data logger and an application logger. The data logger writes 
	out data to a log file. The application logger writes out application events (errors). """
	DATA_LOG = 'DataLogger'
	APP_LOG = 'AppLogger'
	FORMAT = '%(asctime)s%(msecs)d|%(message)s'
	DATE_FORMAT = '%Y%m%d%H%M%S'

	@staticmethod
	def configure_data_logging(data_log_name):
		''' This configures the logger we use to write out data. '''
		data_logger = logging.getLogger(LoggingConfig.DATA_LOG)
		data_logger.setLevel(logging.INFO)

		data_handler = logging.handlers.TimedRotatingFileHandler(data_log_name, 'H', 1)
		data_handler.setFormatter(logging.Formatter(LoggingConfig.FORMAT, datefmt=LoggingConfig.DATE_FORMAT))
		data_logger.addHandler(data_handler)
	
	@staticmethod
	def configure_app_logging(app_log_name):
		''' This configures the logger we use to write out application information '''
		logger = logging.getLogger(LoggingConfig.APP_LOG)
		logger.setLevel(logging.INFO)
		
		#Rotate the application log, once at midnight
		logging_handler = logging.handlers.TimedRotatingFileHandler(app_log_name, 'midnight', 1)
		logging_handler.setFormatter(logging.Formatter(LoggingConfig.FORMAT, datefmt=LoggingConfig.DATE_FORMAT))
		logger.addHandler(logging_handler)

class TweetProcessor:
	""" This class writes the JSON for each tweet to the data_log"""
	@staticmethod
	def parse_json_for_tweet(data):
		data_logger = logging.getLogger(LoggingConfig.DATA_LOG)
		data_logger.info(data)

class TwitterStreamListener(tweepy.StreamListener):
	""" This class listens to a twitter stream and processes each tweet received. It logs errors 
	when necessary."""

	def __init__(self, data_log_name, app_log_name):
		LoggingConfig.configure_data_logging(data_log_name)
		LoggingConfig.configure_app_logging(app_log_name)

	def on_data(self, data):
		logger = logging.getLogger(LoggingConfig.APP_LOG)
		if data is not None:
			if 'in_reply_to_status_id' in data:
				TweetProcessor.parse_json_for_tweet(data)
			elif 'delete' in data:
				logger.info("DELETE: %s" % data)
			elif 'scrub_geo' in data:
				logger.info("SCRUB: %s " % data)		
			elif 'limit' in data:
				limit = json.loads(data)['limit']['track']
				logger.warning('LIMIT: %s' % limit)
		return True

	def on_error(self, status_code):
		logger = logging.getLogger(LoggingConfig.APP_LOG)
		logger.error('An error has occured. Status code: %s' % status_code)
		return True #Keep the stream connection alive.

	def on_timeout(self):
		logger = logging.getLogger(LoggingConfig.APP_LOG)
		logger.error('A timeout has occured')

	def data_log_name(self):
		return LoggingConfig.DATA_LOG

	def app_log_name(self):
		return LoggingConfig.APP_LOG
