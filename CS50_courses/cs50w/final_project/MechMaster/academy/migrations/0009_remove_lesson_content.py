# Generated by Django 4.2.2 on 2023-07-04 23:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0008_lesson_content_alter_course_title_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='content',
        ),
    ]