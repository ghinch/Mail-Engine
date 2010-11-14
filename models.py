"""
Copyright (c) 2010, Greg Hinch
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

 - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
 - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

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
import hashlib
import random

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
	default_sender = db.StringProperty()
	default_subject = db.StringProperty()

	@classmethod
	def reset_auth(self, key):
		rn = random.random()
		today = datetime.datetime.today()
		hash = hashlib.sha1(str(rn) + today.isoformat()).hexdigest()

		settings = Settings.get_or_insert(key_name=key, auth_key=hash)
		return settings
