# coding=utf-8
import redis
from bs4 import BeautifulSoup
import requests
from .verify.one_express.parser import OneExpressParser


def check_delivery(text):
    text = ' '.join(text.replace('\n', ' ').replace('\r', '').split())
    if any([u'签收' in text,
            u'投妥' in text,
            u'妥投' in text,
            u'投到' in text]) and all([
                u'未签收' not in text,
                u'未投妥' not in text,
                u'未妥投' not in text,
                u'未投到' not in text]):
        return True, text
    return False, text.strip()


def get_table(url, tag='table', id_=None, cls=None):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html5lib")
    if id_ is None and cls is None:
        return soup.find(tag)
    elif id_:
        return soup.find(tag, id=id_)
    elif cls:
        return soup.find(tag, class_=cls)
    else:
        return None


def post_table(url, headers, data, tag='table', id_=None, cls=None):
    s = requests.session()
    r = s.post(url, data=data, headers=headers)
    data = r.text
    soup = BeautifulSoup(data, "html5lib")
    if id_ is None and cls is None:
        return soup.find(tag)
    elif id_:
        return soup.find(tag, id=id_)
    elif cls:
        return soup.find(tag, class_=cls)
    else:
        return None


def get_last_record(table, tag='tr', index=-1):
    trs = table.find_all(tag)
    return trs[index].get_text()


# =======================================================
def table_last_tr(url):
    table = get_table(url)
    last_record = get_last_record(table)
    return check_delivery(last_record)


def sfx_track(url):
    table = get_table(url, id_='oTHtable')
    last_record = get_last_record(table)
    return check_delivery(last_record)


def changjiang_track(url):
    table = get_table(url, cls='table')
    last_record = get_last_record(table)
    return check_delivery(last_record)


def transrush_au_track(url):
    table = get_table(url)
    last_record = get_last_record(table, index=1)
    return check_delivery(last_record)


def one_express_track(url, track_id):
    key = 'one_express_code'
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    verify_code = r.get(key)
    if verify_code is None:
        parser = OneExpressParser()
        verify_code = parser.run()
        r.setex(key, 55 * 60, verify_code)

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'number': track_id,
        'verify': verify_code,
        'act': 'do'
    }
    table = post_table(url, headers, data)
    last_record = get_last_record(table)
    return check_delivery(last_record)
