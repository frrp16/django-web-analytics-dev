# Generated by Django 4.2.11 on 2024-03-08 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_datasettable_date_updated_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datasettable',
            name='name',
        ),
    ]