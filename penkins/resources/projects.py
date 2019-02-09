import re
import os
import sys
import subprocess
import logging

import git
import yaml
from flask import request
from flask_restful import Resource
from tinydb import TinyDB, Query
import jsonschema

from penkins import PenkinsConfig
from penkins import PenkinsMail
from penkins.db import db, Query
from penkins.controller import Projects


class ProjectsResource(Resource):
    def get(self):
        """list projects"""
        items = Projects().get_all()
        return {
            'items': items,
            'total': len(items)
        }

    def post(self):
        """Create new project

        {
            "name": "test1",
            "vcs": "git",
            "repository": "git@github.com:vanzhiganov/penka.git",
            "branch": ""
            ""
        }
        """
        try:
            jsonschema.validate(
                request.json,
                {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string"
                            # TODO: regex
                        },
                        "vcs": {"type": "string"},
                        "repository": {"type": "string"},
                    },
                    "required": [
                        "name", "vcs", "repository"
                    ]
                }
            )
        except Exception as e:
            print(e)
            return {}

        name = request.json.get('name')

        pr = Projects()

        if not pr.validate_name(name):
            return {'status': {'code': 2, 'mesage': 'invalid project name format'}}

        if not pr.is_exists(name):
            db.insert(request.json)
        else:
            return {'status': {'code': 1, 'message': 'already exists'}}
        return {'status': {'code': 0, 'message': 'success'}}
