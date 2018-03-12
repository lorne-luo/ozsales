# coding=utf-8
import os
import shutil

from PIL import Image
from bs4 import BeautifulSoup
import requests
from django.conf import settings

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
    # print(data)
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
    s = requests.session()
    code_url = 'http://www.one-express.cn/index.php/app/Index/verify'
    file_path = os.path.join(settings.TEMP_ROOT, 'OneExpress.png')
    response = s.get(code_url, stream=True)
    with open(file_path, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    img = Image.open(file_path)

    parser = OneExpressParser()
    verify_code = parser.verify(img)
    if not verify_code:
        err_file_path = os.path.join(settings.TEMP_ROOT, 'OneExpress.err.png')
        os.rename(file_path, err_file_path)
    else:
        files = os.listdir(settings.TEMP_ROOT)
        for f in files:
            if f.startswith('OneExpress.done'):
                os.remove(os.path.join(settings.TEMP_ROOT, f))
        done_file_path = os.path.join(settings.TEMP_ROOT, 'OneExpress.done.%s.png' % verify_code)
        os.rename(file_path, done_file_path)

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'number': track_id,
        'verify': verify_code,
        'act': 'do'
    }
    # print(data)
    # table = post_table(url, headers, data)

    r = s.post(url, data=data, headers=headers)
    html = r.text
    # print(html)
    soup = BeautifulSoup(html, "html5lib")
    table = soup.find('table')

    last_record = get_last_record(table)
    return check_delivery(last_record)


def arkexpress_track(url):
    table = get_table(url, cls='trackContentTable')
    last_record = get_last_record(table)
    return check_delivery(last_record)
