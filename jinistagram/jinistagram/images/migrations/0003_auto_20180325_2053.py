# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-25 11:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_auto_20180325_1707'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='cpation',
            new_name='caption',
        ),
    ]
