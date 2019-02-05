#!/usr/bin/env python

import re
import os
import sys
import subprocess
import logging

import git
import yaml
from flask import Flask, request
from flask_restful import Api, Resource
from tinydb import TinyDB, Query
import jsonschema

from penkins import PenkinsConfig
from penkins import PenkinsMail


db = TinyDB('ci/projects.json')


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


class BuildResource(Resource):
    def get(self, project_name):
        return {
            'project_name': project_name
        }

    def post(self, name):
        project = db.get(Query().name == name)
        if not project:
            return {}

        if project.vcs == "git":
            git.Git("ci/test1").clone("https://github.com/myscrapyard/test1.git")
        # elif task['vcs'] == "hg":
        #         # clone
        #         repo = hgapi.Repo(task['repository'])
        #         repo.hg_clone(task['repository'], "%s/%s/%s" % (task['path'], project_name, task['build_count']))
        #     print "clone"
        else:
            print("CVS engine not specified for this task")

        #     # TODO: execute commands 'after'
        # elif task['work'] == 'update':
        #     # TODO: execute commands 'before'

        #     if task['cvs'] == "git":
        #         log = git.cmd.Git(task['path']).pull()
        #     # elif task['cvs'] == "hg":
        #     #     # pull
        #     #     repo = hgapi.Repo(task['path'])
        #     #     repo.hg_pull(task['path'])
        #     else:
        #         print("CVS engine not specified for this task")

        #     PenkinsMail().send_mail(task['email'], 'project %s has pulled' % task['name'], log)

        #     # log_file = open('log/%s.log' % project_name, 'w')
        #     # log_file.write(log)
        #     # log_file.write('\n---\n')
        #     # log_file.close()

        #     # TODO: execute commands 'after'

        y_doc = open('ci/%s.yaml' % project_name, 'w')
        y_doc.write(yaml.dump(task))
        y_doc.close()

        return {
            'project_name': project_name
        }


app = Flask(__name__)

api = Api(app)

# projects
api.add_resource(ProjectsResource, '/')
api.add_resource(ProjectResource, '/<name>')
# build
api.add_resource(BuildResource, '/<name>/build')


if __name__ == '__main__':
    app.run(debug=True)
#     # TODO: add conditions
#     # if sys.argv[2]:
#     #     if os.path.isfile(sys.argv[2]):
#     #         logging.debug('config: %s' % sys.argv[2])
#     #         config_file = sys.argv[2]
#     #     else:
#     #         logging.debug('config: %s' % sys.argv[2])
#     #         config_file = '.penkins.yaml'
#     #
#     #     # check exists config file
#     #     if not os.path.isfile(sys.argv[2]):
#     #         logging.error('config: %s not exists' % sys.argv[2])

#     # TODO: add the ability to specified config file from CLI param
#     # TODO: check exists config file
#     config = PenkinsConfig('.penkins.yaml')

#     logging.basicConfig(filename='log/debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
#     logging.debug('start web server: %s:%s' % (config.config['web'][0]['interface'], config.config['web'][0]['port']))

#     server_class = BaseHTTPServer.HTTPServer
#     httpd = server_class((config.config['web'][0]['interface'], config.config['web'][0]['port']), PenkinsWebServer)

#     httpd.serve_forever()
#     httpd.server_close()
