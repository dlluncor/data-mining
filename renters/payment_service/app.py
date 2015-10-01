import base64, datetime, json, logging, sys, util
from flask import Flask, json, jsonify, request
from logging import StreamHandler
from logging import Formatter
from config import config
from models import CreditCard
from mongoengine import ValidationError

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

@app.route('/credit_cards', methods=['POST'])
def credit_cards():
    data = request.get_json()
    card_info = data['encrypted_payment_form']

    if not card_info:
        return jsonify(status='fail',message='Empty Payment Information')

    card = CreditCard(card_info=card_info)
    try:
        card.save()
    except ValidationError as e:
        print(e)
        return jsonify(status='fail',message=str(e))
    return jsonify(status='success', token=card.token)

if __name__ == '__main__':
    if config.DEBUG:
        app.logger.setLevel(logging.DEBUG)
        app.run(debug=True, host='0.0.0.0', port=8888)
    elif config.PROD:
        app.logger.setLevel(logging.ERROR)
        from gevent.wsgi import WSGIServer

        http_server = WSGIServer(('0.0.0.0', 8888), app)
        http_server.serve_forever()
