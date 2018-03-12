# -*- coding: utf-8 -*-
from celery.task import task
from .smtp import send_email


@task
def email_send_task(receivers, subject, html_content, text_content=None):
    subject = subject.encode('utf-8')
    html_content = html_content.encode('utf-8')
    if text_content is not None:
        text_content = text_content.encode('utf-8')

    send_email(receivers, subject, html_content, text_content)
