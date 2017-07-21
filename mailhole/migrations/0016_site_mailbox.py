# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-05 12:45
from __future__ import unicode_literals

from django.db import migrations


def site_mailbox(apps, schema_editor):
    Mailbox = apps.get_model('mailhole', 'Mailbox')
    Peer = apps.get_model('mailhole', 'Peer')
    Message = apps.get_model('mailhole', 'Message')
    peer_mailboxes = {}
    for peer in Peer.objects.all():
        try:
            peer_mailboxes[peer] = Mailbox.objects.get(name=peer.slug)
        except Mailbox.DoesNotExist:
            mailbox = Mailbox(email='%s@pseudo.local' % peer.slug,
                              name=peer.slug)
            mailbox.save()
            for r in peer.default_readers.all():
                mailbox.readers.add(r)
            peer_mailboxes[peer] = mailbox
    for msg in Message.objects.all():
        msg.mailbox = peer_mailboxes[msg.peer]
        msg.save()
    # Note: Message.mailbox is a ForeignKey to Mailbox
    # with on_delete=CASCADE. However, we have just ensured
    # that no Mailbox objects with name=NULL has any messages.
    Mailbox.objects.filter(name__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mailhole', '0015_mailbox_name'),
    ]

    operations = [
        migrations.RunPython(site_mailbox),
    ]