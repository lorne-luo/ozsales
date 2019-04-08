# -*- coding: utf-8 -*-
import json
import os
import datetime
import logging
import random
import shlex
import urllib.request, urllib.error, urllib.parse
import pytz
import redis
import subprocess

import requests
from django.utils import timezone
from django.conf import settings
from decimal import Decimal
from bs4 import BeautifulSoup
from celery.task import periodic_task, task

from dateutil import parser
from dateutil.relativedelta import relativedelta
from core.utils import telegram as tg

from core.aliyun.email.smtp import ALIYUN_EMAIL_DAILY_COUNTER
from core.sms.models import Sms
from core.utils.forext_1forge import ForexDataClient
from core.sms.telstra_api_v2 import send_au_sms, send_to_admin, TELSTRA_LENGTH_PER_SMS, TELSTRA_SMS_MONTHLY_COUNTER
from .models import DealSubscribe, forex

log = logging.getLogger(__name__)
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.CUSTOM_DB_CHANNEL,
                      decode_responses=True)

ozbargin_last_date = 'schedule.ozbargin.last_date'
ozbargin_keywords = ['citibank', 'anz', 'cba', 'nab', 'westpac', 'fee for life',
                     'Trifecta', 'filco']


def get_rss(url):
    return urllib.request.urlopen(urllib.request.Request(url))


def utf8len(s):
    return len(s.encode('utf-8')) if isinstance(s, str) else len(s)


def utf8sub(s, length):
    length = int(length / 3) if isinstance(s, str) else length
    return s[:length]


# @periodic_task(run_every=crontab(minute='*/15', hour='7-0'))
@task
def ozbargin_task():
    url = 'https://www.ozbargain.com.au/deals/feed'

    subscribe_list = DealSubscribe.objects.filter(is_active=True)
    if not subscribe_list.count():
        return

    data = urllib.request.urlopen(urllib.request.Request(url))
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
                content = content[:TELSTRA_LENGTH_PER_SMS]

                # avoid duplication
                day_ago = timezone.now() - relativedelta(days=1)
                if subscribe.mobile and not Sms.objects.filter(time__gt=day_ago, send_to=subscribe.mobile,
                                                               content=content).exists():
                    result, detail = send_au_sms(subscribe.mobile, content, 'OZBARGIN_SUBSCRIBE')
                    subscribe.msg_count += 1
                    subscribe.save(update_fields=['msg_count'])
                    # print 'sending', content
                    log.info('[SMS] success=%s,%s. %s' % (result, detail, summary))

    r.set(ozbargin_last_date, new_last_date)


smzdm_last_date = 'schedule.smzdm.last_date'
smzdm_keywords = []


# @periodic_task(run_every=crontab(minute='*/20', hour='7-0'))
@task
def smzdm_task():
    url = 'http://feed.smzdm.com/'
    haitao_url = 'http://haitao.smzdm.com/feed'

    if not smzdm_keywords:
        return

    req = urllib.request.Request(haitao_url, headers={'User-Agent': "Magic Browser"})
    data = urllib.request.urlopen(req)
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
            result, detail = send_to_admin(content)
            tg.send_me(content)
            # print 'sending', content
            log.info('[SMS] success=%s,%s. %s' % (result, detail, summary))

    r.set(smzdm_last_date, new_last_date)


# @periodic_task(run_every=crontab(minute=3, hour='8,12,16,20', day_of_week='mon,tue,wed,thu,fri'))
@task
def get_forex_quotes():
    api_key = settings.ONE_FORGE_API_KEY
    client = ForexDataClient(api_key)
    currency_pairs = ['AUDCNH', 'USDCNH', 'NZDCNH', 'EURCNH', 'GBPCNH', 'CADCNH', 'JPYCNH']
    quotes = client.getQuotes(currency_pairs)
    msg = ''
    for quote in quotes:
        if not quote['ask']:
            continue
        value = Decimal(str(quote['ask']))
        setattr(forex, quote['symbol'], value)
        msg += '%s: %.4f\n' % (quote['symbol'], value)

    send_to_admin(msg.strip())
    tg.send_me(msg.strip())


# @periodic_task(run_every=crontab(hour=0, minute=5))
@task
def reset_email_daily_counter():
    r.set(ALIYUN_EMAIL_DAILY_COUNTER, 0)
    log.info('[EMAIL] Reset aliyun email daily counter.')


# @periodic_task(run_every=crontab(hour=1, minute=13, day_of_month=1))
@task
def reset_sms_monthly_counter():
    r.set(TELSTRA_SMS_MONTHLY_COUNTER, 0)
    log.info('[SMS] Reset Telstra sms monthly counter.')


def run_shell_command(command_line):
    """ accept shell command and run"""
    command_line_args = shlex.split(command_line)
    log.info('Subprocess: "' + ' '.join(command_line_args) + '"')

    work_dir = os.path.abspath(os.path.join(settings.MEDIA_ROOT, '..'))

    try:
        command_line_process = subprocess.Popen(
            command_line_args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=work_dir
        )

        command_line_process.communicate()
        command_line_process.wait()
    except (OSError, subprocess.CalledProcessError) as exception:
        log.info('Exception occured: ' + str(exception))
        log.info('Subprocess failed')
        return False
    else:
        # no exception was raised
        log.info('Subprocess finished')
    return True


@task
def guetzli_compress_image(image_path):
    # create guetzli link under /usr/local/bin
    GUETZLI_CMD = '/usr/local/bin/guetzli'
    log.info('guetzli_compress_image: image_path=%s' % image_path)

    if os.path.exists(GUETZLI_CMD):
        cmd = '%s --quality 84 %s %s' % (GUETZLI_CMD, image_path, image_path)
        run_shell_command(cmd)


@task
def send_daily_weather():
    url = 'http://api.openweathermap.org/data/2.5/weather?q=Melbourne,au&units=metric&APPID=b796eacf7c532ede8dc2e34f67757945'
    data = requests.get(url)
    try:
        d = json.loads(data.text)
        _max = d.get('main').get('temp_max')
        _min = d.get('main').get('temp_min')
        weather = '->'.join([x.get('main') for x in d.get('weather')])
        date = datetime.datetime.now().strftime('%m-%d %a')
        elec = 5 + 20 * random.random()
        solar = 5 + 20 * random.random()
        tg.send_me('[WEATHER] %s\n%s\n Temp: %s - %s' % (date, weather, _min, _max))
        tg.send_me('[POWER]\nYesterday consume %.2f kWh\nSolar generate %.2f kWh' % (elec, solar))
    except:
        pass
