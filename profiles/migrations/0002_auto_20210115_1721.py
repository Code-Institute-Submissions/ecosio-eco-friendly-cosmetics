# Generated by Django 3.1.4 on 2021-01-15 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='default_street_address1',
            new_name='default_street_address',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='default_county',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='default_street_address2',
        ),
    ]