# Generated by Django 4.1.5 on 2023-05-06 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_relays', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationdata',
            name='data',
            field=models.JSONField(default=dict),
        ),
    ]
