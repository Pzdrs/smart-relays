# Generated by Django 4.1.5 on 2023-05-04 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relays', '0017_alter_relay_channel_relaysharerecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='relay',
            name='synchronized',
            field=models.BooleanField(default=True),
        ),
    ]
