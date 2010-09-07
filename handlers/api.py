from google.appengine.ext import webapp

from utils import auth, tasks

import urllib
import hashlib

POST = 'POST'
	
class PostMessage(webapp.RequestHandler):
	def post(self):
		args = self.request.arguments()
		args.sort()
		params = {}
		for arg in args:
			params[arg] = self.request.get(arg)

		try:
			token = self.request.headers['Mail-Engine-Auth-Token']
		except:
			token = ''

		if auth.check(token, urllib.urlencode(params), self.request.remote_addr):
			tasks.add('/build', params=params)
