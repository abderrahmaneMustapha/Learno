# Generated by Django 2.1.6 on 2019-04-19 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ide', '0006_auto_20190411_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='title',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
