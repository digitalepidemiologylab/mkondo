import logging.handlers
import logging

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
