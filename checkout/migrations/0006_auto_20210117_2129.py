# Generated by Django 3.1.4 on 2021-01-17 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0005_auto_20210117_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='loyalty_points',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
    ]
