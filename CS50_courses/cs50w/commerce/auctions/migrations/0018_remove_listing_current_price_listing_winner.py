# Generated by Django 4.1.7 on 2023-03-25 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_listing_current_price_alter_listing_qty_bids'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='current_price',
        ),
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
