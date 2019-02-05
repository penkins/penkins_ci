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


class ProjectsResource(Resource):
    def get(self):
        """list projects"""
        items = []
        pattern = re.compile(r'^[a-zA-Z0-9]{1,32}\.yml$')
        for root, dirs, files in os.walk("./ci"):
            for filename in files:
                if pattern.match(filename):
                    items.append(filename)
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

        if len(db.search(Query().name == name)) == 0:
            db.insert(request.json)
        else:
            return {'status': {'code': 1, 'message': 'already exists'}}
        return {'status': {'code': 0, 'message': 'success'}}
