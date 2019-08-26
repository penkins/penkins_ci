import os
from flask import current_app
from tinydb import TinyDB, Query

db = TinyDB('{}/.penkins/projects.json'.format(os.path.expanduser('~')))
