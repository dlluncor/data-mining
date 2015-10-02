import logging, random, sendgrid
from flask import render_template
from config import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
sg_client = sendgrid.SendGridClient(config.sendgrid_username, config.sendgrid_password)

def render_common_template(template_name, **kwargs):
    return render_template(template_name, apis=config.apis, **kwargs)

def send_email(receiver, subject, html_template, txt_template, **kwargs):
    if not config.enable_send_email:
        logger.info("Email not actually send to {name} with template: {template}".format(name=first_name, template=html_template))
        return

    message = sendgrid.Mail()
    message.add_to(receiver)
    message.set_from('haoran@rentsafe.co')
    message.set_subject(subject)
    message.set_html(render_template(html_template, **kwargs))
    message.set_text(render_template(txt_template, **kwargs))

    try:
        logger.info("Sending email to {name} with template: {template}".format(name=receiver, template=html_template))
        status, msg = sg_client.send(message)
        return status, msg
    except sendgrid.SendGridClientError as e:
        logger.info("Fail to send email to {name}. Error:{error}".format(name=receiver, error=str(e)))
        return str(e), 'client error'
    except sendgrid.SendGridServerError as e:
        logger.info("Fail to send email to {name} with template: {template}".format(name=receiver, error=str(e)))
        return str(e), 'server error'
