import logging, random, sendgrid
from flask import render_template
from config import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
sg_client = sendgrid.SendGridClient(config.sendgrid_username, config.sendgrid_password)

def render_common_template(template_name, **kwargs):
    return render_template(template_name, apis=config.apis, **kwargs)


def send_email_message(receivers, body, message):
    try:
        logger.info("Sending email to {names} with body: {body}".format(names=str(receivers), body=body))
        status, msg = sg_client.send(message)
        return status, msg
    except sendgrid.SendGridClientError as e:
        logger.info("Fail to send email to {names}. Error:{error}".format(names=str(receivers), error=str(e)))
        return str(e), 'client error'
    except sendgrid.SendGridServerError as e:
        logger.info("Fail to send email to {names} with body: {body}".format(names=str(receiver), error=str(e)))
        return str(e), 'server error'

def send_simple_email(receivers, subject, body, from_person):
    if not config.enable_send_email:
        logger.info("Simple email not actually sent to {name} with body: {body}".format(name=str(receivers), body=body))
        return
    message = sendgrid.Mail()
    for receiver in receivers:
        message.add_to(receiver)
    message.set_from(from_person)
    message.set_subject(subject)
    message.set_text(body)
    return send_email_message(receivers, subject, message)


def send_email(receivers, subject, html_template, txt_template, **kwargs):
    if not config.enable_send_email:
        logger.info("Email not actually sent to {name} with template: {template}".format(name=str(receivers), template=html_template))
        return

    message = sendgrid.Mail()
    for receiver in receivers:
      message.add_to(receiver)
    message.set_from('haoran@rentsafe.co')
    message.set_subject(subject)
    message.set_html(render_template(html_template, **kwargs))
    message.set_text(render_template(txt_template, **kwargs))
    return send_email_message(receivers, html_template, message)

