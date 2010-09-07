"""
Copyright (c) 2010, Greg Hinch
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

 - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
 - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

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
