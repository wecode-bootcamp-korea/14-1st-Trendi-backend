# Generated by Django 3.1.3 on 2020-11-18 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_delete_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nick_name',
            field=models.CharField(max_length=20),
        ),
    ]
