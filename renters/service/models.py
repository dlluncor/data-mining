import datetime, re
from mongoengine import *
from mongoengine.queryset import DoesNotExist
from config import config

connect("mate", host=config.mongodb_uri)

class RenterForm(DynamicDocument):
    payment_info = ReferenceField('PaymentInfo')

class PaymentInfo(Document):
    renter_form = ReferenceField(RenterForm, reverse_delete_rule=CASCADE)
    card_number = StringField(min_length=12, max_length=20, required=True)
    card_expiration_date = StringField(min_length=5, max_length=5, required=True)
    card_cvv = StringField(min_length=4, max_length=4, required=True)
    status = StringField(max_length=128)

    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    @staticmethod
    def luhn_validate(card_number):
        """
        Validate the credit card number

        Params:
            card_number: String[length=12-19]

        Ref:
            1. https://en.wikipedia.org/wiki/Bank_card_number
            2. http://rosettacode.org/wiki/Luhn_test_of_credit_card_numbers#JavaScript
        """
        # TODO skip validation of China UnionPay and Diners Club enRoute
        if re.match(r'^(62|2014|2149)', card_number):
            return True

        r = [int(ch) for ch in card_number][::-1]
        return (sum(r[0::2]) + sum(sum(divmod(d*2,10)) for d in r[1::2])) % 10 == 0

"""
# INsurance Types
INSURANCE_AUTO = 1
INSURANCE_BUSINESS = 2
INSURANCE_CONDO = 3
INSURANCE_HOME = 4
INSURANCE_LIFE = 5
INSURANCE_RENTERS = 6

# Gender
GENDER_FEMALE = 1
GENDER_MALE = 2


PROPERTY_TYPE_RENTED_HOUSE_SINGLE_FAMILY = 1
PROPERTY_TYPE_RENTED_APARTMENT_OR_CONDO  = 2
PROPERTY_TYPE_RENTED_TOWNHOUSE           = 3
PROPERTY_TYPE_RENTED_DUPLEX-OR_TRIPLEX   = 4
PROPERTY_TYPE_RENTED_3M_HOME             = 5 # PROPERTY_TYPE_RENTED_MOBILE_OR_MANUFACTURED_OR_MODULAR_HOME
PROPERTY_TYPE_AL_OR_NURSING_HOME         = 6 # PROPERTY_TYPE_ASSISTED_LIVING_OR_NURSING_HOME
PROPERTY_TYPE_DORMITORY                  = 7
PROPERTY_TYPE_OTHER                      = 8

# Insurance Type,Zip code,First name,Last name,Date of birth,
# Gender,Address,City,State,Auto insurance coverage?,Property Type,
# units,# unrelated roommates,# property losses in last 3 years,Phone number,
# Email address,Fire Sprinkler System?,Central Fire & Burglar Alarm?,
# Local Fire / Smoke Alarm?,Home Security?,Non Smoking Household?,Local Burglar Alarm?,
# Unusual hazards?,Dogs that bite?,Run a business from home?,Start date,Personal property worth,
# Loss of use,Medical payments,Personal liability,Farmers Identity Protection,Deductible,
# Policy number,Timestamp (seconds),Policy price,Name of agent,Address of agent,Elancer Name
class BaseInsurance(Document):
    insurnace_type = IntField(required=True)

    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

class RenterInsurance(BaseInsurance):
    property_type = IntField(required=True)
    units_count   = IntField(required=True)
    unrelated_roommates_count = IntField(required=True)
    property_losses_count = IntField(required=True)

    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

class House(Document):
    zip_code = IntField(required=True)
    address = StringField(max_length=256, required=True)
    city = StringField(max_length=128, required=True)
    state = StringField(max_length=128, required=True)

    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

class User(Document):
    first_name    = StringField(max_length=128, required=True)
    last_name     = StringField(max_length=128, required=True)
    date_of_birth = DateTimeField(default=datetime.datetime.now, required=True)
    gender        = IntField(required=True)
    email = StringField(max_length=256, required=True)


    status = StringField(max_length=256)

    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    meta = {
        'allow_inheritance': True,
        'indexes': ['email'],
        'ordering': ['email']
    }
"""
