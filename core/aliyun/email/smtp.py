# -*- coding:utf-8 -*-
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.header import Header

ALIYUN_EMAIL_SYDNEY_HOST = 'smtpdm-ap-southeast-2.aliyun.com'
SENDER_EMAIL = 'dev@luotao.net'  # 自定义的回复地址
SENDER_NAME = 'Youdan Team'  # 自定义的发件人名称
# 单一发信地址
SINGLE_EMAIL_USERNAME = 'notice@em.luotao.net'  # 发件人地址，通过控制台创建的发件人地址
SINGLE_EMAIL_PASSWORD = 'nv98273rH12j3nF'  # 发件人密码，通过控制台创建的发件人密码
# 批量发信地址
BATCH_EMAIL_USERNAME = 'info@em.luotao.net'
BATCH_EMAIL_PASSWORD = 'nv98273rH12j3nF'


def send_email(receivers, subject, html_content, text_content=None):
    if isinstance(receivers, str):
        username = SINGLE_EMAIL_USERNAME
        password = SINGLE_EMAIL_PASSWORD
    else:
        username = BATCH_EMAIL_USERNAME
        password = BATCH_EMAIL_PASSWORD

    # 构建alternative结构
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header(subject.decode('utf-8')).encode()
    msg['From'] = '%s <%s>' % (Header(SENDER_NAME.decode('utf-8')).encode(), username)
    msg['To'] = receivers
    msg['Reply-to'] = SENDER_EMAIL
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
        host = ALIYUN_EMAIL_SYDNEY_HOST
        client.connect(host, 465)
        # 开启DEBUG模式
        # client.set_debuglevel(0)
        client.login(username, password)
        # 发件人和认证地址必须一致
        # 备注：若想取到DATA命令返回值,可参考smtplib的sendmaili封装方法:
        #      使用SMTP.mail/SMTP.rcpt/SMTP.data方法
        client.sendmail(username, SENDER_EMAIL, msg.as_string())
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
