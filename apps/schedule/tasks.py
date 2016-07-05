# -*- coding: utf-8 -*-
import urllib2
import redis
import pytz
import logging
import datetime
from dateutil import parser
from bs4 import BeautifulSoup
from celery.task import periodic_task
from celery.task.schedules import crontab
from utils.telstra_api import MessageSender

log = logging.getLogger(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)

ozbargin_last_date = 'schedule.ozbargin.last_date'
ozbargin_keywords = ['citibank', 'anz', 'cba', 'nab', 'westpac', 'fee for life',
                     'Trifecta', 'filco', 'bose', 'headphone']


def get_rss(url):
    return urllib2.urlopen(urllib2.Request(url))


def utf8len(s):
    return len(s.encode('utf-8')) if isinstance(s, unicode) else len(s)


def utf8sub(s, length):
    length = int(length / 3) if isinstance(s, unicode) else length
    return s[:length]


@periodic_task(run_every=crontab(minute='*/15', hour='8-23'))
def ozbargin_task():
    url = 'https://www.ozbargain.com.au/feed'
    all_deals_url = 'https://www.ozbargain.com.au/deals/feed'

    if not ozbargin_keywords:
        return

    data = urllib2.urlopen(urllib2.Request(all_deals_url))
    soup = BeautifulSoup(data, "html.parser")
    items = soup.find_all("item")
    last_date_str = r.get(ozbargin_last_date)
    last_date = parser.parse(last_date_str) if last_date_str else datetime.datetime(2016, 1, 1, 0, 0)
    new_last_date = last_date

    for item in reversed(items):
        title = item.title.text
        description = item.description.text
        link = item.link.text
        meta = item.find('ozb:meta')
        click_count = meta['click-count']
        try:
            votes_pos = int(meta['votes-pos'])
        except:
            votes_pos = 0
        org_url = meta['url']
        pub_date = item.pubdate.text

        try:
            item_date = parser.parse(pub_date)
        except:
            log.info('[Item Parsing] date parsing failed: %s' % pub_date)
            continue
        # print comment_count, title, item_date

        # convert aware and naive time
        if item_date.tzinfo and not last_date.tzinfo:
            last_date = last_date.replace(tzinfo=pytz.UTC)
        elif not item_date.tzinfo and last_date.tzinfo:
            last_date = last_date.replace(tzinfo=None)

        if item_date < last_date:
            continue
        elif item_date > new_last_date:
            new_last_date = item_date

        # check keywords
        flag = False
        for key in ozbargin_keywords:
            if key.lower() in title.lower() or votes_pos > 30:
                if votes_pos > 30:
                    title = '* %s' % title
                flag = True
                break

        if flag:
            text_list = BeautifulSoup(description, "html.parser").findAll(text=True)
            description = ' '.join(x.strip() for x in text_list)
            summary = '[%s]%s\n%s\n' % (item_date.strftime('%H:%M'), title, link)
            content = summary + description
            sender = MessageSender()
            result, detail = sender.send_to_self(content)
            # print 'sending', content
            log.info('[SMS] success=%s,%s. %s' % (result, detail, summary))

    r.set(ozbargin_last_date, new_last_date)


smzdm_last_date = 'schedule.smzdm.last_date'
smzdm_keywords = [u'蓝牙耳机', u'无线耳机']


@periodic_task(run_every=crontab(minute='*/15', hour='8-23'))
def smzdm_task():
    url = 'http://feed.smzdm.com/'
    haitao_url = 'http://haitao.smzdm.com/feed'

    if not smzdm_keywords:
        return

    req = urllib2.Request(haitao_url, headers={'User-Agent': "Magic Browser"})
    data = urllib2.urlopen(req)
    soup = BeautifulSoup(data, "html.parser")
    items = soup.find_all("item")
    last_date_str = r.get(smzdm_last_date)
    last_date = parser.parse(last_date_str) if last_date_str else datetime.datetime(2016, 1, 1, 0, 0)
    new_last_date = last_date

    for item in reversed(items):
        title = item.title.text
        link = item.link.text
        description = item.description.text
        pub_date = item.pubdate.text

        try:
            item_date = parser.parse(pub_date)
        except:
            log.info('[Item Parsing] date parsing failed: %s' % pub_date)
            continue
        # print title, item_date
        # print link

        # convert aware and naive time
        if item_date.tzinfo and not last_date.tzinfo:
            last_date = last_date.replace(tzinfo=pytz.UTC)
        elif not item_date.tzinfo and last_date.tzinfo:
            last_date = last_date.replace(tzinfo=None)

        if item_date < last_date:
            continue
        elif item_date > new_last_date:
            new_last_date = item_date

        # check keywords
        flag = False
        for key in smzdm_keywords:
            if key.lower() in title.lower():
                flag = True
                break

        if flag:
            text_list = BeautifulSoup(description, "html.parser").findAll(text=True)
            description = ' '.join(x.strip() for x in text_list)
            summary = '[%s]%s\n%s\n' % (item_date.strftime('%H:%M'), title, link)
            content = summary + description
            sender = MessageSender()
            result, detail = sender.send_to_self(content)
            # print 'sending', content
            log.info('[SMS] success=%s,%s. %s' % (result, detail, summary))

    r.set(smzdm_last_date, new_last_date)
