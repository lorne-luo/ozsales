# -*- coding: utf-8 -*-
import datetime
import logging
import urllib2
import pytz
import redis
import python_forex_quotes
from django.utils import timezone
from django.conf import settings
from decimal import Decimal
from bs4 import BeautifulSoup
from celery.task import periodic_task
from celery.task.schedules import crontab
from dateutil import parser
from dateutil.relativedelta import relativedelta

from core.aliyun.email.smtp import ALIYUN_EMAIL_DAILY_COUNTER
from core.sms.models import Sms
from core.sms.telstra_api import TELSTRA_SMS_MONTHLY_COUNTER, telstra_sender
from ..express.models import ExpressOrder
from .models import DealSubscribe, forex

log = logging.getLogger(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)

ozbargin_last_date = 'schedule.ozbargin.last_date'
ozbargin_keywords = ['citibank', 'anz', 'cba', 'nab', 'westpac', 'fee for life',
                     'Trifecta', 'filco']


def get_rss(url):
    return urllib2.urlopen(urllib2.Request(url))


def utf8len(s):
    return len(s.encode('utf-8')) if isinstance(s, unicode) else len(s)


def utf8sub(s, length):
    length = int(length / 3) if isinstance(s, unicode) else length
    return s[:length]


@periodic_task(run_every=crontab(minute='*/15', hour='7-0'))
def ozbargin_task():
    url = 'https://www.ozbargain.com.au/deals/feed'

    subscribe_list = DealSubscribe.objects.filter(is_active=True)
    if not subscribe_list.count():
        return

    data = urllib2.urlopen(urllib2.Request(url))
    soup = BeautifulSoup(data, "lxml-xml")
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
        pub_date = item.pubDate.text

        try:
            item_date = parser.parse(pub_date)
        except:
            log.info('[Item Parsing] date parsing failed: %s' % pub_date)
            continue
        # print comment_count, title, item_date

        # convert aware and naive time
        if item_date.tzinfo and not last_date.tzinfo:
            last_date = last_date.replace(tzinfo=pytz.UTC)
            new_last_date = new_last_date.replace(tzinfo=pytz.UTC)
        elif not item_date.tzinfo and last_date.tzinfo:
            last_date = last_date.replace(tzinfo=None)
            new_last_date = new_last_date.replace(tzinfo=None)

        if item_date < last_date:
            continue
        elif item_date > new_last_date:
            new_last_date = item_date

        for subscribe in subscribe_list:
            includes = subscribe.get_keyword_list()
            excludes = subscribe.get_exclude_list()

            # check keywords
            if any([x.lower() in title.lower() for x in excludes if x]):
                continue

            flag = any([key.lower() in title.lower() for key in includes if key])
            if votes_pos > 30:
                title = '* %s' % title
                flag = True

            if flag:
                text_list = BeautifulSoup(description, "html.parser").findAll(text=True)
                description = ' '.join(x.strip() for x in text_list)
                summary = '[%s]%s\n%s\n' % (item_date.strftime('%H:%M'), title, link)
                content = summary + description
                content = content[:telstra_sender.LENGTH_PER_SMS]

                # avoid duplication
                day_ago = timezone.now() - relativedelta(days=1)
                if not Sms.objects.filter(time__gt=day_ago, send_to=subscribe.mobile, content=content).exists():
                    result, detail = telstra_sender.send_sms(subscribe.mobile, content, 'OZBARGIN_SUBSCRIBE')
                    subscribe.msg_count += 1
                    subscribe.save(update_fields=['msg_count'])
                    # print 'sending', content
                    log.info('[SMS] success=%s,%s. %s' % (result, detail, summary))

    r.set(ozbargin_last_date, new_last_date)


smzdm_last_date = 'schedule.smzdm.last_date'
smzdm_keywords = []


@periodic_task(run_every=crontab(minute='*/20', hour='7-0'))
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
        pub_date = item.pubDate.text

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
            new_last_date = new_last_date.replace(tzinfo=pytz.UTC)
        elif not item_date.tzinfo and last_date.tzinfo:
            last_date = last_date.replace(tzinfo=None)
            new_last_date = new_last_date.replace(tzinfo=None)

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
            result, detail = telstra_sender.send_to_self(content)
            # print 'sending', content
            log.info('[SMS] success=%s,%s. %s' % (result, detail, summary))

    r.set(smzdm_last_date, new_last_date)


@periodic_task(run_every=crontab(minute=0, hour='8,12,16,20', day_of_week='mon,tue,wed,thu,fri'))
def get_forex_quotes():
    api_key = settings.ONE_FORGE_API_KEY
    client = python_forex_quotes.ForexDataClient(api_key)
    currency_pairs = ['AUDCNH', 'USDCNH', 'NZDCNH', 'EURCNH', 'GBPCNH', 'CADCNH', 'JPYCNH']
    quotes = client.getQuotes(currency_pairs)
    msg = ''
    for quote in quotes:
        if not quote['ask']:
            continue
        value = Decimal(quote['ask'])
        setattr(forex, quote['symbol'], value)
        msg += '%s: %.4f\n' % (quote['symbol'], value)
        
    telstra_sender.send_to_self(msg.strip())


@periodic_task(run_every=crontab(hour=20, minute=30))
def express_id_upload_task():
    unupload_order = ExpressOrder.objects.filter(id_upload=False)
    if unupload_order.exists():
        ids = ','.join([o.track_id for o in unupload_order])
        telstra_sender.send_to_self('Upload ID for %s' % ids)

    log.info('[Express] Daily id upload checking.')


@periodic_task(run_every=crontab(hour=0, minute=1))
def reset_email_daily_counter():
    r.set(ALIYUN_EMAIL_DAILY_COUNTER, 0)
    log.info('[EMAIL] Reset aliyun email daily counter.')


@periodic_task(run_every=crontab(hour=0, minute=1, day_of_month=1))
def reset_sms_monthly_counter():
    r.set(TELSTRA_SMS_MONTHLY_COUNTER, 0)
    log.info('[SMS] Reset Telstra sms monthly counter.')
