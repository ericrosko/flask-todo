#!/usr/bin/env python3

import os

from peewee import Model, CharField, DateTimeField, ForeignKeyField
import os

from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL', 'sqlite:///my_database.db'))


class User(Model):
    name = CharField(max_length=255, unique=True)
    password = CharField(max_length=255, unique=False)

    class Meta:
        database = db


class Task(Model):
    name = CharField(max_length=255, unique=True)
    performed = DateTimeField(null=True)
    performed_by = ForeignKeyField(User, null=True)

    class Meta:
        database = db

if __name__ == "__main__":
    pass
