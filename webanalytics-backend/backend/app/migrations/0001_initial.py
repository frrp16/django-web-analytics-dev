# Generated by Django 4.2.9 on 2024-02-25 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_cryptography.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='connection', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('table_name', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('CHANGED', 'Changed'), ('STABLE', 'Stable')], default='STABLE', max_length=7)),
                ('is_trained', models.CharField(choices=[('TRAINING', 'Training'), ('TRAINED', 'Trained'), ('UNTRAINED', 'Untrained')], default='UNTRAINED', max_length=9)),
                ('connection', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.databaseconnection')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='datasets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DatasetMonitorLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('row_count', models.IntegerField(default=0)),
                ('column_count', models.IntegerField(default=0)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monitor_logs', to='app.dataset')),
            ],
        ),
    ]
