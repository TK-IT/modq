# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-17 23:21
from __future__ import unicode_literals

from django.db import migrations
from django.core.files.base import ContentFile


def populate_message_fields(apps, schema_editor):
    Message = apps.get_model('mailhole', 'Message')

    import mailhole.models

    for message in Message.objects.all():
        if message.message_file:
            continue
        message.message_file.save(
            'message.msg', ContentFile(message.message_bytes))
        mailhole.models.Message.extract_message_data(message)
        message.save()


class Migration(migrations.Migration):

    dependencies = [
        ('mailhole', '0005_add_split_message_fields'),
    ]

    operations = [
        migrations.RunPython(populate_message_fields),
    ]
