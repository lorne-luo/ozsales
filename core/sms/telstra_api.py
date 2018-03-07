import os
import pycurl
import datetime
import json
import redis
import logging
from urllib import urlencode
from StringIO import StringIO
from django.conf import settings
from .models import Sms

log = logging.getLogger(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)
TELSTRA_SMS_MONTHLY_COUNTER = 'TELSTRA_SMS_MONTHLY_COUNTER'


class MessageSender(object):
    CONSUMER_KEY = settings.TELSTRA_CONSUMER_KEY
    CONSUMER_SECRET = settings.TELSTRA_CONSUMER_SECRET
    AUTH_URL = 'https://api.telstra.com/v1/oauth/token'
    SEND_URL = 'https://api.telstra.com/v1/sms/messages'
    TOKEN = None
    TOKEN_EXPIRY = datetime.datetime.now()
    _instance = None
    LENGTH_PER_SMS = 160

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

    def send_sms(self, to, content, app_name=None):
        counter = r.get(TELSTRA_SMS_MONTHLY_COUNTER) or 0
        counter = int(counter)
        if not counter < 1000:
            log.info('[SMS] Telstra SMS reach 1000 free limitation.')
            return False, 'Telstra SMS reach 1000 free limitation.'

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

        sms = Sms(app_name=app_name, send_to=to, content=content)
        if 'messageId' in data:
            sms.success = True
            counter += 1
            r.set(TELSTRA_SMS_MONTHLY_COUNTER, counter)
            sms.save()
            if counter == 999:
                self.send_to_admin('[Warning] Telstra sms meet monthly limitation.')
            return True, data['messageId']
        elif 'status' in data:
            sms.success = False
            sms.save()
            return False, data['status']

    def send_to_admin(self, content, app_name=None):
        return self.send_sms(settings.ADMIN_MOBILE_NUMBER, content, app_name)


# singleton pattern
telstra_sender = MessageSender()

# if __name__ == '__main__':
#     m = MessageSender()
#     m.send_to_admin('hello boy')
