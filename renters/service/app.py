import datetime, logging, os, sys, traceback, copy
import requests, util
from flask import Flask, render_template, json, jsonify, request, redirect, send_from_directory
from logging import StreamHandler, Formatter
from config import config
from models import RenterForm
from helper import *

sys.path.append("..") # Adds higher directory to python modules path.

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

log_handler = StreamHandler(sys.stdout)
app.logger.addHandler(log_handler)
log_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
log_err_handler = StreamHandler(sys.stderr)
log_err_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(log_err_handler)

# Displaying templates.
@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('assets', path)

@app.route('/')
def home_page():
    return util.render_common_template('index.html')

@app.route('/quote', methods=['GET', 'POST'])
def quote_page():
    # The Amazon Elastic Load Balancer (ELB) supports a HTTP header called X-FORWARDED-PROTO.
    # All the HTTPS requests going through the ELB will have the value of X-FORWARDED-PROTO equal to 'HTTPS'.
    zip_code = request.form.get('zip_code')
    if request.headers.get('X-Forwarded-Proto') == 'http':
        secure_qoute = "https://rentsafe.co/quote"
        return redirect(secure_qoute, code=302)

    return util.render_common_template('quote.html', public_key=config.public_key, zip_code=zip_code)

@app.route('/payment_complete')
def payment_complete_page():
    return util.render_common_template('payment_complete.html')

@app.route('/terms')
def terms():
    return util.render_common_template('terms.html')

@app.route('/privacy_policy')
def privacy_policy():
    return util.render_common_template('privacy_policy.html')

@app.route('/about')
def about():
    return util.render_common_template('about.html')

# Practice handlers
@app.route('/email_template', methods=['GET'])
def email_template():
    form = {'last_name': u'Lee', 'is_non_smoking_household': 'Y', 'property_losses_count': '0',
            'personal_property_worth': '60000', 'medical_payments': '1000', 'has_home_security': 'Y',
            'email_address': u'david@bonjoylabs.com', 'has_local_fire_smoke_alarm': 'Y', 'first_name': u'David',
            'personal_liability': '300000', 'has_bite_dog': 'N', 'label': -1, 'state': u'California',
            'unit_count': '5+', 'zip_code': u'94063', 'phone_number': u'', 'insurance_type': u'renters',
            'city': u'Rewood City', 'has_center_fire_burglar_alarm': 'Y', 'has_fire_sprinkler_system': 'Y',
            'has_local_burglar_alarm': 'Y', 'address': u'3328 Bay Road', 'farmers_identity_protection': 'N',
            'dob': '01/01/1984', 'has_auto_insurance_coverage': 'N', 'deductible': '1000',
            'purchase_category': 'deluxe', 'policy_price': '$%.2f' % (13.4567)}
    #return util.render_common_template('email/confirmation.txt', first_name="David")
    return util.render_common_template('email/full_page.html', page="email/confirmation.html", **form)

from price_engine import renters_serving_scorer
from price_engine import renter_constants
from price_engine.ml import model_cfg

def ExpandDefaults(purchase_category):
  d = {
    'dob': '01/01/1984',
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
    'personal_liability': '100000'
  }
  cat = purchase_category
  if cat == 'cheap':
    d['personal_property_worth'] = '4000'
    d['deductible'] = '500'
  elif cat == 'medium':
    d['personal_property_worth'] = '30000'
    d['deductible'] = '1000'
  elif cat == 'deluxe':
    d['personal_property_worth'] = '60000'
    d['personal_liability'] = '300000'
    d['deductible'] = '1000'
  else:
    app.logger.error('Unrecognized purchase category: %s' % cat)
    raise Exception('Unrecognized purchase category: %s' % cat)
  return d


