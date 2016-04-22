import urllib2
from bs4 import BeautifulSoup
from celery import Celery
from django.conf import settings
from celery.task import periodic_task
from celery.task.schedules import crontab

strict_keywords = ['citibank']
loose_keywords = ['fee for life']


def ozbargin():
    url = 'https://www.ozbargain.com.au/deals/feed'
    all_deals_url = 'https://www.ozbargain.com.au/feed'
    data = urllib2.urlopen(urllib2.Request(url))
    soup = BeautifulSoup(data, "html.parser")
    items = soup.find_all("item")
    last_id = 0
    for item in items:
        title = item.title.text
        link = item.link.text
        meta = item.find('ozb:meta')
        click_count = meta['click-count']
        comment_count = meta['comment-count']
        org_url = meta['url']

        try:
            if link.find('/') > -1:
                id = link.split('/')[-1]
                id = int(id)
                if id > last_id:
                    last_id = id
                    # todo updae last id
        except:
            pass

        print id, title
        # print link
        # print click_count
        # print comment_count
        # print org_url
        print ''


ozbargin()


def smzdm():
    url = 'http://feed.smzdm.com/'
    haitao_url = 'http://haitao.smzdm.com/feed'
    req = urllib2.Request(haitao_url, headers={'User-Agent': "Magic Browser"})
    data = urllib2.urlopen(req)
    soup = BeautifulSoup(data, "html.parser")
    items = soup.find_all("item")
    last_id = 0
    for item in items:
        title = item.title.text
        link = item.link.text
        try:
            if link.strip('/').find('/') > -1:
                id = link.strip('/').split('/')[-1]
                id = int(id)
                if id > last_id:
                    last_id = id
                    # todo updae last id
        except:
            pass
        print id, title
        print link


smzdm()
