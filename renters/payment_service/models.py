import base64, datetime, hashlib, json, re, util
from mongoengine import *
from mongoengine.queryset import DoesNotExist
from config import config

connect("credit_cards", host=config.mongodb_uri)

class CreditCard(Document):
    card_info = StringField(required=True)

    masked_number = StringField(min_length=12, max_length=20)
    token = StringField(max_length=32)

    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    meta = {
        'ordering': ['-created_at']
    }

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        if not document.card_info:
            raise ValidationError("Empty Card Information")

        try:
            info = CreditCard.decrypt_card_info(document.card_info)
        except Exception as e:
            print(e)
            raise ValidationError("Fail to parse card information. %s" % e)

        if not CreditCard.luhn_validate(info['card_number']):
            raise ValidationError("Invalid Credit Card Number")

        if not CreditCard.validate_expiration_date(info['exp_month'], info['exp_year']):
            raise ValidationError("Expired Credit Card or Invalid Expiration Date")

        document.masked_number = info['card_number'][:6] + 'X' * 6 + info['card_number'][-4:]
        key = "{}-{}/{}-{}".format(info['card_number'], info['exp_month'], info['exp_year'], info['cvc'])
        m = hashlib.md5(key)
        document.token = m.hexdigest()

    @classmethod
    def decrypt_card_info(cls, info):
        # The encrypt card information is encoded to base64 string by client side, should decode before decrypt
        ciphertext = base64.b64decode(info)
        plaintext = util.decrypt(ciphertext, config.private_key_path)
        card_info = json.loads(plaintext)
        return card_info

    @staticmethod
    def validate_expiration_date(month, year):
        if not re.match('\d\d', month):
            return False

        if not re.match('\d\d', year):
            return False

        # expiration_date should be in format '%m/%y' with zero-padded decimal number
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
        if not re.match('^\d+$', card_number):
            return False

        # skip validation of China UnionPay and Diners Club enRoute
        if re.match(r'^(62|2014|2149)', card_number):
            return True

        r = [int(ch) for ch in card_number][::-1]
        return (sum(r[0::2]) + sum(sum(divmod(d*2,10)) for d in r[1::2])) % 10 == 0

pre_save.connect(CreditCard.pre_save, sender=CreditCard)
