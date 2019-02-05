
from flask_restful import Resource
from penkins.db import db, Query

class ProjectResource(Resource):
    def get(self, name):
        if not db.get(Query().name == name):
            return {'status': {'code': 2, 'message': 'not found'}}

        return {
            'item': db.get(Query().name == name)
        }

    # TODO: update

    def delete(self, name):
        """delete project and all builds"""
        if not db.get(Query().name == name):
            return {'status': {'code': 2, 'message': 'not found'}}
        db.remove(Query().name == name)
        # os.unlink('ci/{}.json'.format(name))
        return {'status': {'code': 0, 'message': 'success'}}

