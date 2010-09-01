from google.appengine.ext import webapp
from google.appengine.ext import db

try:
	from google.appengine.api.labs import taskqueue
except ImportError:
	from google.appengine.api import taskqueue # for official inclusion of taskqueue.

import auth
from settings import DEFAULT_SENDER, DEFAULT_SUBJECT

import urllib
import hashlib
import logging

TOKEN = 'token'
RECIPIENT = 'recipient'

SENDER = 'sender'
SUBJECT = 'subject'
BODY = 'body'
POST = 'POST'
MAILQUEUE = 'mailqueue'

class Message(db.Model):
	recipients = db.StringListProperty(required=True)
	sender = db.StringProperty(required=True, default=DEFAULT_SENDER)
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
			q = taskqueue.Queue(MAILQUEUE)
			logging.debug('sending message')
			t = taskqueue.Task(url='/dispatch', method=POST, params=params)
			q.add(t)
			
		self.sent = True
		db.put(self)
	
class Mailbox(webapp.RequestHandler):
	def get(self):
		return

	def post(self):
		args = self.request.arguments()
		args.sort()
		params = {}
		for arg in args:
			params[arg] = self.request.get(arg)

		token = self.request.headers['Mail-Engine-Auth-Token']

		if auth.check(token, urllib.urlencode(params), self.request.remote_addr):
			logging.debug('adding message to queue')
			taskqueue.add(url='/mailbox', method=POST, params=params)
		else:
			logging.debug('fail')
