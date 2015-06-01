# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import comaf.apps.metrics.models


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0002_auto_20150601_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plot',
            name='src',
            field=models.FileField(max_length=1024, null=True, upload_to=comaf.apps.metrics.models.get_image_path),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='plot',
            name='thumb',
            field=models.ImageField(max_length=1024, null=True, upload_to=comaf.apps.metrics.models.get_image_path),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='plot',
            name='type',
            field=models.CharField(max_length=128),
            preserve_default=True,
        ),
    ]
