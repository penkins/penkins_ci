
import smtplib
import yaml
import os
import datetime


class PenkinsConfig:
    def __init__(self, config):
        self.config = self.__read(config)

    def __read(self, config):
        if os.path.isfile(config):
            config = yaml.load(open(config, 'r'))
        return config
