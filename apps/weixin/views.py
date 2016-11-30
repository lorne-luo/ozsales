# coding=utf-8
import logging
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import urlquote, urlunquote
from django.views.generic import ListView, CreateView, UpdateView
from django.core.urlresolvers import reverse
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from core.views.views import CommonContextMixin, CommonViewSet
from wechat_sdk.lib.request import WechatRequest

from models import WxApp
import conf

# import serializers
# import forms
log = logging.getLogger(__name__)


def wx_login(request, app_name):
    try:
        app = WxApp.objects.get(name=app_name)
    except ObjectDoesNotExist:
        raise Http404

    next = request.GET.get('next', '')
    login_url = app.get_login_url(conf.SCOPE_USERINFO, next)
    log.info('%s_login_url: %s' % (app_name, login_url))
    return HttpResponseRedirect(login_url)


def wx_auth(request, app_name):
    try:
        app = WxApp.objects.get(name=app_name)
    except ObjectDoesNotExist:
        raise Http404

    code = request.GET.get("code")
    wechat_request = WechatRequest()
    response_json = wechat_request.get(
        url='https://api.weixin.qq.com/sns/oauth2/access_token',
        params={
            'grant_type': 'authorization_code',
            'appid': app.app_id,
            'secret': app.app_secret,
            'code': code
        },
        access_token=app.access_token
    )
    openid = response_json['openid']
    scope = response_json['scope']
    token = response_json['access_token']

    if (scope == conf.SCOPE_USERINFO):
        # continue to get userinfo
        userinfo_json = wechat_request.get(
            url='https://api.weixin.qq.com/sns/userinfo',
            params={
                'openid': openid,
                'lang': 'zh_CN'
            },
            access_token=token
        )

        print userinfo_json
        openid = userinfo_json['openid']
        nickname = userinfo_json['nickname']
        headimgurl = userinfo_json['headimgurl']
        sex = userinfo_json['sex']
        province = userinfo_json['province']
        city = userinfo_json['city']
        country = userinfo_json['country']
        unionid = userinfo_json.get('unionid', None)
        privilege_list = userinfo_json['privilege']
        language = userinfo_json['language']

        # todo login wx user

    state = request.GET.get('state', '')  # next url
    if state:
        url = urlunquote(state)
    else:
        url = reverse('weixin:index', args=[app_name])

    return HttpResponseRedirect(url)


def wx_index(request, app_name):
    return HttpResponse('test page for ' + app_name)
