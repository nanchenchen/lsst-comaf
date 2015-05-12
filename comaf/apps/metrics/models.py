from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class OpSimRun(models.Model):
    name = models.CharField(max_length=200)

class Metric(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, unique=True)
    opsim_run = models.ForeignKey(OpSimRun, unique=True)
    opsim_comment = models.TextField(null=True, blank=True, default="")
    opsim_date = models.DateField(null=True)
    maf_comment = models.TextField(null=True, blank=True, default="")
    maf_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def create_from_json(self, json_str):
        pass


class Plot(models.Model):
    metric = models.ForeignKey(Metric, related_name="plots")
    type = models.CharField(max_length=100)
    src = models.ImageField(upload_to='plots')

class Stat(models.Model):
    metric = models.ForeignKey(Metric, related_name="stats")
    type = models.CharField(max_length=100)
    value = models.FloatField()