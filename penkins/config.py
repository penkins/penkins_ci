
import smtplib
import yaml
import os
import datetime


class PenkinsConfig:
    def __init__(self, file_name='/var/lib/penkins/.penkins.yaml'):
        self.config = self.__read(file_name)

    def __read(self, config_file):
        if os.path.isfile('.penkins.yaml'):
            config = yaml.load(open('.penkins.yaml', 'r'))
        return config

