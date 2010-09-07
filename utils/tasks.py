try:
	from google.appengine.api.labs import taskqueue
except ImportError:
	from google.appengine.api import taskqueue # for official inclusion of taskqueue.

POST = 'post'

def add (url, params, queue='default'):
	q = taskqueue.Queue(queue)
	t = taskqueue.Task(url=url, method=POST, params=params)
	q.add(t)
