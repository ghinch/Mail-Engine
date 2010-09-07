"""
Copyright (c) 2010, Greg Hinch
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

 - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
 - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import os
from django.utils import simplejson

import config
from models import Settings, Message
from forms import SettingsForm

class Admin(webapp.RequestHandler):
	def get(self, form=None):
		current_settings = Settings.get_by_key_name(config.SETTINGS_KEY)
		if current_settings:
			current_settings = current_settings.to_dict()
			current_settings['allowed_ips'] = ','.join(current_settings['allowed_ips'])
		if form is None:
			form = SettingsForm(current_settings)

		self.response.out.write(template.render(os.path.join(config.APP_ROOT_DIR, "templates/index.html"),
								{"no_settings" : (current_settings is None), "form" : form, "title" : "Mail Engine for App Engine"}))

	def post(self):
		args = self.request.arguments()
		post_data = {}
		for arg in args:
			d = self.request.get(arg)
			post_data[arg] = d

		form = SettingsForm(post_data)
		if form.is_valid():
			form.save()

		self.get(form=form)

class MessageList(webapp.RequestHandler):
	def get(self):
		messages = Message.all().order('-datetime')

		results = []
		for message in messages:
			results.append(message.to_dict())

		
		response = {"list" : results, "total" : len(results)}
		json = simplejson.dumps(response)
		self.response.out.write(json)

