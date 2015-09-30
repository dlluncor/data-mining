import datetime, logging, sys
from flask import Flask, render_template, json, jsonify, request, send_from_directory
import util
import traceback
import os

from logging import StreamHandler
from logging import Formatter
from flask import Flask, request, json, jsonify
from config import config
from errors import ChargeException
from helper import *
from models import RenterForm

sys.path.append("..") # Adds higher directory to python modules path.

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

log_handler = StreamHandler(sys.stdout)
app.logger.addHandler(log_handler)
log_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
app.logger.setLevel(logging.INFO)

log_handler2 = StreamHandler(sys.stderr)
log_handler2.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(log_handler2)

# payment messages

SUCCESS_MSG = 'Thanks for the subsription. We will let you know when we launch!'
MISS_EMAIL_MSG = 'Sorry, email is required for subscription.'
ALREADY_SUBSCRIBED_MSG = "Thanks, you have already placed your deposit with this email."

# Displaying templates.
@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('assets', path)

@app.route('/')
def home_page():
    return util.render_common_template('index.html')

@app.route('/test')
def test_page():
    return util.render_common_template('test.html')

@app.route('/quote')
def quote_page():
    return util.render_common_template('quote.html')

@app.route('/terms')
def terms():
    return util.render_common_template('terms.html')

@app.route('/privacy_policy')
def privacy_policy():
    return util.render_common_template('privacy_policy.html')

@app.route('/about')
def about():
    return util.render_common_template('about.html')

from price_engine import renters_serving_scorer
from price_engine import renter_constants
from price_engine.ml import model_cfg

def ExpandDefaults(purchase_category):
  d = {
    'has_bite_dog': 'N',
    'has_auto_insurance_coverage': 'N',
    'has_fire_sprinkler_system': 'Y',
    'has_center_fire_burglar_alarm': 'Y',
    'has_local_fire_smoke_alarm': 'Y',
    'has_home_security': 'Y',
    'is_non_smoking_household': 'Y',
    'has_local_burglar_alarm': 'Y',
    'farmers_identity_protection': 'N',
    'unit_count': '5+',
    'property_losses_count': '0',
    'medical_payments': '1000',
    'personal_liability': '100000' # REALLLY?
  }
  cat = purchase_category
  if cat == 'cheap':
    d['personal_property_worth'] = '5000'
    d['deductible'] = '500'
  elif cat == 'medium':
    d['personal_property_worth'] = '15000'
    d['deductible'] = '1000'
  elif cat == 'deluxe':
    d['personal_property_worth'] = '35000'
    d['deductible'] = '500'
  else:
    raise Exception('Unrecognized purchase category: %s' % cat)
  return d


def get_price_of_form(renter_form_dict):
  # Fill out the entire renter form.
  defaults = ExpandDefaults(renter_form_dict['purchase_category'])
  renter_form_dict.update(defaults)

  # Create config to pass into renter serving scorer.
  l_config = renter_constants.learned_config2
  # Change directories so that we can properly access the files.
  # Right now they are set up to be relative to the engine
  model_cfg.change_dirs('../price_engine/tmp', l_config.model_configs)

  price = renters_serving_scorer.get_price(l_config, renter_form_dict)
  return price

@app.route('/price', methods=['POST'])
def price():
    """
      When the user wants to know what is the estimated price of
      their insurance policy.
    """
    try:
      data = request.get_json()
      renter_form_dict = data['renter_form']
      price = get_price_of_form(renter_form_dict)
      return '%f' % (price)
    except Exception as e:
      line = traceback.format_exc()
      return line

    #return util.render_common_template('about.html')

#first name, last name, address, phone number, dob
@app.route('/buy', methods=['POST'])
def buy():
    """
      When the user has completed the flow and is completing their
      insurance purchase.

      Example input:
      form = {
       'insurance_type': 'Renters',
       'first_name': 'Christian',
       'last_name': 'Bale',
       'dob': '01/30/1974',
       'gender': 'm',
       'address': '3328 Bay Road',
       'city': 'Rewood City',
       'state': 'CA',
       'zip_code': '94063'
      }
    """
    try:
      data = request.get_json()
      renter_form_dict = data['renter_form']
      price = get_price_of_form(renter_form_dict)

      # Expand defaults so we know what we are assuming.
      defaults = ExpandDefaults(renter_form_dict['purchase_category'])
      renter_form_dict.update(defaults)
      # Log whatever price we have calculated here.
      renter_form_dict['policy_price'] = '$%f' % (price)
      print renter_form_dict
      #payment = data['payment']
      #form = RenterForm(**renter_form_dict)
      #form.save()
      return 'success'
    except Exception as e:
      line = traceback.format_exc()
      return line

@app.route('/error', methods=['GET'])
def error():
    raise Exception('shit', status_code=500)

@app.errorhandler(404)
def page_not_found(e):
    return util.render_common_template('errors/404.html'), 404

#@app.errorhandler(Exception)
#def handle_exception(error):
#    return util.render_common_template('errors/500.html', err_msg=repr(error))


if __name__ == '__main__':
    if config.DEBUG:
        app.logger.setLevel(logging.DEBUG)
        app.run(debug=True, host='0.0.0.0', port=8080)
    elif config.PROD:
        app.logger.setLevel(logging.ERROR)
        from gevent.wsgi import WSGIServer

        http_server = WSGIServer(('', 80), app)
        http_server.serve_forever()
