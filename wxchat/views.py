from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import logging
from django.shortcuts import render
import time
import datetime
import json
import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from redis import Redis
from wechatpy import WeChatClient, WeChatPay, parse_message, WeChatOAuth
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.replies import TransferCustomerServiceReply, ImageReply, VoiceReply, create_reply
from wechatpy.session.redisstorage import RedisStorage
from wechatpy.utils import random_string, check_signature
from wxchat.decorators import weixin_decorator
from wxchat.models import WxUserInfo


logger = logging.getLogger("django")

redis_client = Redis.from_url(settings.REDIS_URL)
session_interface = RedisStorage(
    redis_client,
    prefix="wechatpy"
)

def wxClient():
    """
    创建微信客户端对象
    :return:
    """
    client = WeChatClient(settings.WECHAT_APPID, settings.WECHAT_SECRET, session=session_interface)
    return client


def WeixinPay():
    """
     创建微信支付对象
    :return:
    """
    wxPay = WeChatPay(appid=settings.WECHAT_APPID, api_key=settings.MCH_KEY, mch_id=settings.MCH_ID)
    return wxPay


def getJsApiSign(request):
    """
    微信JSAPI支付
    """
    client = wxClient()
    ticket = client.jsapi.get_jsapi_ticket()
    noncestr = random_string(15)
    timestamp = int(time.time())
    url = request.build_absolute_uri()
    signature = client.jsapi.get_jsapi_signature(noncestr, ticket, timestamp, url)
    sign_package = {
        "appId": settings.WECHAT_APPID,
        "nonceStr": noncestr,
        "timestamp": timestamp,
        "signature": signature
    }
    return sign_package


@csrf_exempt
def wechat(request):
    if request.method == 'GET':
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)

        try:
            check_signature(settings.WECHAT_TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            echostr = 'error'

        return HttpResponse(echostr)

    elif request.method == 'POST':
        msg = parse_message(request.body)
        print('+++++:', msg, msg.type)
        if msg.type == 'text':
            reply = TransferCustomerServiceReply(message=msg)
        elif msg.type == 'image':
            reply = ImageReply(message=msg)
            reply.media_id = msg.media_id
        elif msg.type == 'voice':
            reply = VoiceReply(message=msg)
            reply.media_id = msg.media_id
            reply.content = '语音信息'
        elif msg.type == 'event':
            print('eventkey=', msg.event)
            if msg.event == 'subscribe':
                saveUserinfo(msg.source)
                reply = create_reply('您好，欢迎关注祥子律师事务所', msg)
            elif msg.event == 'unsubscribe':
                reply = create_reply('取消关注公众号', msg)
                unSubUserinfo(msg.source)
            elif msg.event == 'subscribe_scan':
                reply = create_reply('您好，欢迎关注祥子律师事务所', msg)
                saveUserinfo(msg.source, msg.scene_id)
            elif msg.event == 'scan':
                reply = create_reply('', msg)
            else:
                reply = create_reply('view', msg)
        else:
            reply = create_reply('', msg)

        response = HttpResponse(reply.render(), content_type="application/xml")
        return response


def saveUserinfo(openid, scene_id=None):
    """
    保存或更新关注用户信息
    :param openid:
    :param scene_id:
    :return:
    """
    client = wxClient()
    user = client.user.get(openid)
    if 'errcode' not in user:
        user.pop('groupid')
        user.pop('qr_scene_str')
        user.pop('remark')
        user.pop('tagid_list')
        sub_time = user.pop('subscribe_time')
        sub_time = datetime.datetime.fromtimestamp(sub_time)
        user['subscribe_time'] = sub_time
        obj, created = WxUserInfo.objects.update_or_create(defaults=user, openid=openid)
        logger.info(obj)
        logger.info(created)
    else:
        logger.info(user)


def unSubUserinfo(openid):
    """
    取消订阅
    :param openid:
    :return:
    """
    try:
        user = WxUserInfo.objects.get(openid=openid)
        user.subscribe = 0
        user.save()
    except WxUserInfo.DoesNotExist as ex:
        logging.info(ex)


@login_required
def createMenu(request):
    client = wxClient()
    resp = client.menu.create({
        "button": [
            {
                "type": "view",
                "name": "律师服务",
                "url": settings.ROOT_URL + "/"
            },
            # {
            #     "type": "view",
            #     "name": "充电桩",
            #     "url": settings.ROOT_URL + "/order/"
            # },
            # {
            #     "type": "view",
            #     "name": "扫码充电",
            #     "url": settings.ROOT_URL + "/wechat/scanqrcode/"
            # },
            # {
            #     "type": "view",
            #     "name": "个人中心",
            #     "url": settings.ROOT_URL + "/wechat/personinfo/"
            # },

        ]
    })
    return HttpResponse(json.dumps(resp))


@login_required
def deleteMenu(request):
    client = wxClient()
    resp = client.menu.delete()
    return HttpResponse(json.dumps(resp))


@login_required
def getMenu(request):
    client = wxClient()
    resp = client.menu.get()
    return HttpResponse(json.dumps(resp, ensure_ascii=False))


def getWechatAuthCode(request):
    code = request.GET.get('code', None)
    if code is None:  # 获取授权码code
        url = request.GET.get('url', None)
        redirect_url = url if url is not None else settings.WEB_URL
        print(redirect_url)
        webchatOAuth = WeChatOAuth(settings.WECHAT_APPID, settings.WECHAT_SECRET, redirect_url, 'snsapi_userinfo')
        authorize_url = webchatOAuth.authorize_url
        res = {
            'status_code': 200,
            "authorize_url": authorize_url
        }
        print(res)
        return JsonResponse(res)


def getWechatAuth(request):
    code = request.GET.get('code', None)
    webchatOAuth = WeChatOAuth(settings.WECHAT_APPID, settings.WECHAT_SECRET, '', 'snsapi_userinfo')
    res = webchatOAuth.fetch_access_token(code)
    if 'errcode' in res:
        return HttpResponse(json.dumps(res))
    else:
        open_id = webchatOAuth.open_id
        userinfo = webchatOAuth.get_user_info()
        userinfo.pop('privilege')
        obj, created = WxUserInfo.objects.update_or_create(openid=open_id, defaults=userinfo)
        print('-------------', obj, created)
        data = {
            'status_code': 200,
            'openid': open_id,
            'member_role': obj.member_role_id if obj.member_role else 0
        }
        return JsonResponse(data)


# 获取用户openid列表
@login_required
def get_user_info(request):
    client = wxClient()
    userid_list = client.user.get_followers()
    logger.info(userid_list)
    WxUserInfo.objects.all().update(qr_scene=0)

    if 'errcode' not in userid_list and userid_list['count'] > 0:
        openid_list = userid_list['data']['openid']
        n = 100
        for openids in [openid_list[i:i + n] for i in range(0, len(openid_list), n)]:
            print("openids:", openids)
            userinfo_lists = client.user.get_batch(openids)
            for user in userinfo_lists:
                logger.info(user)
                sub_time = user.pop('subscribe_time')
                sub_time = datetime.datetime.fromtimestamp(sub_time).strftime('%Y-%m-%d %H:%M:%S')
                user['subscribe_time'] = sub_time
                WxUserInfo.objects.update_or_create(defaults=user, openid=user['openid'])

    return HttpResponse(json.dumps(userid_list, ensure_ascii=False))
