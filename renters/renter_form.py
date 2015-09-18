"""Renter form represents the raw information retrieved for a renters page.

"""

class RenterForm(object):

  def __init__(self):
    self.insurance_type = 'Renters'
    self.first_name = ''
    self.last_name = ''
    self.dob = ''
    self.has_auto_insurance_coverage = False