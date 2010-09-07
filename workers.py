from google.appengine.api import mail
from google.appengine.ext import webapp

from models import Message, Settings
import config

SENDER = 'sender'
SUBJECT = 'subject'
BODY = 'body'
RECIPIENT = 'recipient'
RECIPIENTS = RECIPIENT + 's'
COMMA = ','

class Dispatcher(webapp.RequestHandler):
	def post(self):
		message = mail.EmailMessage(sender=self.request.get(SENDER),
									subject=self.request.get(SUBJECT),
									body=self.request.get(BODY),
									to=self.request.get(RECIPIENT))
		message.send()

class Builder(webapp.RequestHandler):
	def post(self):
		settings = Settings.get_by_key_name(config.SETTINGS_KEY)

		sender = self.request.get(SENDER, settings.default_sender)
		subject = self.request.get(SUBJECT, settings.default_subject)
		body = self.request.get(BODY, '')

		recipients = self.request.get(RECIPIENTS)
		if recipients:
			recipients = recipients.split(COMMA)
		else:
			recipients = []

		m = Message(recipients=recipients,
					sender=sender,
					subject=subject,
					body=body)
		m.put()
		m.send()
