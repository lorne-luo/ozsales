# -*- coding:utf-8 -*-
import logging
import redis
import smtplib
import email
from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

log = logging.getLogger(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)  # todo move it into settings
ALIYUN_EMAIL_DAILY_COUNTER = 'ALIYUN_EMAIL_DAILY_COUNTER'

ALIYUN_EMAIL_HOST = settings.ALIYUN_EMAIL_HOST  # smtp server address
ADMIN_EMAIL = settings.ADMIN_EMAIL  # 管理员地址
SITE_NAME = settings.SITE_NAME  # 自定义的发件人名称
# 单一发信地址
SINGLE_EMAIL_USERNAME = settings.ALIYUN_SINGLE_EMAIL_USERNAME  # 发件人地址，通过控制台创建的发件人地址
SINGLE_EMAIL_PASSWORD = settings.ALIYUN_SINGLE_EMAIL_PASSWORD  # 发件人密码，通过控制台创建的发件人密码
# 批量发信地址
BATCH_EMAIL_USERNAME = settings.ALIYUN_BATCH_EMAIL_USERNAME
BATCH_EMAIL_PASSWORD = settings.ALIYUN_BATCH_EMAIL_PASSWORD

ALIYUN_EMAIL_DAILY_FREE_LIMIT = 200


def _send_email(receivers, subject, html_content, text_content=None):
    if isinstance(receivers, str):
        username = SINGLE_EMAIL_USERNAME
        password = SINGLE_EMAIL_PASSWORD
    else:
        username = BATCH_EMAIL_USERNAME
        password = BATCH_EMAIL_PASSWORD

    # 构建alternative结构
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header(subject.decode('utf-8')).encode()
    msg['From'] = '%s <%s>' % (Header(SITE_NAME.decode('utf-8')).encode(), username)
    msg['To'] = ';'.join(receivers) if isinstance(receivers, list) else receivers
    msg['Reply-to'] = ADMIN_EMAIL
    msg['Message-id'] = email.utils.make_msgid()
    msg['Date'] = email.utils.formatdate()
    # 构建alternative的text/plain部分
    textplain = MIMEText(text_content or html_content, _subtype='plain', _charset='UTF-8')
    msg.attach(textplain)
    # 构建alternative的text/html部分
    texthtml = MIMEText(html_content, _subtype='html', _charset='UTF-8')
    msg.attach(texthtml)
    # 发送邮件
    try:
        # 必须使用SSL，端口465
        client = smtplib.SMTP_SSL()
        host = ALIYUN_EMAIL_HOST
        client.connect(host, 465)
        # 开启DEBUG模式
        # client.set_debuglevel(0)
        client.login(username, password)
        # 发件人和认证地址必须一致
        # 备注：若想取到DATA命令返回值,可参考smtplib的sendmaili封装方法:
        #      使用SMTP.mail/SMTP.rcpt/SMTP.data方法
        client.sendmail(username, receivers, msg.as_string())
        client.quit()
        print ('邮件发送成功！')
    except smtplib.SMTPConnectError as e:
        print ('邮件发送失败，连接失败:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPAuthenticationError as e:
        print ('邮件发送失败，认证错误:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPSenderRefused as e:
        print ('邮件发送失败，发件人被拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPRecipientsRefused as e:
        print ('邮件发送失败，收件人被拒绝:', e.recipients, e.args)
    except smtplib.SMTPDataError as e:
        print ('邮件发送失败，数据接收拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPException as e:
        print ('邮件发送失败, ', e.message)
    except Exception as e:
        print ('邮件发送异常, ', str(e))


def send_email(receivers, subject, html_content, text_content=None):
    counter = r.get(ALIYUN_EMAIL_DAILY_COUNTER) or 0
    counter = int(counter)
    if counter == ALIYUN_EMAIL_DAILY_FREE_LIMIT - 1:
        msg = 'Aliyun email exceed %s daily free limitation.' % ALIYUN_EMAIL_DAILY_FREE_LIMIT
        _send_email([ADMIN_EMAIL], msg, msg)
        r.set(ALIYUN_EMAIL_DAILY_COUNTER, counter + 1)
    elif counter < ALIYUN_EMAIL_DAILY_FREE_LIMIT - 1:
        _send_email(receivers, subject, html_content, text_content)
        r.set(ALIYUN_EMAIL_DAILY_COUNTER, counter + 1)
    else:
        msg = 'Aliyun email exceed %s daily free limitation.' % ALIYUN_EMAIL_DAILY_FREE_LIMIT
        log.warning('[EMAIL SENDER] %s' % msg)
