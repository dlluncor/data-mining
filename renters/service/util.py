import random
from flask import render_template
from config import config

def render_common_template(template_name, **kwargs):
    return render_template(template_name, apis=config.apis, **kwargs)
