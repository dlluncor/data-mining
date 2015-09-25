import datetime
from mongoengine import *
from mongoengine.queryset import DoesNotExist
from config import config

connect("mate", host=config.mongodb_uri)

class Subscription(Document):
    email = StringField(max_length=256, required=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    meta = {
        'allow_inheritance': True,
        'indexes': ['email'],
        'ordering': ['email']
    }

    @staticmethod
    def is_exist(email):
        try:
            sub = Subscription.objects.get(email=email)
            return True
        except DoesNotExist:
            return False

    @staticmethod
    def get_by(email=None):
        try:
            sub = None
            if email:
                sub = Subscription.objects.get(email=email)
            return sub
        except DoesNotExist:
            return None

class Feedback(Document):
    email = StringField(max_length=256, required=True)
    comment = StringField(max_length=1024)
    created_at = DateTimeField(default=datetime.datetime.now)

    meta = {
        'allow_inheritance': True,
        'indexes': ['email'],
        'ordering': ['email']
    }

class Contact(Document):
    email = StringField(max_length=256, required=True)
    first_name = StringField(max_length=256, required=True)
    last_name = StringField(max_length=256, required=True)
    address_line_1 = StringField(max_length=1024, required=True)
    address_line_2 = StringField(max_length=1024)
    city = StringField(max_length=256, required=True)
    state = StringField(max_length=256, required=True)
    zip_code = StringField(max_length=256, required=True)
    phone_number = StringField(max_length=256, required=True)

    created_at = DateTimeField(default=datetime.datetime.now)

    meta = {
        'allow_inheritance': True,
        'indexes': ['email'],
        'ordering': ['email']
    }

    @staticmethod
    def is_exist(email):
        try:
            contact = Contact.objects.get(email=email)
            return True
        except DoesNotExist:
            return False

    @staticmethod
    def get_by(email=None):
        try:
            contact = None
            if email:
                contact = Contact.objects.get(email=email)
            return contact
        except DoesNotExist:
            return None
