from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import logging
from django.shortcuts import render
import time
import datetime
import json

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from redis import Redis
from wechatpy import WeChatClient, WeChatPay, parse_message
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.replies import TransferCustomerServiceReply, ImageReply, VoiceReply, create_reply
from wechatpy.session.redisstorage import RedisStorage
from wechatpy.utils import random_string, check_signature
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
                reply = create_reply('你好，欢迎关注祥子律师事务所', msg)
            elif msg.event == 'unsubscribe':
                reply = create_reply('取消关注公众号', msg)
                unSubUserinfo(msg.source)
            elif msg.event == 'subscribe_scan':
                reply = create_reply('你好，欢迎关注祥子律师事务所', msg)
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
                "url": settings.ROOT_URL + "/lawyer/"
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

