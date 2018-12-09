# -*- coding: utf-8 -*-
from celery.task import task
from .smtp import send_email


@task
def email_send_task(receivers, subject, html_content, text_content=None):
    subject = subject
    html_content = html_content
    if text_content is not None:
        text_content = text_content

    send_email(receivers, subject, html_content, text_content)
