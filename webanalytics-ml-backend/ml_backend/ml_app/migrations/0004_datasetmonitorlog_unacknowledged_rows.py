# Generated by Django 4.2.9 on 2024-03-04 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ml_app', '0003_datasetmonitorlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasetmonitorlog',
            name='unacknowledged_rows',
            field=models.IntegerField(default=0),
        ),
    ]
