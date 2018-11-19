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
            '代收' in text,
            '自提' in text,
            '投到' in text,
            '已取' in text]) and '未' not in text and '不' not in text:
        return True, text
    return False, text.strip()


def get_track_items(url, selector):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html5lib")
    items = soup.select(selector)
    return items


def post_table(url, headers, data, selector):
    s = requests.session()
    r = s.post(url, data=data, headers=headers)
    data = r.text
    soup = BeautifulSoup(data, "html5lib")
    items = soup.select('selector')
    return items


def get_last_record(table, tag='tr', index=-1):
    trs = table.find_all(tag)
    return trs[index].get_text()


# =======================================================
def track_info(url, selector='table', item_index=-1):
    items = get_track_items(url, selector)
    # last_record = get_last_record(items, item_tag, item_index)
    last_record = ''
    if (items and items[item_index]):
        last_record = items[item_index].get_text()
    return check_delivery(last_record)


def table_last_tr(url):
    table = get_track_items(url)
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


def ewe_track(url, latest_index=-1):
    r = requests.get(url)
    if 300 > r.status_code > 199:
        try:
            data = r.json()
            last_item = data['Payload'][0]['Details'][latest_index]
            msgs = []
            for col in last_item.values():
                if isinstance(col, str):
                    msgs.append(col)
            return check_delivery(', '.join(msgs))
        except Exception as ex:
            return False, str(ex)
    else:
        return False, r.text


def aus_express_track(url, track_id, latest_index=-1):
    try:
        s = requests.session()
        r = s.get(url, stream=True)
        data = r.text
        soup = BeautifulSoup(data, "html5lib")
        viewstate = soup.find('input', id='__VIEWSTATE').attrs['value']
        eventvalidation = soup.find('input', id='__EVENTVALIDATION').attrs['value']
        code = soup.find('table', class_='code').find('font').get_text().strip()
        data = {'__VIEWSTATE': viewstate,
                '__EVENTVALIDATION': eventvalidation,
                'txtYzm': code,
                'txtNo': track_id,
                'btnSearch': '查询'}

        r = s.post(url, data=data, headers={'content-type': 'application/x-www-form-urlencoded',
                                            'referer': 'http://www.aus-express.com/Search.aspx'})
        soup = BeautifulSoup(r.text, "html5lib")
        trs = soup.select('div#main_left_depot ul table tr')
        if (trs and trs[latest_index]):
            return check_delivery(trs[latest_index].text)
    except Exception as ex:
        return False, str(ex)
