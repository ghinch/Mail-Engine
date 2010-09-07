from google.appengine.ext import db

SENDER = 'sender'
SUBJECT = 'subject'
BODY = 'body'
RECIPIENT = 'recipient'
MAILQUEUE = 'mailqueue'
ES = ''

from utils import tasks

import datetime
import time

SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)

class BaseModel(db.Model):
	def to_dict(self):
		output = {}

		for key, prop in self.properties().iteritems():
			value = getattr(self, key)

			if value is None or isinstance(value, SIMPLE_TYPES):
				output[key] = value
			elif isinstance(value, datetime.date):
				# Convert date/datetime to ms-since-epoch ("new Date()").
				ms = time.mktime(value.utctimetuple()) * 1000
				ms += getattr(value, 'microseconds', 0) / 1000
				output[key] = int(ms)
			elif isinstance(value, db.Model):
				output[key] = value.to_dict()
			else:
				raise ValueError('cannot encode ' + repr(prop))

		return output

class Message(BaseModel):
	recipients = db.StringListProperty(required=True)
	sender = db.StringProperty(required=True)
	subject = db.StringProperty(required=True)
	body = db.TextProperty(required=True)
	datetime = db.DateTimeProperty(auto_now_add=True)
	sent = db.BooleanProperty(default=False)

	def send(self):
		recipients = self.recipients
		params = {
			SUBJECT : self.subject,
			BODY : self.body,
			SENDER : self.sender
		}
		for addr in recipients:
			params[RECIPIENT] = addr
			tasks.add('/dispatch', params, MAILQUEUE)
			
		self.sent = True
		db.put(self)

class Settings(BaseModel):
	auth_key= db.StringProperty(required=True, default=ES)
	allowed_ips = db.StringListProperty()
	default_sender = db.StringProperty(required=True, default=ES)
	default_subject = db.StringProperty(required=True, default=ES)
