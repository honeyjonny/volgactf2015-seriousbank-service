from django.utils import timezone
from hashlib import md5

def set_cookie(response, key, value, expire_minutes = 20):
	expires = timezone.now() + timezone.timedelta(minutes=expire_minutes)
	response.set_cookie(key, value, expires=expires)

def gen_password(passfraze):
	m = md5()
	m.update(passfraze)
	key = m.hexdigest()
	return key[:8].encode('ascii'), key[-8:].encode('ascii')

def perform_query(model, query):
	qset = model.objects.raw(query)
	return list(qset)

def validate_permissions(user, username):
	return True if (user.is_authenticated() and user.username == username) else False