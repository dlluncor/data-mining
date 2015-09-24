
import gen_offline_model
from ml import seti_server
from ml import model_cfg

def testLearn():
  d = gen_offline_model.main(['gen_offline_model.py', 'regression_test'])
  # Make sure that every SETI object that we generate, we have the exact price for
  # when run back through the code.
  l_config = d['l_config']
  ss = seti_server.make_from_config(l_config.model_configs)
  for seti in d['setis']:
    price = ss.score(seti)
    assertFloatEquals(seti.label, price)

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