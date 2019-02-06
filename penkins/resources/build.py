import os
import git
import subprocess
from flask_restful import Resource
from penkins.db import db, Query, TinyDB
from tinydb.operations import increment
from penkins.config import PenkinsConfig


class BuildResource(Resource):
    def get(self, name):
        project = db.get(Query().name == name)

        if not os.path.exists('builds/{}'.format(name)):
            os.mkdir('builds/{}'.format(name))
        if not os.path.exists('builds/{}'.format(name)):
            os.mkdir('builds/{}'.format(name))

        is_init = os.path.exists('builds/{}/builds.json'.format(name))

        dbbuils = TinyDB('builds/{}/builds.json'.format(name))

        if is_init:
            dbbuils.insert({'counter': 0})

        dbbuils.update(increment('counter'))

        build_id = dbbuils.get(Query().counter).get('counter')

        if os.path.exists('builds/{}/{}'.format(name, build_id)):
            os.rmdir('builds/{}/{}'.format(name, build_id))
        if not os.path.exists('builds/{}/{}'.format(name, build_id)):
            os.mkdir('builds/{}/{}'.format(name, build_id))
            os.mkdir('builds/{}/{}/build'.format(name, build_id))

        if project.get('vcs') == "git":
            g1 = git.Git('builds/{}/{}/build/'.format(name, build_id))
            g1.clone(project.get('repository'), '.')

        # Read .penkins-ci.yml file
        # https://docs.gitlab.com/ee/ci/yaml/
        if os.path.exists('builds/{}/{}/build/.penkins.yml'.format(name, build_id)):
            pc = PenkinsConfig('builds/{}/{}/build/.penkins.yml'.format(name, build_id)).config
            print(pc)
            # scripts
            for cmd in pc.get('script'):
                subprocess.call(cmd.split(' '), cwd='builds/{}/{}/build/'.format(name, build_id), shell=True)
        return {
            'project_name': name
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

        # y_doc = open('ci/%s.yaml' % project_name, 'w')
        # y_doc.write(yaml.dump(task))
        # y_doc.close()

        # return {
        #     'project_name': project_name
        # }
