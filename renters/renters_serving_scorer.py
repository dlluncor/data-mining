
from ml.serving_scorer import SetiServer
import renter_form
import feature_extractor
from ml import feature_selector

def to_renter_form(form_info):
  return renter_form.RenterForm(form_info)

def get_price(form_info):
  # Setup the seti server.
  cols_cfg = ['gender', 'dob']
  fs = feature_selector.FeatureSelector()
  fs.read_feature_map('feature_map_v0.csv')
  ss = SetiServer(fs, cols_cfg)
  ss.load_model('renters-price-v1.csv')

  # Generate a price for the form.
  form = to_renter_form(form_info)
  print 'Form: '
  print(form)
  #print 'Age: '
  #print(form.get_age())
  fe = feature_extractor.FeatureExtractor()
  seti = fe.to_seti(form)
  price = ss.score(seti)
  return price

if __name__ == '__main__':
  price = get_price({'dob': '11/11/1988', 'gender': 'f'})
  print 'Price received: '
  print(price)
