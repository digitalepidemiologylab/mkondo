import tweepy

import logging
import httplib
from socket import timeout
from socket import error as socket_error
from time import sleep

class CompliantStream(tweepy.Stream):
	''' This class extends Tweepy's Stream class by adding HTTP and TCP/IP back-off 
	(according to Twitter's guidelines). '''
	DEBUG_LOG = 'Stream'

	def enable_debug(self, stream_log_name):
		#Set up some logging for debugging
		logger = logging.getLogger(CompliantStream.DEBUG_LOG)
		logger.setLevel(logging.DEBUG)

		handler = logging.handlers.TimedRotatingFileHandler(stream_log_name, 'midnight', 1)
		handler.setFormatter(logging.Formatter('%(asctime)s%(msecs)d|%(message)s', datefmt='%Y%m%d%H%M%S'))

		logger.addHandler(handler)


	def __init__(self, auth, listener, retry_count, min_http_delay=10, max_http_delay=240, min_tcp_ip_delay=0.5, max_tcp_ip_delay=16, stream_log_name='stream.log', **options):
		self.min_http_delay = min_http_delay
		self.max_http_delay = max_http_delay
		self.min_tcp_ip_delay = min_tcp_ip_delay
		self.max_tcp_ip_delay = max_tcp_ip_delay
		self.running = False
		self.retry_count = retry_count
		self.auth = auth

		self.enable_debug(stream_log_name)

		#Twitter sends a keep-alive every twitter_keepalive seconds
		self.twitter_keepalive = 30

		#Add a couple seconds more wait time. 
		self.twitter_keepalive += 2.0

		tweepy.Stream.__init__(self, auth, listener, secure=True, **options)
	
	def _run(self):
		url = "%s://%s%s" % (self.scheme, self.host, self.url)
		self.auth.apply_auth(url, 'POST', self.headers, self.parameters)

		logger = logging.getLogger(CompliantStream.DEBUG_LOG)

        # Connect and process the stream
		error_counter = 0
		conn = None
		exception = None
		while self.running:
			logger.debug('Loop. Error count: %s' % error_counter)
			if self.retry_count and error_counter > self.retry_count:
				# quit if error count greater than retry count
				break
			try:
				if self.scheme == "http":
					conn = httplib.HTTPConnection(self.host)
				else:
 					conn = httplib.HTTPSConnection(self.host)
				conn.connect()
				conn.sock.settimeout(self.twitter_keepalive)
				conn.request('POST', self.url, self.body, headers=self.headers)
				resp = conn.getresponse()
				logger.debug("Response status: %s " % resp.status)
				if resp.status != 200:
					if self.listener.on_error(resp.status) is False:
						break
					error_counter += 1
					#HTTP delay is based on error count, since we have exponential back-off
					http_delay = self.get_http_delay(error_counter)
					logger.debug('HTTP Delay. Sleeping for: %s' % http_delay)
					sleep(http_delay)
				else:
					error_counter = 0
					http_delay = 0
					tcp_ip_delay = 0
					self._read_loop(resp)
			except (timeout, socket_error):
				logger.exception('Socket timeout or socket error.')
				if self.listener.on_timeout() == False:
					break
				if self.running is False:
					break
				conn.close()
				error_counter += 1
				tcp_ip_delay = self.get_tcp_ip_delay(error_counter)
				logger.error('TCP/IP Delay. Sleeping for: %s' % tcp_ip_delay)
				sleep(tcp_ip_delay)
			except httplib.IncompleteRead:
				logger.exception('Incomplete Read.')

				#We assume there are connection issues at the other end, so we'll 
				#try again in a little bit. 
				error_counter += 1
				#HTTP delay is based on error count, since we have exponential back-off
				http_delay = self.get_http_delay(error_counter)
				logger.debug('HTTP Delay. Sleeping for: %s' % tcp_ip_delay)
				sleep(http_delay)

			except Exception, exception:
				logger.exception('Unexpected exception: %s' % exception)
				# any other exception is fatal, so kill loop
				break

		# cleanup
		self.running = False
		if conn:
			conn.close()

		if exception:
			raise 

	def get_http_delay(self, error_count):
			''' Exponential back-off, based on the number of times we've failed (error_count) '''
			delay = self.min_http_delay * (2.0 ** error_count)
			if delay > self.max_http_delay:
				return self.max_http_delay
			return delay

	def get_tcp_ip_delay(self, error_count):
		''' Linear back-off, based on the number of times we've failed (error_count) '''
		delay = float(self.min_tcp_ip_delay * error_count)
		if delay > self.max_tcp_ip_delay:
			return self.max_tcp_ip_delay
		return delay
