# Generated by Django 4.1.7 on 2023-03-20 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_bids_bid_rename_comments_comment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='listing',
            name='url_image',
            field=models.URLField(default=''),
        ),
    ]
