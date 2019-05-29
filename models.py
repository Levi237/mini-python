import datetime

from peewee import *

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin

DATABASE = SqliteDatabase('newdb.sqlite')
### psql
### CREATE DATABASE blogs;
### CREATE USER levi WITH PASSWORD 'password';
### GRANT ALL PRIVILEGES ON DATABASE blogs TO levi;
# DATABASE = PostgresqlDatabase('blogs', user='levi', password='123')





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

class Blog(Model):
    title    = CharField()
    location = CharField()
    entry    = CharField()
    imageUrl = CharField()
    userId   = CharField()
    created_by = ForeignKeyField(User, related_name='blog_set')
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

class  Comment(Model):
    comment = CharField()

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Blog, Comment], safe=True)
    DATABASE.close()