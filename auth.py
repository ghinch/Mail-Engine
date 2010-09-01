import hashlib

import logging

from settings import PRIVATE_KEY

try:
	from settings import ALLOWED_IP_ADDRESSES
except:
	logging.debug('no ip addresses to check against')
	ALLOWED_IP_ADDRESSES = None

def check(token, public, remote_addr):
	authorized = False
	compare_token = hashlib.sha1(public + PRIVATE_KEY).hexdigest()
	if compare_token == token:
		logging.debug('tokens match')
		authorized = True
	
	if ALLOWED_IP_ADDRESSES and remote_addr not in ALLOWED_IP_ADDRESSES:
		logging.debug('remote address not in list')
		authorized = False

	return authorized
