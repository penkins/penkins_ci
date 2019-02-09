from flask import Blueprint, render_template
from penkins.controller import Projects

IndexView = Blueprint('index', __name__)

@IndexView.route('/')
def index():
    return render_template('index.html', projects=Projects().get_all())
