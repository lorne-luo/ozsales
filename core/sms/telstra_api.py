import os
import pycurl
import datetime
import json
import logging
from urllib import urlencode
from StringIO import StringIO
from django.conf import settings

log = logging.getLogger(__name__)


class MessageSender(object):
    CONSUMER_KEY = "ZDuzM5gKWl9IM8G4e0VMH2bKorRIU33t"
    CONSUMER_SECRET = "AUbyh8CJy8gASog1"
    AUTH_URL = 'https://api.telstra.com/v1/oauth/token'
    SEND_URL = 'https://api.telstra.com/v1/sms/messages'
    TOKEN = None
    TOKEN_EXPIRY = datetime.datetime.now()
    _instance = None
    LENGTH_PER_SMS = 160
    SMS_TXT_PATH = os.path.join(settings.MEDIA_ROOT, 'sms.txt')

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MessageSender, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def clean_content(self, content):
        content = unicode(content)
        content = content.replace('%', 'percent')
        if len(content) > MessageSender.LENGTH_PER_SMS:
            content = content[:MessageSender.LENGTH_PER_SMS]
        return content

    def get_token(self):
        buffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, MessageSender.AUTH_URL)

        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/x-www-form-urlencoded'])
        post_data = {'client_id': MessageSender.CONSUMER_KEY, 'client_secret': MessageSender.CONSUMER_SECRET,
                     'grant_type': 'client_credentials', 'scope': 'SMS'}
        c.setopt(pycurl.POST, 1)
        c.setopt(c.POSTFIELDS, urlencode(post_data))
        c.setopt(c.WRITEFUNCTION, buffer.write)
        c.perform()

        response = buffer.getvalue().decode('utf-8')
        # print response
        data = json.loads(response)
        MessageSender.TOKEN = str(data['access_token'])
        sec = int(data['expires_in'])
        MessageSender.TOKEN_EXPIRY = datetime.datetime.now() + datetime.timedelta(seconds=sec)
        # log.info(MessageSender.TOKEN, MessageSender.TOKEN_EXPIRY)

    def send_sms(self, to, content):
        if MessageSender.TOKEN_EXPIRY <= datetime.datetime.now() or not MessageSender.TOKEN:
            self.get_token()

        buffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, MessageSender.SEND_URL)

        content = self.clean_content(content)
        c.setopt(pycurl.HTTPHEADER, ['Authorization: Bearer %s' % MessageSender.TOKEN])
        post_dict = {'to': unicode(to), 'body': unicode(content)}
        post_data = json.dumps(post_dict)
        c.setopt(pycurl.POST, 1)
        c.setopt(c.POSTFIELDS, post_data)
        c.setopt(c.WRITEFUNCTION, buffer.write)
        c.perform()

        response = buffer.getvalue().decode('utf-8')
        # log.info('Response = ' % response)
        data = json.loads(response)
        if 'messageId' in data:
            return True, data['messageId']
        elif 'status' in data:
            return False, data['status']

    def send_to_self(self, content):
        my_number = '0413725868'
        try:
            with open(self.SMS_TXT_PATH, 'r+') as f:
                all_content = f.read()
                f.seek(0, 0)
                f.write('%s\n\n%s' % (content[:500], all_content[:6000]))
        except Exception as e:
            log.info('[SMS] sms.txt error %s' % e.message)

        return self.send_sms(my_number, content)


if __name__ == '__main__':
    m = MessageSender()
    m.send_to_self('hello boy')
