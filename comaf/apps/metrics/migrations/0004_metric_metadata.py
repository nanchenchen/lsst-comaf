# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0003_auto_20150601_0129'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='metadata',
            field=models.TextField(default=b'', null=True, blank=True),
            preserve_default=True,
        ),
    ]
