import re

from django import forms
from django.forms.util import ValidationError
from google.appengine.ext import db

import config
from models import Settings

class SettingsForm (forms.Form):
	auth_key = forms.CharField()
	default_sender = forms.EmailField()
	default_subject = forms.CharField()
	allowed_ips = forms.CharField(required=False, widget=forms.Textarea)

	def clean_allowed_ips(self):
		if self.cleaned_data['allowed_ips'] == '':
			return []

		ipv4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
		data = self.cleaned_data['allowed_ips'].split(',')
		valid = True
		for index, addr in enumerate(data):
			cleaned_addr = addr.strip()

			if not ipv4_re.search(cleaned_addr):
				valid = False

			data[index] = cleaned_addr
		
		if not valid:
			raise ValidationError("Invalid IP address")
		return data

	def save(self):
		d = self.cleaned_data
		def txn():
			settings = Settings(key_name=config.SETTINGS_KEY, 
								auth_key=d['auth_key'],
								default_subject=d['default_subject'],
								default_sender=d['default_sender'],
								allowed_ips=d['allowed_ips'])
			settings.put()
		
		return db.run_in_transaction(txn)
