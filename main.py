#from google.appengine.ext.webapp import WSGIApplication
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import config
import sys

# Force sys.path to have our own directory first, so we can import from it.
sys.path.insert(0, config.APP_ROOT_DIR)

from workers import Builder, Dispatcher
from handlers.views import Admin, MessageList
from handlers.api import PostMessage

ROUTES = [
	('/build', Builder),
	('/dispatch', Dispatcher),
	('/post', PostMessage),
	('/messages', MessageList),
	('/', Admin),
]

def main():
	application = webapp.WSGIApplication(ROUTES, debug=config.DEBUG)
	run_wsgi_app(application)

if __name__ == '__main__':
	main()
