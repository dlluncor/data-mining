
import app
import copy
from price_engine.ml import model_cfg
from price_engine import renter_constants

def testGetPriceOfForm():
  data = {
    "renter_form": {
       "insurance_type": "Renters",
       "first_name": "Christian",
       "last_name": "Bale",
       "dob": "01/30/1974",
       "gender": "m",
       "address": "3328 Bay Road",
       "city": "Rewood City",
       "state": "CA",
       "zip_code": "94063",
       "purchase_category": "cheap"
    }
  }
  categories = ['cheap', 'medium', 'deluxe']
  for i in xrange(len(categories)):
    data['renter_form']['purchase_category'] = categories[i]
    # Question 0: Do the prices increase?
    print app.get_price_of_user_form(data, use_memorized_only=False)
    # Question 1: Do we have all the data scraped memorized except
    # for dob and address?
    l_config = copy.deepcopy(renter_constants.learned_config2)
    l_config.delete_learned_model()

# Test that we score all memorized version of the prices.
def testGetMemorizedPrices():
  data = {
    "renter_form": {
       "insurance_type": "Renters",
       "first_name": "Christian",
       "last_name": "Bale",
       "dob": "01/30/1974",
       "gender": "m",
       "address": "3328 Bay Road",
       "city": "Rewood City",
       "state": "CA",
       "zip_code": "94063",
       "purchase_category": "cheap"
    }
  }
  d = app.get_three_prices(data, use_memorized_only=True)
  assertEquals(len(d.keys()), 3)

# Test util template.
import sys
import inspect

errs = []

def assertFloatEquals(expected, got):
  caller_name = sys._getframe().f_back.f_code.co_name
  v0 = '%.4f' % expected
  v1 = '%.4f' % got
  if v0 != v1:
    errs.append('In %s, Expected: %s. \nGot: %s' % (caller_name, expected, got))

def assertEquals(expected, got):
  caller_name = sys._getframe().f_back.f_code.co_name
  if expected != got:
    errs.append('In %s, \nExpected: %s. \nGot: %s' % (caller_name, expected, got))

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