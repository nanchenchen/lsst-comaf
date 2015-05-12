from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import json
# Create your models here.



class Metric(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User)
    opsim_run = models.CharField(max_length=200)
    opsim_comment = models.TextField(null=True, blank=True, default="")
    opsim_date = models.DateField(null=True)
    maf_comment = models.TextField(null=True, blank=True, default="")
    maf_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.name + " / " + self.opsim_run


class Plot(models.Model):
    metric = models.ForeignKey(Metric, related_name="plots")
    type = models.CharField(max_length=100)
    src = models.ImageField(upload_to='plots')

class Stat(models.Model):
    metric = models.ForeignKey(Metric, related_name="stats")
    type = models.CharField(max_length=100)
    value = models.FloatField()


def create_from_post(user_key, data):
    metric = Metric()
    metric.name = data['name']
    # TODO: handle failure
    metric.owner = User.objects.get(key__value=user_key)
    metric.opsim_run = data['opsim_run']
    if data.get('opsim_comment'):
        metric.opsim_comment = data['opsim_comment']
    if data.get('opsim_date'):
        metric.opsim_comment = data['opsim_date']
    if data.get('maf_comment'):
        metric.opsim_comment = data['maf_comment']
    if data.get('maf_date'):
        metric.opsim_comment = data['maf_date']
    metric.save()
