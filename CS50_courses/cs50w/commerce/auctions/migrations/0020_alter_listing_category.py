# Generated by Django 4.1.7 on 2023-03-26 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_remove_listing_active_listing_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]