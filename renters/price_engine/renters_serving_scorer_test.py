
import renters_serving_scorer as ss
import renter_constants

def testLogsToSeti():
  # Setup the seti server.
  l_config = renter_constants.learned_config2
  # First three lines are copied from tdg_v0.csv
  price = ss.get_price(l_config, 
    {'dob': '11/11/1988', 'age_group': 'middle-age',
     'has_bite_dog': 'F'}, for_test=True)
  print 'Price received: '
  assertGt(price, 10)


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

def assertGt(expected, got):
  caller_name = sys._getframe().f_back.f_code.co_name
  if expected <= got:
    errs.append('In %s, Got: %s > %s' % (caller_name, expected, got))

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