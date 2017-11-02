# coding=utf-8
from bs4 import BeautifulSoup
import requests


def parse_last_track(text):
    if any([u'签收' in text,
            u'投妥' in text,
            u'投到' in text]) and all([
                u'未签收' not in text,
                u'未投妥' not in text,
                u'未投到' not in text]):
        return True, text
    return False, text


def table_last_tr(url, id_=None, cls=None):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    if id_ is None and cls is None:
        table = soup.find('table')
    elif id_:
        table = soup.find('table', id=id_)
    elif cls:
        table = soup.find('table', class_=cls)

    trs = table.find_all('tr')
    last_track = trs[-1].get_text()
    return parse_last_track(last_track)


def sfx_track(url):
    return table_last_tr(url, id_='oTHtable')


def changjiang_track(url):
    return table_last_tr(url, cls='table')
