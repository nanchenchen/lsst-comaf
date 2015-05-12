from django.contrib.auth.models import User
import hashlib
from time import gmtime, strftime
from comaf.apps.base.models import UserKey

def create_user(name, email):
    user = User()
    user.username = name
    user.email = email
    user.is_staff = False
    user.save()
    key = UserKey(user=user, value=generate_new_key(name))
    key.save()


def generate_new_key(name):
    time_str = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return hashlib.sha224(name + time_str).hexdigest()