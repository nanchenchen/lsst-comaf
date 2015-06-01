# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import comaf.apps.base.utils.overwrite_storage
import comaf.apps.metrics.models


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0006_metric_slicer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plot',
            name='src',
            field=models.FileField(storage=comaf.apps.base.utils.overwrite_storage.OverwriteStorage(), max_length=1024, null=True, upload_to=comaf.apps.metrics.models.get_image_path),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='plot',
            name='thumb',
            field=models.ImageField(storage=comaf.apps.base.utils.overwrite_storage.OverwriteStorage(), max_length=1024, null=True, upload_to=comaf.apps.metrics.models.get_image_path),
            preserve_default=True,
        ),
    ]
