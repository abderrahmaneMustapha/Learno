# Generated by Django 2.1.6 on 2019-04-29 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_auto_20190412_2158'),
        ('ide', '0007_auto_20190419_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportedlanguages',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='course.Course'),
        ),
    ]
