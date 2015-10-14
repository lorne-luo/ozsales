import pycurl
import datetime
import json
from urllib import urlencode
from StringIO import StringIO

class MessageSender(object):
    CONSUMER_KEY = "ZDuzM5gKWl9IM8G4e0VMH2bKorRIU33t"
    CONSUMER_SECRET = "AUbyh8CJy8gASog1"
    AUTH_URL = 'https://api.telstra.com/v1/oauth/token'
    SEND_URL = 'https://api.telstra.com/v1/sms/messages'
    TOKEN = None
    TOKEN_EXPIRY = datetime.datetime.now()
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MessageSender, cls).__new__(cls, *args, **kwargs)
        return cls._instance

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
        print MessageSender.TOKEN, MessageSender.TOKEN_EXPIRY

    def send_sms(self, to, content):
        if MessageSender.TOKEN_EXPIRY <= datetime.datetime.now() or not MessageSender.TOKEN:
            self.get_token()

        buffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, MessageSender.SEND_URL)

        c.setopt(pycurl.HTTPHEADER, ['Authorization: Bearer %s' % MessageSender.TOKEN])
        post_dict = {'to': str(to), 'body': content}
        post_data = json.dumps(post_dict)
        c.setopt(pycurl.POST, 1)
        c.setopt(c.POSTFIELDS, post_data)
        c.setopt(c.WRITEFUNCTION, buffer.write)
        c.perform()

        response = buffer.getvalue().decode('utf-8')
        print response
        data = json.loads(response)
        msg_id = data['messageId']
        print msg_id


if __name__ == '__main__':
    m = MessageSender()
    m.send_sms('0478543891', 'hello boy')
