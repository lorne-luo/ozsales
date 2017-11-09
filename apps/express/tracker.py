# coding=utf-8
from bs4 import BeautifulSoup
import requests


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


def get_last_record(table, tag='tr', index=-1):
    trs = table.find_all(tag)
    return trs[index].get_text()


# =======================================================
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
