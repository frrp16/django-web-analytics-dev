# Generated by Django 4.2.9 on 2024-03-12 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0004_datasetmonitorlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasetmonitorlog',
            name='changes',
            field=models.JSONField(null=True),
        ),
    ]
