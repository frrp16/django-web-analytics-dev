from django.db import models

from django_cryptography.fields import encrypt

import uuid
import dotenv
import os

dotenv.load_dotenv()

from sqlalchemy import create_engine, URL

# connection to database_etl
database_etl_url = URL.create(
    drivername='postgresql',
    username=os.getenv('DATABASE_USER'),
    password=os.getenv('DATABASE_PASSWORD'),
    host=os.getenv('DATABASE_HOST'),
    port=os.getenv('DATABASE_PORT'),
    database=os.getenv('DATABASE_NAME')
)

database_etl_engine = create_engine(database_etl_url)


class DatabaseConnection(models.Model):
    class DatabaseType(models.TextChoices):
        POSTGRESQL = 'postgresql'
        MYSQL = 'mysql'
        MARIABD = 'mariadb'
        ORACLE = 'oracle'
        SQLITE = 'sqlite'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)    
    database_type = models.CharField(max_length=10, choices=DatabaseType.choices, default=DatabaseType.POSTGRESQL)
    host = models.CharField(max_length=255, default='localhost')
    port = models.IntegerField()
    database = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = encrypt(models.CharField(max_length=255))  
    ssl = models.BooleanField(default=False)

    def _get_engine_instance(self):
        try:
            url_object = URL.create(
                drivername=self.database_type,
                username=self.username,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database,
                query={'sslmode': 'require'} if self.ssl else {'sslmode': 'prefer'}
            )
            return create_engine(url_object)
        except Exception as e:
            raise Exception(e)

    engine_instance = property(_get_engine_instance)

    def get_connection_url(self):
        try:
            url_object = URL.create(
                drivername=self.database_type,
                username=self.username,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database,
                query={'sslmode': 'require'} if self.ssl else {}
            )
            return url_object.render_as_string(hide_password=False)
        except Exception as e:
            raise Exception(e)
    
    def connect(self, *args, **kwargs):
        try:
            return self.engine_instance.connect()
        except Exception as e:
            raise Exception(e)
    
    def disconnect(self, *args, **kwargs):
        self.engine_instance.dispose()