"""
  Feature extractor generates the features given an input vector.
"""

from ml import seti

"""

DONE:

  ('Insurance Type', (['Renters'], 'fixed')),


  ('Fire Sprinkler System?', (['N', 'Y'], 'fixed')), # Y / N
  ('Central Fire & Burglar Alarm?', (['N', 'Y'], 'fixed')), # Y / N
  ('Local Fire / Smoke Alarm?', (['N', 'Y'], 'fixed')), # Y / N
  ('Home Security?', (['N', 'Y'], 'fixed')), # Y / N
  ('Non Smoking Household?', (['Y', 'N'], 'fixed')), # Y / N
  ('Local Burglar Alarm?', (['N', 'Y'], 'fixed')), # Y / N

  ('Dogs that bite?', (['N', 'Y'], 'fixed')), # Y / N

  ('Personal property worth', (property_worth, 'iterate')),
  ('Medical payments', (medical_payments, 'iterate')),
  ('Personal liability', (personal_liability, 'iterate')),
  ('Farmers Identity Protection', (['N', 'Y'], 'fixed')), # Y / N
  ('Deductible', (deductible, 'iterate'))

IGNORE:
  ('Phone number', (phone_numbers, 'random')),
  ('Email address', (emails, 'random')),

  ('Unusual hazards?', (['NONE'], 'fixed')),
  ('Run a business from home?', (['N'], 'fixed')),

  ('Start date', (['Keep default.'], 'fixed')),
  ('Loss of use', (['Keep default'], 'iterate')),

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
  # Security systems.

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
    s.add_continuous('dob', rf.get_age())
    s.add_binary('gender', rf.gender) # TODO(dlluncor): REMOVE.
    
    s.weight = 1
    s.label = rf.label
    if self.for_test:
      return s

    # Binary.

    s.add_binary('insurance_type', 'renters')
    # Systems.
    systems = ['has_fire_sprinkler_system',
               'has_center_fire_burglar_alarm',
               'has_local_fire_smoke_alarm',
               'has_home_security',
               'is_non_smoking_household',
               'has_local_burglar_alarm']
    for system in systems:
      s.add_binary(system, getattr(rf, system))
    # Checks.
    s.add_binary('has_bite_dog', rf.has_bite_dog)
    s.add_binary('farmers_identity_protection', rf.farmers_identity_protection)

    # Continuous
    s.add_continuous('property_losses_count', rf.get_property_losses_count())

    s.add_continuous('personal_property_worth', rf.personal_property_worth)
    s.add_continuous('medical_payments', rf.medical_payments)
    s.add_continuous('personal_liability', rf.personal_liability)
    s.add_continuous('deductible', rf.get_deductible())
    return s


