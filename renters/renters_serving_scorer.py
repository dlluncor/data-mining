
import ml.serving_scorer
import renter_form
import feature_extractor

def to_renter_form(form_info):
  return renter_form.RenterForm()

def get_price(form_info):
  form = to_renter_form(form_info)
  fe = feature_extractor.FeatureExtractor()
  seti = fe.to_seti(form)
  ss = SetiServer()
  ss.load_model('renters-price-v1')
  price = ss.score(seti)
  return price