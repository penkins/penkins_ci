#!/usr/bin/env python

import git
import yaml
import BaseHTTPServer
import os
import sys
import subprocess
import logging
from penkins import PenkinsConfig
from penkins import PenkinsMail


class PenkinsWebServer(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
        self.action()

    def do_GET(self):
        """
        respond to a GET-request
        """
        self.action()

    def action(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        project_name = self.path[1:]
        # self.wfile.write(self.path[1:])

        if os.path.isfile('ci/%s.yaml' % project_name):
            task = yaml.load(open('ci/%s.yaml' % project_name, 'r'))
            # print task

            if task['work'] == 'build':
                if 'build_count' in task:
                    task['build_count'] += 1
                else:
                    task['build_count'] = 1

                # TODO: execute commands 'before'

                git.Git().clone(task['repository'], "%s/%s/%s" % (task['path'], project_name, task['build_count']))
                # print "clone"

                # TODO: execute commands 'after'
            elif task['work'] == 'update':
                # TODO: execute commands 'before'

                log = git.cmd.Git(task['path']).pull()

                PenkinsMail().send_mail(task['email'], 'project %s has pulled' % task['name'], log)

                # log_file = open('log/%s.log' % project_name, 'w')
                # log_file.write(log)
                # log_file.write('\n---\n')
                # log_file.close()

                # TODO: execute commands 'after'

            y_doc = open('ci/%s.yaml' % project_name, 'w')
            y_doc.write(yaml.dump(task))
            y_doc.close()
        else:
            logging.error('project %s not found' % project_name)


if __name__ == '__main__':
    # TODO: add conditions
    # if sys.argv[2]:
    #     if os.path.isfile(sys.argv[2]):
    #         logging.debug('config: %s' % sys.argv[2])
    #         config_file = sys.argv[2]
    #     else:
    #         logging.debug('config: %s' % sys.argv[2])
    #         config_file = '.penkins.yaml'
    #
    #     # check exists config file
    #     if not os.path.isfile(sys.argv[2]):
    #         logging.error('config: %s not exists' % sys.argv[2])

    config = PenkinsConfig('.penkins.yaml')

    logging.basicConfig(filename='log/debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.debug('start web server: %s:%s' % (config.config['web'][0]['interface'], config.config['web'][0]['port']))

    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((config.config['web'][0]['interface'], config.config['web'][0]['port']), PenkinsWebServer)

    httpd.serve_forever()
    httpd.server_close()
