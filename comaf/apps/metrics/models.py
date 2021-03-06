from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import json
import os
from comaf.apps.base.utils.overwrite_storage import OverwriteStorage
from django.core.urlresolvers import reverse

# Create your models here.


class OpsimRun(models.Model):
    name = models.CharField(max_length=200)
    comment = models.TextField(null=True, blank=True, default="")
    date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    def __unicode__(self):
        return self.name


class Metric(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User)
    opsim_run = models.ForeignKey(OpsimRun)
    metadata = models.TextField(null=True, blank=True, default="")
    slicer = models.CharField(max_length=128, null=True, blank=True, default="")
    display_group = models.TextField(null=True, blank=True, default="")
    display_subgroup = models.TextField(null=True, blank=True, default="")
    display_order = models.IntegerField(null=True)
    display_caption = models.TextField(null=True, blank=True, default="")
    maf_comment = models.TextField(null=True, blank=True, default="")
    maf_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.owner.username + "/" + self.name + " / " + self.opsim_run.name

    def get_absolute_url(self):
        """What is the main url for this object"""
        return reverse('project', kwargs={
            'pk': self.pk,
        })

    def get_plots_in_order(self):
        plots = []
        skymap = self.plots.get(type='Skymap')
        if skymap:
            plots.append(skymap)
        histogram = self.plots.get(type='Histogram')
        if histogram:
            plots.append(histogram)
        query = self.plots.exclude(type='Skymap')
        query = query.exclude(type='Histogram')
        plots.extend(query.all())
        return plots


def get_image_path(instance, filename):
    return os.path.join('plots', filename)


class Plot(models.Model):
    metric = models.ForeignKey(Metric, related_name="plots")
    type = models.CharField(max_length=128)
    src = models.FileField(upload_to=get_image_path, null=True, max_length=1024, storage=OverwriteStorage())
    thumb = models.ImageField(upload_to=get_image_path, null=True, max_length=1024, storage=OverwriteStorage())
    ordering = ['type']
    def __unicode__(self):
        return self.src.name




class Stat(models.Model):
    metric = models.ForeignKey(Metric, related_name="stats")
    type = models.CharField(max_length=100)
    value = models.FloatField()


class Comment(models.Model):
    metric = models.ForeignKey(Metric, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    owner = models.ForeignKey(User)
    text = models.TextField(null=True, blank=True, default="")


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
