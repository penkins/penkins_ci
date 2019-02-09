#!/usr/bin/env python
import os
from flask import Flask
from flask_restful import Api
# from penkins import PenkinsConfig, PenkinsMail
from penkins.views import IndexView
from penkins.resources import ProjectsResource, ProjectResource, BuildResource


app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
app.config['PENKINS_DIR'] = '{}/.penkins'.format(os.path.expanduser('~'))

api = Api(app)

app.register_blueprint(IndexView, url_prefix="")

# projects
api.add_resource(ProjectsResource, '/api/v1/')
api.add_resource(ProjectResource, '/api/v1/<name>')
# build
api.add_resource(BuildResource, '/api/v1/<name>/build')


if __name__ == '__main__':
    app.run(debug=True)
