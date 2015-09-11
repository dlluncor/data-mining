import datetime
from mongoengine import *
from mongoengine.queryset import DoesNotExist

connect("social")

class Tweet(DynamicDocument):
    id = LongField(primary_key=True)
    pass
