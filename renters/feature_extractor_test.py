
import feature_extractor
import renter_form
from ml import seti
from collections import OrderedDict

def testFeatureExtract():
  fe = feature_extractor.FeatureExtractor()
  s0 = seti.create_seti(19.15, bfs=[('gender', 'f')], cfs=[
    ('dob', 26.0), ('deductible', 150.0), ('personal_property_value', 4000),
    ('personal_liability', 2000)])
  rf = renter_form.RenterForm(
    OrderedDict([
      ('dob', '2/3/1989'),
      ('gender', 'f'),
      ('deductible', '100 / 250'),
      ('personal_property_value', '4000'),
      ('personal_liability', '2000')
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