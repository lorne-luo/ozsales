# coding=utf-8
from django.apps import AppConfig

__author__ = 'Lorne'


class MessageAppConfig(AppConfig):
    name = "core.messageset"
    verbose_name = u"消息中心"

    def ready(self):
        pass