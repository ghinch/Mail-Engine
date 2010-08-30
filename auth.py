import hashlib

from settings import PRIVATE_KEY

def check(token, public):
	compare_token = hashlib.sha1(public + PRIVATE_KEY).hexdigest()
	if compare_token == token:
		return True

	return False
