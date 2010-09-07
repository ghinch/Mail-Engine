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

