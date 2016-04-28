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
                     'Trifecta', 'filco', 'dyson']


@periodic_task(run_every=crontab(minute='*/30', hour='7-22'))
def ozbargin():
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
        link = item.link.text
        meta = item.find('ozb:meta')
        click_count = meta['click-count']
        try:
            comment_count = int(meta['comment-count'])
        except:
            comment_count = 0
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
            if key.lower() in title.lower() or comment_count > 80:
                flag = True
                break

        if flag:
            content = '%s\n%s\n%s' % (pub_date, title, link)
            sender = MessageSender()
            sender.send_to_self(content)
            # print 'sending', content
            log.info('[SMS] %s' % content)

    r.set(ozbargin_last_date, new_last_date)


smzdm_last_date = 'schedule.smzdm.last_date'
smzdm_keywords = [u'羽绒服']


@periodic_task(run_every=crontab(minute='*/30', hour='8-23'))
def smzdm():
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
            content = '%s\n%s\n%s' % (pub_date, title, link)
            sender = MessageSender()
            sender.send_to_self(content)
            # print 'sending', content
            log.info('[SMS] %s' % content)

    r.set(smzdm_last_date, new_last_date)
