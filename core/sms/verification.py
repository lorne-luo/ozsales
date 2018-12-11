import logging
import redis
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.utils import timezone
from django.utils.crypto import get_random_string

from core.sms.models import Sms
from core.aliyun.sms.service import validate_cn_mobile, send_cn_sms
from core.sms.telstra_api_v2 import validate_au_mobile, send_au_sms

log = logging.getLogger(__name__)

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.VERIFICATION_CODE_DB_CHANNEL,
                      decode_responses=True)

EXPIRES_IN = 600  # seconds
REGISTERATION_PURPOSE = 'REGISTERATION_PURPOSE'


def set_register_code(mobile, code):
    r.setex(mobile, EXPIRES_IN, code)


def send_verification_code(mobile):
    number = validate_cn_mobile(mobile)
    if number:
        country = 'CN'
    else:
        number = validate_au_mobile(mobile)
        if number:
            country = 'AU'
        else:
            return False, 'NUMBER_NOT_VALID'

    bz_id = 'Registeration#%s = %s' % (country, number)
    minute_ago = timezone.now() - relativedelta(seconds=60)
    if Sms.objects.filter(app_name=bz_id, send_to=number, success=True, time__gte=minute_ago).exists():
        return False, 'TOO_FREQUENTLY'

    code = get_random_string(4, '1234567890')
    r.setex(number, EXPIRES_IN, code)

    if country == 'CN':
        data = '''{"code":"%s"}''' % code
        return send_cn_sms(bz_id, mobile, settings.VERIFICATION_CODE_TEMPLATE, data)
    elif country == 'AU':
        content = '[%s] 验证码为 %s, 10分钟内有效.' % (settings.SITE_NAME, code)
        return send_au_sms(number, content, app_name=bz_id)


def verify_code(mobile, code):
    code = str(code)
    number = validate_cn_mobile(mobile) or validate_au_mobile(mobile)
    if number:
        return r.get(number) == code
    return False
