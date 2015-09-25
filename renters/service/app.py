import datetime, logging, sys
from flask import Flask, render_template, json, jsonify, request, send_from_directory
import util

from logging import StreamHandler
from flask import Flask, request, json, jsonify
from config import config
from errors import ChargeException
from helper import *

#import sys
#sys.path.append("..")

import sys
sys.path.append("..") # Adds higher directory to python modules path.

from renters import place #renters import place #import hello

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

log_handler = StreamHandler(sys.stdout)
app.logger.setLevel(logging.INFO)
app.logger.addHandler(log_handler)

# payment messages

SUCCESS_MSG = 'Thanks for the subsription. We will let you know when we launch!'
MISS_EMAIL_MSG = 'Sorry, email is required for subscription.'
ALREADY_SUBSCRIBED_MSG = "Thanks, you have already placed your deposit with this email."

# Displaying templates.

@app.route('/')
def home_page():
    return util.render_common_template('index.html')

@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('assets', path)

@app.route('/terms')
def tos():
    return util.render_common_template('tos.html')

@app.route('/privacy_policy')
def privacy_policy():
    return util.render_common_template('privacy_policy.html')

@app.route('/about')
def about():
    return util.render_common_template('about.html')

@app.route('/price')
def about():
    return '%s' % (place.hello())
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
     app.run(debug=True, host='0.0.0.0', port=8080)
