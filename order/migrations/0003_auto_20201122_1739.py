# Generated by Django 3.1.3 on 2020-11-22 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20201122_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlist',
            name='color',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='size',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
