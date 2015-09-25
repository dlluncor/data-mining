
import feature_extractor
import renter_form
from ml import seti
from collections import OrderedDict

def testFeatureExtract():
  fe = feature_extractor.FeatureExtractor()
  s0 = seti.create_seti(19.15, 
    bfs=[
    ('has_bite_dog', 'N'),
    ('age_group', 'middle-age'),

    ('insurance_type', 'renters'),
    ('full_address', '1599 Warburton Ave, Santa Clara, CA, 95050'),
    ('has_auto_insurance_coverage', 'Y'),

    ('has_fire_sprinkler_system', 'N'),
    ('has_center_fire_burglar_alarm', 'N'),
    ('has_local_fire_smoke_alarm', 'Y'),
    ('has_home_security', 'N'),
    ('is_non_smoking_household', 'Y'),
    ('has_local_burglar_alarm', 'N'),
    #
    ('farmers_identity_protection', 'Y'),
    ],
    cfs=[
    ('dob', 26.0), 

    ('unit_count', 2),
    ('property_losses_count', 3),

    ('personal_property_worth', 4000),
    ('medical_payments', 2000),
    ('personal_liability', 100000),
    ('deductible', 150.0)
    ])
  rf = renter_form.RenterForm(
    OrderedDict([
      ('dob', '2/3/1989'),

      ('address', '1599 Warburton Ave'),
      ('city', 'Santa Clara'),
      ('state', 'CA'),
      ('zip_code', '95050'),

      ('has_auto_insurance_coverage', 'Y'),
      ('unit_count', '2 to 4'),
      ('property_losses_count', 3),

      # Hazards.
      ('has_fire_sprinkler_system', 'N'),
      ('has_center_fire_burglar_alarm', 'N'),
      ('has_local_fire_smoke_alarm', 'Y'),
      ('has_home_security', 'N'),
      ('is_non_smoking_household', 'Y'),
      ('has_local_burglar_alarm', 'N'),

      ('has_bite_dog', 'N'),
      #
      ('personal_property_worth', '4000'),
      ('medical_payments', '2000'),
      ('personal_liability', '100000'),
      ('farmers_identity_protection', 'Y'),
      ('deductible', '100 / 250'),
    ])
  )
  rf.label = 19.15
  #s1 = seti.create_seti(22.51, bfs=[('gender', 'm')], cfs=[('dob', 66.0)])
  assertEquals(str(s0), str(fe.to_seti(rf)))

"""
def testFeatureExtract2():
  fe = feature_extractor.FeatureExtractor()
  s0 = seti.create_seti(19.15, bfs=[('gender', 'f')], cfs=[
    ('dob', 26.0), ('deductible', 100.0)])
  rf = renter_form.RenterForm(
    OrderedDict([
      ('dob', '2/3/1989'),
      ('gender', 'f'),
      ('deductible', '100')
      ('personal_property', '4000'),
    ])
  )
  rf.label = 19.15
  #s1 = seti.create_seti(22.51, bfs=[('gender', 'm')], cfs=[('dob', 66.0)])
  assertEquals(str(s0), str(fe.to_seti(rf)))
"""

# Test util template.
import sys
import inspect

errs = []

def assertFloatEquals(expected, got):
  caller_name = sys._getframe().f_back.f_code.co_name
  v0 = '%.4f' % expected
  v1 = '%.4f' % got
  if v0 != v1:
    errs.append('In %s, Expected: %s. Got: %s' % (caller_name, expected, got))

def assertEquals(expected, got):
  caller_name = sys._getframe().f_back.f_code.co_name
  if expected != got:
    errs.append('In %s, Expected: %s. Got: %s' % (caller_name, expected, got))

def main():
  funs = dir(sys.modules[__name__])
  for fun in funs:
    if fun.startswith('test'):
      globals()[fun]()
  if len(errs) == 0:
    print '%s test passes!' % (sys.argv[0])
  else:
    for err in errs:
      print err
  
if __name__ == '__main__':
  main()