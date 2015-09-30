import datetime, re, hashlib
from mongoengine import *
from mongoengine.queryset import DoesNotExist

from config import config

connect("credit_cards", host=config.mongodb_uri)

class CreditCard(Document):
    number = StringField(min_length=12, max_length=20, required=True)
    expiration_date = StringField(min_length=5, max_length=5, required=True)
    cvv = StringField(min_length=4, max_length=4, required=True)

    status = StringField(max_length=128)
    token = StringField(max_length=32)

    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        if not CreditCard.luhn_validate(document.number):
            raise ValidationError("Invalidate Credit Card Number")

        if not CreditCard.validate_expiration_date(document.expiration_date):
            raise ValidationError("Expired Credit Card")

        key = "{}-{}-{}".format(document.number, document.expiration_date, document.cvv)
        m = hashlib.md5(key)
        document.token = m.hexdigest()

    @staticmethod
    def validate_expiration_date(expiration_date):
        # expiration_date should be in format '%m/%y' with zero-padded decimal number
        month, year = expiration_date.split('/')
        now = datetime.datetime.now().strftime('%y/%m')
        return now <= "{}/{}".format(year, month)

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
        # skip validation of China UnionPay and Diners Club enRoute
        if re.match(r'^(62|2014|2149)', card_number):
            return True

        r = [int(ch) for ch in card_number][::-1]
        return (sum(r[0::2]) + sum(sum(divmod(d*2,10)) for d in r[1::2])) % 10 == 0

pre_save.connect(CreditCard.pre_save, sender=CreditCard)
