from google.appengine.ext.webapp import WSGIApplication
from google.appengine.ext.webapp.util import run_wsgi_app

from worker import Worker
from mailer import Mailbox
from dispatch import Dispatch

application = WSGIApplication([
	('/mailbox', Worker),
	('/dispatch', Dispatch),
	('/', Mailbox),
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
