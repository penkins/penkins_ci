
import re
from penkins.db import db, Query


class Projects(object):
    def get_all(self):
        return db.all()

    def is_exists(self, name):
        return False if len(db.search(Query().name == name)) == 0 else True

    def get(self):
        pass

    def validate_name(self, name):
        pattern = re.compile(r'^[a-zA-Z0-9]{1,32}$')
        return True if pattern.match(name) else False
