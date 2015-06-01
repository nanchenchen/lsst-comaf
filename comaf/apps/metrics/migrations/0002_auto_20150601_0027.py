# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import comaf.apps.metrics.models


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpsimRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('comment', models.TextField(default=b'', null=True, blank=True)),
                ('date', models.DateField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='metric',
            name='opsim_comment',
        ),
        migrations.RemoveField(
            model_name='metric',
            name='opsim_date',
        ),
        migrations.AddField(
            model_name='plot',
            name='thumb',
            field=models.ImageField(null=True, upload_to=comaf.apps.metrics.models.get_image_path),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='metric',
            name='opsim_run',
            field=models.ForeignKey(to='metrics.OpsimRun'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='plot',
            name='src',
            field=models.FileField(null=True, upload_to=comaf.apps.metrics.models.get_image_path),
            preserve_default=True,
        ),
    ]
