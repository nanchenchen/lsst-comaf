# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('metrics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberSpace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('plots', models.ManyToManyField(default=None, related_name='member_spaces', null=True, to='metrics.Plot', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpaceView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('plots', models.ManyToManyField(default=None, related_name='space_views', null=True, to='metrics.Plot', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkSpace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('current_views', models.ForeignKey(to='workspace.SpaceView')),
                ('member_spaces', models.ManyToManyField(default=None, related_name='workspaces', null=True, to='workspace.MemberSpace', blank=True)),
                ('members', models.ManyToManyField(default=None, related_name='workspaces', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('space_views', models.ManyToManyField(default=None, related_name='workspaces', null=True, to='workspace.SpaceView', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='memberspace',
            name='space_views',
            field=models.ManyToManyField(default=None, related_name='member_spaces', null=True, to='workspace.SpaceView', blank=True),
            preserve_default=True,
        ),
    ]
