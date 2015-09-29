import datetime, logging, sys
from flask import Flask, render_template, json, jsonify, request, send_from_directory
import util

from logging import StreamHandler
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

# payment messages

SUCCESS_MSG = 'Thanks for the subsription. We will let you know when we launch!'
MISS_EMAIL_MSG = 'Sorry, email is required for subscription.'
ALREADY_SUBSCRIBED_MSG = "Thanks, you have already placed your deposit with this email."

# Displaying templates.

@app.route('/')
def home_page():
    return util.render_common_template('index.html')

@app.route('/test')
def test_page():
    return util.render_common_template('test.html')

@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('assets', path)

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

@app.route('/price')
def price():
    price = renters_serving_scorer.get_price({})
    return '%f' % (price)
    #return util.render_common_template('about.html')

#first name, last name, address, phone number, dob
@app.route('/buy', methods=['POST'])
def buy():
    data = request.get_json()
    app.logger.error(data)
    renter_form = data['renter_form']
    #payment = data['payment']
    form = RenterForm(**renter_form)
    form.save()
    return jsonify(status='done')
    #return util.render_common_template('about.html')

@app.route('/error', methods=['GET'])
def error():
    raise Exception('shit', status_code=500)

@app.errorhandler(404)
def page_not_found(e):
    return util.render_common_template('errors/404.html'), 404

@app.errorhandler(Exception)
def handle_exception(error):
    return util.render_common_template('errors/500.html', err_msg=repr(error))


if __name__ == '__main__':
    if config.DEBUG:
        app.logger.setLevel(logging.DEBUG)
        app.run(debug=True, host='0.0.0.0', port=8080)
    elif config.PROD:
        app.logger.setLevel(logging.ERROR)
        from gevent.wsgi import WSGIServer

        http_server = WSGIServer(('', 80), app)
        http_server.serve_forever()
