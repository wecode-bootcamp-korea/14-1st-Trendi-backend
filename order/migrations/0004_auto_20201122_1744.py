# Generated by Django 3.1.3 on 2020-11-22 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20201122_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlist',
            name='color',
            field=models.IntegerField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='size',
            field=models.IntegerField(blank=True, default='', null=True),
        ),
    ]
