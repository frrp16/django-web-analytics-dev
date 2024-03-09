# Generated by Django 4.2.11 on 2024-03-08 00:57

from django.db import migrations, models
import django.db.models.deletion
import django_cryptography.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DatabaseConnection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('database_type', models.CharField(choices=[('postgresql', 'Postgresql'), ('mysql', 'Mysql'), ('mariadb', 'Mariabd'), ('oracle', 'Oracle'), ('sqlite', 'Sqlite')], default='postgresql', max_length=10)),
                ('host', models.CharField(default='localhost', max_length=255)),
                ('port', models.IntegerField()),
                ('database', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('password', django_cryptography.fields.encrypt(models.CharField(max_length=255))),
                ('ssl', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DatasetTable',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('table_name', models.CharField(max_length=255)),
                ('connection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.databaseconnection')),
            ],
        ),
    ]