# Generated by Django 3.1.1 on 2020-09-21 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200921_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='ksh_price',
        ),
        migrations.RemoveField(
            model_name='category',
            name='usd_price',
        ),
        migrations.AddField(
            model_name='product',
            name='ksh_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='usd_price',
            field=models.FloatField(default=0, editable=False),
        ),
    ]
