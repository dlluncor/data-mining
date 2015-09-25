
import renter_form
import feature_extractor
import renter_constants

from ml import seti_server
from ml import feature_selector


def to_renter_form(form_info):
  return renter_form.RenterForm(form_info)

def get_price(form_info, for_test=False):
  # Setup the seti server.
  l_config = renter_constants.learned_config2
  ss = seti_server.make_from_config(l_config.model_configs)

  # Generate a price for the form.
  form = to_renter_form(form_info)
  print 'Form: '
  print(form)
  #print 'Age: '
  #print(form.get_age())
  fe = feature_extractor.FeatureExtractor(for_test)
  seti = fe.to_seti(form)
  price = ss.score(seti)
  return price