def get_price_of_user_form(data, use_memorized_only, l_config=None):
  renter_form_dict = data['renter_form']
  # Fill out the entire renter form.
  defaults = ExpandDefaults(renter_form_dict['purchase_category'])
  renter_form_dict.update(defaults)

  # Create config to pass into renter serving scorer.
  # Change directories so that we can properly access the files.
  # Right now they are set up to be relative to the engine
  if l_config is None:
    l_config = renter_constants.learned_config2
    model_cfg.change_dirs('../price_engine/models', l_config.model_configs)
  price = renters_serving_scorer.get_price(l_config, renter_form_dict, use_memorized_only)
  return price

def get_three_prices(data, use_memorized_only):
  """
    Get three prices returns the price engine for each of the three prices.
  """
  categories = ['cheap', 'medium', 'deluxe']
  d = {}
  for cat in categories:
    # Generate three prices.
    cat_data = copy.deepcopy(data)
    cat_data['renter_form']['purchase_category'] = cat
    price = get_price_of_user_form(cat_data, use_memorized_only)
    d[cat] = '%f' % (price)
  return d

@app.route('/three_prices', methods=['POST'])
def three_prices():
    """
      When the user wants to know three options.
    """
    try:
      d = get_three_prices(request.get_json(), config.use_memorized_only)
      return jsonify(prices=d)
    except Exception as e:
      line = traceback.format_exc()
      return line

@app.route('/price', methods=['POST'])
def price():
    """
      When the user wants to know what is the estimated price of
      their insurance policy.
    """
    try:
      data = request.get_json()
      price = get_price_of_user_form(data, config.use_memorized_only)
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
      token = None
      if data.get('payment_form', None):
          payment_form = data['payment_form']
          # Store payment information, get token and save it into renter_form_dict.
          headers = {'content-type': 'application/json'}

          try:
              r = requests.post(config.payment_endpoint, data=json.dumps(payment_form), headers=headers)
              result = r.json()
              if result['status'] == 'success':
                  app.logger.info("Success to store credit card info.")
                  token = result['token']
              else:
                  app.logger.error("Fail to store credicard. {message}".format(**result) )
                  return jsonify(status='fail', message="Invalid Credit Card Information")
          except Exception as e:
              app.logger.error("Fail to connect to payment service. %s" % e)

      memorized_price = get_price_of_user_form(data, use_memorized_only=True)
      app.logger.info("Get price of the form")
      # Expand defaults so we know what we are assuming.
      renter_form_dict = data['renter_form']
      defaults = ExpandDefaults(renter_form_dict['purchase_category'])
      renter_form_dict.update(defaults)
      # Log whatever price we have calculated here.
      renter_form_dict['policy_price'] = '$%.2f' % (memorized_price)
      learned_price = get_price_of_user_form(data, use_memorized_only=False)
      renter_form_dict['learned_policy_price'] = '$%.2f' % (learned_price)

      # Payment information
      renter_form = RenterForm(**renter_form_dict)
      renter_form.token = token
      renter_form.save()
      app.logger.info("Save the form to database")
      util.send_email(renter_form.email_address, 'Thank You for Trusting! Confirmation for Your Purchase!',
                      'email/confirmation.html', 'email/confirmation.txt', **renter_form_dict)
      return jsonify(status='success')

    except Exception as e:
      print(e)
      line = traceback.format_exc()
      return jsonify(status='fail', message=line)

@app.errorhandler(404)
def page_not_found(e):
    return util.render_common_template('errors/404.html'), 404

@app.errorhandler(Exception)
def handle_exception(error):
    app.logger.error(str(error))
    return util.render_common_template('errors/500.html', err_msg=repr(error))


if __name__ == '__main__':
    logging.basicConfig()
    if config.DEBUG:
        app.logger.setLevel(logging.DEBUG)
        app.run(debug=True, host='0.0.0.0', port=8080)
    elif config.PROD:
        app.logger.setLevel(logging.ERROR)
        from gevent.wsgi import WSGIServer

        http_server = WSGIServer(('0.0.0.0', 80), app)
        http_server.serve_forever()
