"""
  Feature extractor generates the features given an input vector.
"""

from ml import seti

"""

DONE:

  ('Insurance Type', (['Renters'], 'fixed')),

  ('Personal property worth', (property_worth, 'iterate')),
  ('Loss of use', (['Keep default'], 'iterate')),
  ('Medical payments', (medical_payments, 'iterate')),
  
  ('Personal liability', (personal_liability, 'iterate')),
  ('Farmers Identity Protection', (['N', 'Y'], 'fixed')), # Y / N
  ('Deductible', (deductible, 'iterate'))

NOT DONE:
d = OrderedDict([
  # header0
  ('Zip code', (zip_codes, 'fixed')),
  ('First name', (first_names, 'random')),
  ('Last name', (last_names, 'random')),
  ('Date of birth', (dobs, 'iterate')),
  ('Gender', (['m', 'f'], 'random')),
  ('Address', (addresses, 'fixed')),
  ('City', (cities, 'fixed')),
  ('State', (['CA'], 'fixed')),
  ('Zip code', (zip_codes, 'fixed')),
  ('Auto insurance coverage?', (['N', 'Y'], 'fixed')), # Y / N
  # header1
  ('Property Type', (['RENTED HOUSE - SINGLE FAMILY'], 'fixed')),
  ('# units', (['1', '2 to 4', '5+'], 'iterate')),
  #('# unrelated roommates', (['0', '1', '2', '3 or more'], 'fixed')),
  ('# unrelated roommates', (['0', '1', '2'], 'fixed')),
  ('roommate names', (('david', 'lee'), 'random')),
  #('# property losses in last 3 years', (['0', '1', '2', '3', '4', '5 or more'], 'fixed')), # '0', '1', '2', '3', '4', '5 or more'
  ('# property losses in last 3 years', (['0', '1', '2', '3', '4'], 'fixed')), # '0', '1', '2', '3', '4', '5 or more'
  ('Phone number', (phone_numbers, 'random')),
  ('Email address', (emails, 'random')),
  # Security systems.
  ('Fire Sprinkler System?', (['N', 'Y'], 'fixed')), # Y / N
  ('Central Fire & Burglar Alarm?', (['N', 'Y'], 'fixed')), # Y / N
  ('Local Fire / Smoke Alarm?', (['N', 'Y'], 'fixed')), # Y / N
  ('Home Security?', (['N', 'Y'], 'fixed')), # Y / N
  ('Non Smoking Household?', (['Y', 'N'], 'fixed')), # Y / N
  ('Local Burglar Alarm?', (['N', 'Y'], 'fixed')), # Y / N
  ('Unusual hazards?', (['NONE'], 'fixed')),
  ('Dogs that bite?', (['N', 'Y'], 'fixed')), # Y / N
  ('Run a business from home?', (['N'], 'fixed')),
  ('Start date', (['Keep default.'], 'fixed')),

])
"""

class FeatureExtractor(object):
  def __init__(self, for_test=False):
    self.for_test = for_test

  def to_seti(self, rf):
    """
    Args:
      rf: A renter_form.RenterForm.
    """
    # Do all logic to produce a SETI example here.
    s = seti.SETIExample()
    s.add_binary('insurance_type', 'renters')
    s.add_continuous('dob', rf.get_age())
    s.add_binary('gender', rf.gender)
    s.add_binary('farmers_identity_protection', rf.farmers_identity_protection)
    s.weight = 1
    s.label = rf.label
    if self.for_test:
      return s
    s.add_continuous('personal_property_value', rf.personal_property_value)
    s.add_continuous('personal_liability', rf.personal_liability)
    s.add_continuous('deductible', rf.get_deductible())
    return s


