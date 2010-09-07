import os
import logging

from google.appengine.dist import use_library
use_library('django', '1.1')

APP_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
SETTINGS_KEY = os.environ['CURRENT_VERSION_ID'].split('.')[0]

# If we're debugging, turn the cache off, etc.
# Set to true if we want to have our webapp print stack traces, etc
DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Dev')
logging.info("Starting application in DEBUG mode: %s", DEBUG)
