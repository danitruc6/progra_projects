# Generated by Django 4.1.7 on 2023-03-20 14:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_listing_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 3, 20, 14, 18, 33, 666874, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
