# Generated by Django 4.1.5 on 2023-04-09 18:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('relays', '0009_rename_userrelaypermissions_userrelaypermission'),
    ]

    operations = [
        migrations.AddField(
            model_name='relay',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
