from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

sign = Blueprint('sign', __name__, 
                template_folder='templates',
                static_folder='static')

@sign.route('/')
def home():
    return render_template('./sign/index.html')