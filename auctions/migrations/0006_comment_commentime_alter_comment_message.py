# Generated by Django 5.0 on 2024-01-03 13:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_item_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='commentime',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='comment',
            name='message',
            field=models.CharField(max_length=120),
        ),
    ]