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
    if any(['签收' in text,
            '投妥' in text,
            '妥投' in text,
            '投到' in text,
            '收件人已取走' in text]) and all([
            '未签收' not in text,
            '未投妥' not in text,
            '未妥投' not in text,
            '未投到' not in text]):
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
def track_info(url, list_tag='table', id_=None, cls=None, item_tag='tr', item_index=-1):
    table = get_table(url, list_tag, id_, cls)
    last_record = get_last_record(table, item_tag, item_index)
    return check_delivery(last_record)


def table_last_tr(url):
    table = get_table(url)
    last_record = get_last_record(table)
    return check_delivery(last_record)


def sfx_track(url):
    table = get_table(url, id_='oTHtable')
    last_record = get_last_record(table)
    return check_delivery(last_record)


def bluesky_track(url):
    table = get_table(url, id_='oTHtable')
    last_record = get_last_record(table)
    return check_delivery(last_record)


def changjiang_track(url):
    table = get_table(url, cls='table')
    last_record = get_last_record(table)
    return check_delivery(last_record)


def transrush_au_track(url):
    resp = requests.get(url=url)
    data = resp.json()
    last = data['data'][0]['tracks'][0]
    last_text = '%s %s' % (last['TrackDate'], last['TrackContent'])
    return check_delivery(last_text)


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


def ewe_track(url):
    r = requests.get(url)
    if 300 > r.status_code > 199:
        try:
            data = r.json()
            last_item = data['Payload'][0]['Details'][-1]
            msgs = []
            for col in last_item.values():
                if isinstance(col, str):
                    msgs.append(col)
            return True, ', '.join(msgs)
        except Exception as ex:
            return False, str(ex)
    else:
        return False, r.text
