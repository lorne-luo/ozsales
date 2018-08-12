# -*- coding: utf-8 -*-
import sys
import uuid
import json
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from django.conf import settings

from core.sms.models import Sms

"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""

reload(sys)
sys.setdefaultencoding('utf8')

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"
SIGN_NAME = '海马爸爸澳洲代购'

# ACCESS_KEY_ID/ACCESS_KEY_SECRET 根据实际申请的账号信息进行替换
ACCESS_KEY_ID = settings.ALIYUN_ACCESS_KEY_ID
ACCESS_KEY_SECRET = settings.ALIYUN_ACCESS_KEY_SECRET

acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


def send_sms(business_id, phone_numbers, template_code, template_param=None):
    if not phone_numbers:
        return False, 'INVALID_PHONE_NUMBER'

    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(SIGN_NAME)

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    data = json.loads(smsResponse)
    # {u'Message': u'OK', u'Code': u'OK', u'RequestId': u'22DB9012-D22D-412A-A27A-816CF80F09AA', u'BizId': u'178515533880148197^0'}
    success = data.get('Code', None) == 'OK'
    msg = data.get('Message', '')
    request_id = data.get('RequestId', '')

    # save sms history
    sms = Sms(app_name=business_id, send_to=phone_numbers, content=str(template_param), url=template_code,
              remark=msg, request_id=request_id, success=success)
    sms.save()
    return success, data['Message']


def query_send_detail(biz_id, phone_number, page_size, current_page, send_date):
    queryRequest = QuerySendDetailsRequest.QuerySendDetailsRequest()
    # 查询的手机号码
    queryRequest.set_PhoneNumber(phone_number)
    # 可选 - 流水号
    queryRequest.set_BizId(biz_id)
    # 必填 - 发送日期 支持30天内记录查询，格式yyyyMMdd
    queryRequest.set_SendDate(send_date)
    # 必填-当前页码从1开始计数
    queryRequest.set_CurrentPage(current_page)
    # 必填-页大小
    queryRequest.set_PageSize(page_size)

    # 调用短信记录查询接口，返回json
    queryResponse = acs_client.do_action_with_exception(queryRequest)

    data = json.loads(queryResponse)
    success = data.get('Code', None) == 'OK'
    return success, data['Message']
