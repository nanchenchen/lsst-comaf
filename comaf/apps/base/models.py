from django.db import models
from django.contrib.auth.models import User
import hashlib
from time import gmtime, strftime



def create_user(name, email):
    user = User()
    user.username = name
    user.email = email
    user.is_staff = False
    user.save()
    key = UserKey(user=user, key=generate_new_key(name))
    key.save()


def generate_new_key(name):
    time_str = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return hashlib.sha224(name + time_str).hexdigest()
# Create your models here.
class UserKey(models.Model):
    """
    Key for uploading models
    """
    user = models.ForeignKey(User, related_name="key", unique=True)
    value = models.TextField(default="")

    def __unicode__(self):
        return self.user.username + "/ " + self.value

