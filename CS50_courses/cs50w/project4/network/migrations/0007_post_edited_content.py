# Generated by Django 4.2.1 on 2023-05-29 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_follow_delete_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='edited_content',
            field=models.TextField(blank=True),
        ),
    ]