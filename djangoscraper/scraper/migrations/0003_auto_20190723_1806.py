# Generated by Django 2.2.3 on 2019-07-23 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_auto_20190722_2001'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='article_body',
            new_name='article_text',
        ),
    ]
