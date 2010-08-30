from google.appengine.api import mail
from google.appengine.ext import webapp

import main
import logging

SENDER = 'sender'
SUBJECT = 'subject'
BODY = 'body'
RECIPIENT = 'recipient'

class Dispatch(webapp.RequestHandler):
	def post(self):
		message = mail.EmailMessage(sender=self.request.get(SENDER),
									subject=self.request.get(SUBJECT),
									body=self.request.get(BODY),
									to=self.request.get(RECIPIENT))
		logging.debug('sending')
		message.send()

if __name__ == '__main__':
	main.main()
