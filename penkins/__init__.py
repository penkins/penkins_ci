
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


class PenkinsMail(PenkinsConfig):
    def send_mail(self, to, subject, message):
        smtp_config = PenkinsConfig().config['smtp'][0]

        smtpserver = smtplib.SMTP(smtp_config['host'], smtp_config['port'])
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(smtp_config['login'], smtp_config['password'])

        smtpserver.sendmail(smtp_config['email'], to, self.message(smtp_config['email'], to, subject, message))
        smtpserver.close()
        return None

    def message(self, sender, to, subject, message):
        date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        # message_text = "Hello\nThis is a mail from your server\n\nBye\n"

        return "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (sender, to, subject, date, message)


# PenkinsMail().send_mail('user@yandex.ru', 'efef', 'wdwd')
