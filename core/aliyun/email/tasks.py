# -*- coding: utf-8 -*-
from celery.task import task
from .smtp import send_email


@task
def email_send_task(receivers, subject, html_content, text_content=None):
    send_email(receivers, subject, html_content, text_content)
