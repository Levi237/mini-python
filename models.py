import datetime
import os

from peewee import *

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin

from playhouse.db_url import connect

# DATABASE = connect(os.environ.get('postgres://tovozpuskotolm:97df10193701f1e0dee2e5fa7003705178385d390829136fb05eac6370395d88@ec2-54-83-1-101.compute-1.amazonaws.com:5432/df785ca9cdnia1'))
DATABASE = SqliteDatabase('users.sqlite')

### psql
### CREATE DATABASE blogs;
### CREATE USER levi WITH PASSWORD 'password';
### GRANT ALL PRIVILEGES ON DATABASE blogs TO levi;
# DATABASE = PostgresqlDatabase('blogs', user='admin', password='myPassword')




#################### EXAMPLE FOR ONE TO MANY

# class BaseModel(Model):
#     class Meta:
#         database = psql_db

# class Authors(BaseModel):
#     id = PrimaryKeyField(null=False)
#     name = CharField(max_length=100, unique=True)

# class Books(BaseModel):
#     id = PrimaryKeyField(null=False)
#     title = CharField(max_length=100)
#     author = ForeignKeyField(Authors, related_name='author_details')
#     edition = CharField(max_length=100)
#     year_written = SmallIntegerField()
#     price = DecimalField()


class User(UserMixin, Model):
    username = CharField()
    email    = CharField(unique=True)
    password = CharField()
    # verify_password = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password, **kwargs):
        email = email.lower()
        try:
            cls.select().where(
                (cls.email==email)
            ).get()
        except cls.DoesNotExist:
            user = cls(username=username, email=email)
            user.password = generate_password_hash(password)
            user.save()
            return user
        else: 
            raise Exception('user with that email already exists')


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()