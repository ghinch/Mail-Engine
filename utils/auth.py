import hashlib

import config
from models import Settings

def check(token, public, remote_addr):
	authorized = False
	
	settings = Settings.get_by_key_name(config.SETTINGS_KEY)

	if settings is not None:
		compare_token = hashlib.sha1(public + settings.auth_key).hexdigest()
		if compare_token == token:
			authorized = True
		
		if settings.allowed_ips and remote_addr not in settings.allowed_ips:
			authorized = False

	return authorized
