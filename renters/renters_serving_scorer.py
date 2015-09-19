
import ml.serving_scorer
import renter_form
import feature_extractor

def to_renter_form(form_info):
  # TODO(haoran): Convert a form_info object to this RenterForm object.
  return renter_form.RenterForm(form_info)

def get_price(form_info):
  # TODO(haoran): Fill in this function and make it work.
  # Basically read in the model files you generated in gen_offline_model and
  # test this function given an example form_info.
  # form_info is what the frontend will pass most likely.
  form = to_renter_form(form_info)
  fe = feature_extractor.FeatureExtractor()
  seti = fe.to_seti(form)
  ss = SetiServer()
  ss.load_model('renters-price-v1.csv')
  price = ss.score(seti)
  return price
