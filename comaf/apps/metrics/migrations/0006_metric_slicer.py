# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0005_auto_20150601_0202'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='slicer',
            field=models.CharField(default=b'', max_length=128, null=True, blank=True),
            preserve_default=True,
        ),
    ]
