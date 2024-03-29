# Generated by Django 4.1.5 on 2023-05-04 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('relays', '0016_channel_relay_channel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relay',
            name='channel',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='relays.channel'),
        ),
        migrations.CreateModel(
            name='RelayShareRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('state', models.BooleanField(default=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('relay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='relays.relay')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
