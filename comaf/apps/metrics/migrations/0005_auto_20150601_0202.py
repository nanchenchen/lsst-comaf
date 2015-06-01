# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0004_metric_metadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='display_caption',
            field=models.TextField(default=b'', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='metric',
            name='display_group',
            field=models.TextField(default=b'', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='metric',
            name='display_order',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='metric',
            name='display_subgroup',
            field=models.TextField(default=b'', null=True, blank=True),
            preserve_default=True,
        ),
    ]
