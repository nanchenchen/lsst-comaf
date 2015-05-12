# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('opsim_run', models.CharField(max_length=200)),
                ('opsim_comment', models.TextField(default=b'', null=True, blank=True)),
                ('opsim_date', models.DateField(null=True)),
                ('maf_comment', models.TextField(default=b'', null=True, blank=True)),
                ('maf_date', models.DateField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Plot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100)),
                ('src', models.ImageField(upload_to=b'plots')),
                ('metric', models.ForeignKey(related_name='plots', to='metrics.Metric')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100)),
                ('value', models.FloatField()),
                ('metric', models.ForeignKey(related_name='stats', to='metrics.Metric')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
