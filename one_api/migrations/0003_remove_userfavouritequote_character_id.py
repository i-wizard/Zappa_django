# Generated by Django 4.0.2 on 2022-02-01 21:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('one_api', '0002_rename_qoutes_userfavoritecharacter_quotes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfavouritequote',
            name='character_id',
        ),
    ]