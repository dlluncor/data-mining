"""Renter form represents the raw information retrieved for a renters page.

"""

from datetime import datetime

class RenterForm(object):
    def __init__(self, *args, **kwargs):
        """
        Init form from dict or keyword arguments.

        Args should be dict type

        Below are keys for args or kwargs with values
            insurance_type = 'Renters'
            first_name = ''
            last_name = ''
            dob = '' # date of birth
            gender = '' # male, female
            address = ''
            city = ''
            state = '' # CA
            zip_code = '' # 94063
            has_auto_insurance_coverage = False
            property_type = ['RENTED HOUSE - SINGLE FAMILY' | 'RENTED APARTMENT/CONDO' |
                'RENTED TOWNHOUSE' | 'RENTED DUPLEX/TRIPLEX' | 'RENTED MOBILE, MANUFACTURED OR MODULAR HOME' |
                'ASSISTED LIVING OR NURSING HOME' | 'DORMITORY' | 'OTHER']
            unit_count = ['1' | '2 - 4' | '5+']
            unrelated_roommates_count = ['0' | '1' | '2' | '3 or more']
        """
        for data in args:
            for key in data:
                setattr(self, key, data[key])

        for key in kwargs:
            setattr(self, key, kwargs[key])

        self.label = -1

    def get_age(self):
        return float(datetime.now().year - datetime.strptime(self.dob, '%m/%d/%Y').year)

    def get_policy_price(self):
        try:
          return float(self.policy_price.replace('$', '')), None
        except Exception as e:
          return None, str(e)

    def __str__(self):
        return str(self.__dict__) + " | " + str(self.label)
