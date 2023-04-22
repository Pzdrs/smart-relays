# Generated by Django 4.1.5 on 2023-04-11 21:34

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('relays', '0014_alter_userrelayshare_unique_together'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RelayCreateLog',
            new_name='RelayCreateRecord',
        ),
        migrations.RenameModel(
            old_name='RelayUpdateLog',
            new_name='RelayUpdateRecord',
        ),
    ]