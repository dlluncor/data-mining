
from ml.serving_scorer import SetiServer
import renter_form
import feature_extractor
from ml import feature_selector
import renter_constants

def to_renter_form(form_info):
  return renter_form.RenterForm(form_info)

def get_price(form_info):
  # Setup the seti server.
  cols_cfg = ['gender', 'dob']
  fs = feature_selector.FeatureSelector()
  l_config = renter_constants.learned_config
  fs.read_feature_map(l_config.feature_map_loc)
  ss = SetiServer(fs)
  for model_config in l_config.model_configs:
    ss.load_model_from_config(model_config)

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
