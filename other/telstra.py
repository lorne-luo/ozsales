import pycurl
from urllib import urlencode
from StringIO import StringIO


CONSUMER_KEY = "ZDuzM5gKWl9IM8G4e0VMH2bKorRIU33t"
CONSUMER_SECRET = "AUbyh8CJy8gASog1"

# buffer = StringIO()
# c = pycurl.Curl()
# c.setopt(c.URL, 'https://api.telstra.com/v1/oauth/token')
#
# c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/x-www-form-urlencoded'])
# post_data = {'client_id': CONSUMER_KEY, 'client_secret': CONSUMER_SECRET,
# 'grant_type': 'client_credentials', 'scope': 'SMS'}
# c.setopt(pycurl.POST, 1)
# c.setopt(c.POSTFIELDS, urlencode(post_data))
# c.setopt(c.WRITEFUNCTION, buffer.write)
# c.perform()
#
# body = buffer.getvalue()
# print(body.decode('iso-8859-1'))


RECIPIENT_NUMBER = "0478543891"
TOKEN = "7mf8X7yseSvgfMDV18dBA2fxvtub"
CONTENT = 'HELLO BODY'

# curl -H "Content-Type: application/json" \
# -H "Authorization: Bearer $TOKEN" \
# -d "{\"to\":\"$RECIPIENT_NUMBER\", \"body\":\"Hello!\"}" \
# "https://api.telstra.com/v1/sms/messages"

buffer = StringIO()
c = pycurl.Curl()
c.setopt(c.URL, 'https://api.telstra.com/v1/sms/messages')

c.setopt(pycurl.HTTPHEADER, ['Authorization: Bearer %s' % TOKEN])
post_data = '{\"to\":\"%s\", \"body\":\"%s\"}' % (RECIPIENT_NUMBER, CONTENT)
c.setopt(pycurl.POST, 1)
c.setopt(c.POSTFIELDS, post_data)
c.setopt(c.WRITEFUNCTION, buffer.write)
c.perform()

body = buffer.getvalue()
print(body.decode('iso-8859-1'))
