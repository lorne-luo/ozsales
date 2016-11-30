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
        request.session['wx_app_name'] = app.name
        request.session['wx_app_id'] = app.app_id
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
    request.session['wx_openid'] = openid
    scope = response_json['scope']
    token = response_json['access_token']  # 网页授权access_token和公众号的access_token不一样
    # 关于网页授权access_token和普通access_token的区别
    # 1、微信网页授权是通过OAuth2.0机制实现的，在用户授权给公众号后，公众号可以获取到一个网页授权特有的接口调用凭证（网页授权access_token），通过网页授权access_token可以进行授权后接口调用，如获取用户基本信息；
    # 2、其他微信接口，需要通过基础支持中的“获取access_token”接口来获取到的普通access_token调用。

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
        # 关于UnionID机制
        # 1、请注意，网页授权获取用户基本信息也遵循UnionID机制。即如果开发者有在多个公众号，或在公众号、移动应用之间统一用户帐号的需求，需要前往微信开放平台（open.weixin.qq.com）绑定公众号后，才可利用UnionID机制来满足上述需求。
        # 2、UnionID机制的作用说明：如果开发者拥有多个移动应用、网站应用和公众帐号，可通过获取用户基本信息中的unionid来区分用户的唯一性，因为同一用户，对同一个微信开放平台下的不同应用（移动应用、网站应用和公众帐号），unionid是相同的。

        # todo login wx user

    state = request.GET.get('state', '')  # next url
    if state:
        url = urlunquote(state)
    else:
        url = reverse('weixin:index', args=[app_name])

    return HttpResponseRedirect(url)


def wx_index(request, app_name):
    return HttpResponse('test page for ' + app_name)
