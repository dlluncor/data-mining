import random
from flask import render_template
from config import config

def render_common_template(template_name, **kwargs):
	form_name, form_url = random.choice(config.weighted_forms)
	placeholders = [('subscription', 'Enter email to get our phone insurance market report'),
	                ('contact', 'Enter email to contact insurance expert')]
	has_example = random.choice([True, False])
	placeholder_name, placeholder_text = random.choice(placeholders)
	info = {
		'form_name': form_name,
		'form_url': form_url,
		'placeholder_name': placeholder_name,
		'placeholder_text': placeholder_text,
		'has_example': has_example,
	}
	return render_template(template_name, apis=config.apis, info=info, **kwargs)

def get_form_token(url):
	return url.split('/')[-1]
