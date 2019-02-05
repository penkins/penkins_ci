
import smtplib
import yaml
import os
import datetime


class PenkinsConfig(object):
    def __init__(self, config_file):
        self.config = self.__read(config_file)

    def __read(self, config_file):
        if os.path.isfile(config_file):
            config = yaml.load(open(config_file, 'r'))
        return config
