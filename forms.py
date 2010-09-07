"""
Copyright (c) 2010, Greg Hinch
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

 - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
 - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

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
