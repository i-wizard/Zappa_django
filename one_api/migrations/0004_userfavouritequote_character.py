# Generated by Django 4.0.2 on 2022-02-01 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('one_api', '0003_remove_userfavouritequote_character_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfavouritequote',
            name='character',
            field=models.CharField(blank=True, max_length=555, null=True),
        ),
    ]