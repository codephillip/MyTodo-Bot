# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-11-04 10:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mytodobot', '0002_auto_20171104_1027'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='text_message',
            new_name='description',
        ),
    ]
