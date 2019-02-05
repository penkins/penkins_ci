#!/usr/bin/env python

import re
import os
import sys
import subprocess
import logging

import yaml
from flask import Flask, request
from flask_restful import Api, Resource

import jsonschema

from penkins import PenkinsConfig
from penkins import PenkinsMail
from penkins.db import db, Query
from penkins.resources import ProjectsResource, ProjectResource, BuildResource


app = Flask(__name__)

api = Api(app)

# projects
api.add_resource(ProjectsResource, '/')
api.add_resource(ProjectResource, '/<name>')
# build
api.add_resource(BuildResource, '/<name>/build')


if __name__ == '__main__':
    app.run(debug=True)
