# Generated by Django 4.2.9 on 2024-03-13 22:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ml_app', '0012_mlmodel_prediction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mlmodel',
            name='prediction',
        ),
    ]