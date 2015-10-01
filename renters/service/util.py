import random
from flask import render_template
from config import config

def render_common_template(template_name, **kwargs):
	placeholders = [('subscription', 'Enter email to get our phone insurance market report'),
	                ('contact', 'Enter email to contact insurance expert')]
	has_example = random.choice([True, False])
	placeholder_name, placeholder_text = random.choice(placeholders)
	return render_template(template_name, apis=config.apis, **kwargs)

def get_form_token(url):
	return url.split('/')[-1]
