# Generated by Django 3.1.4 on 2021-01-22 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20210120_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='donated_loyalty_points_clean_forest',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='donated_loyalty_points_plant_tree',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='donated_loyalty_points_recycle_plastic',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
    ]
