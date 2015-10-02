
import renter_form
import feature_extractor
import renter_constants

from ml import seti_server
from ml import feature_selector


def to_renter_form(form_info):
  return renter_form.RenterForm(form_info)

def get_price(l_config, form_info, use_memorized_only, for_test=False):
  ss = seti_server.make_from_config(l_config.model_configs)

  # Generate a price for the form.
  form = to_renter_form(form_info)
  print 'Form: '
  print(form)
  #print 'Age: '
  #print(form.get_age())
  fe = feature_extractor.FeatureExtractor(for_test)
  seti = fe.to_seti(form)
  price = ss.score(seti, use_memorized_only)
  return price
