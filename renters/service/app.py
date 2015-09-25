import datetime, logging, sys
import util
from flask import render_template
from logging import StreamHandler
from flask import Flask, request, json, jsonify
from models import Subscription, Feedback, Contact
from config import config
from errors import ChargeException
from helper import *

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
def landing_page():
    return util.render_common_template('index.html')

# Sending assets.

from flask import Flask, request, send_from_directory

@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('assets', path)

@app.route('/tos')
def tos():
    return util.render_common_template('tos.html')

@app.route('/privacy_policy')
def privacy_policy():
    return util.render_common_template('privacy_policy.html')

@app.route('/about')
def about():
    return util.render_common_template('about.html')
# Actual handlers

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email', None)

    if not email:
        return jsonify(status='fail', msg=MISS_EMAIL_MSG)

    if not Subscription.is_exist(email):
        sub = Subscription()
        sub.email = email
        sub.save()

        return jsonify(status='success', msg=SUCCESS_MSG)

    return jsonify(status='warn', msg=ALREADY_SUBSCRIBED_MSG)

@app.route('/feedback', methods=['POST'])
def feedback():
    email = request.form.get('email', None)
    comment = request.form.get('comment', None)

    if not email:
        return jsonify(status='fail', msg=MISS_EMAIL_MSG)

    fb = Feedback()
    fb.email = email
    fb.comment = comment
    fb.save()

    return jsonify(status='success', msg=SUCCESS_MSG)

@app.route('/error', methods=['GET'])
def error():
    raise Exception('shit', status_code=500)

@app.errorhandler(404)
def page_not_found(e):
    return util.render_common_template('errors/404.html'), 404

@app.errorhandler(Exception)
def handle_exception(error):
    return util.render_common_template('errors/500.html', err_msg=repr(error))

@app.route('/phone_ins_form_completed', methods=['POST'])
def phone_ins_form_completed():
    q = request.form.get('q')
    return jsonify(status='success', q=q)

@app.route('/insurance-exchange', methods=['GET'])
@crossdomain(origin='*')
def insurance_exchange():
    return jsonify(name='Loss/Theft Insurance', price='$7.99/month', description='Reduce you loss~enjoy your life.')

@app.route('/contacts', methods=['POST'])
@crossdomain(origin='*')
def contacts():
    email = request.form.get('email')
    contact = Contact.get_by(email)
    if contact:
        return jsonify(status='warn', msg='You have already submited your address.')

    try:
        contact = Contact()

        contact.email = email;

        contact.first_name = request.form.get('firstName')
        contact.last_name = request.form.get('lastName')

        contact.address_line_1 = request.form.get('addressLine1')
        contact.address_line_2 = request.form.get('addressLine2')

        contact.city = request.form.get('city')
        contact.state = request.form.get('state')
        contact.zip_code = request.form.get('zipCode')
        contact.phone_number = request.form.get('phoneNumber')

        contact.save()

    except Exception as e:
        print("Ooops! got an error -> %s" % e)
        return jsonify(status='fail', msg='Ooops, some error occurs. Please call us to get a shipping box.')

    print("success for [%s]" % email)
    return jsonify(status='success', msg='Thank you! We will send you a shipping box as soon as possible.')

if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=8080)
