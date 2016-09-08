# mylib.py
from logging import *
import logging.config
import os
import tempfile
import datetime
import getpass

mb_log = os.getenv('MB_LOG_DIR') 

if not mb_log:
	sysTemp = tempfile.gettempdir()
	mb_log = os.path.join(sysTemp, 'mbPipeline') 

if not os.path.exists(mb_log):
	os.makedirs(mb_log) 


def getLoggerPrefix():
	''' 
	return logger file name depending on where the logger gets created from 
 
	''' 
	modules = ['maya', 'nuke'] 
	application = 'main' 

	for mod in modules: 
		try: 
			__import__(mod) 
			application = mod 
			break 
		except ImportError: 
			pass 

	studio = os.getenv('STUDIO', 'no_studio') 
	site = os.getenv('SITE', 'no_site') 
	ctime = datetime.datetime.now().strftime('%Y%m%d') 
	user = getpass.getuser() 

	logfilename = '%s.mbPipeline.%s.%s.%s.%s.' % (ctime, studio, site, user, application) 

	return logfilename 


logfile = tempfile.NamedTemporaryFile( 
	prefix=getLoggerPrefix(), 
	suffix='.log', 
	delete=False, 
	dir=mb_log 
).name 

DEFAULT_LOG_SETTINGS = {
	'version': 1,
	'handlers': {
		'console': {
			'class': 'logging.StreamHandler',
			'level': 'WARNING',
			'formatter': 'default',
			'stream': 'ext://sys.stdout',
		},
		'file': {
			'class': 'logging.handlers.RotatingFileHandler',
			'level': 'DEBUG',
			'formatter': 'file',
			'filename': logfile,
			'mode': 'a',
			'maxBytes': 10485760,
			'backupCount': 5,
		},

	},
	'formatters': {
		'default': {
			'()': 'mb_logging.formatters.ColorFormatter',
			'format': (
				'[%(levelname)s:%(asctime)s]:%(name)s.%(funcName)s()@%(lineno)d - '
				'%(message)s '
			)
		},
		'file': {
			'format': (
				'[%(levelname)s:%(asctime)s]:%(name)s.%(funcName)s()@%(lineno)d - '
				'%(message)s '
			)
		},
		'email': {
			'format': (
				'Timestamp: %(asctime)s\nModule: %(module)s\n'
				'Line: %(lineno)d\nMessage: %(message)s'
			),
		},
	},
	'loggers': {
		'mbPipeline': {
			'level': 'DEBUG',
			'handlers': ['console', 'file'],
			'propagate': False
		},
	}
}


logging.config.dictConfig(DEFAULT_LOG_SETTINGS)
logging.captureWarnings(True)

root_logger = getLogger('mbPipeline') 
 
def getLogger(name='default'):
	if os.getenv('MB_DEBUG', '0') == '1':
		for handler in root_logger.handlers:
			handler.setLevel(DEBUG)
	return logging.getLogger('mbPipeline.%s' % name)

log = getLogger('mb-logger') 
log.warning('Saving log file : %s' % logfile)

#def do_something():
#	logging.info('Doing something')