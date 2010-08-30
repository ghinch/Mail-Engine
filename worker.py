from google.appengine.ext import webapp
from google.appengine.ext import db

from mailer import Message

import logging

import main
from settings import DEFAULT_SENDER, DEFAULT_SUBJECT

SENDER = 'sender'
SUBJECT = 'subject'
BODY = 'body'
RECIPIENTS = 'recipients'
COMMA = ','

class Worker(webapp.RequestHandler):
	def post(self):
		logging.debug("worker started")
		sender = self.request.get(SENDER)
		if not sender:
			sender = DEFAULT_SENDER

		subject = self.request.get(SUBJECT)
		if not subject:
			subject = DEFAULT_SUBJECT

		body = self.request.get(BODY)

		recipients = self.request.get(RECIPIENTS)
		if recipients:
			recipients = recipients.split(COMMA)
		else:
			recipients = []

		m = Message(recipients=recipients,
					subject=subject,
					body=body)
		m.put()
		m.send()

if __name__ == '__main__':
	main.main()
