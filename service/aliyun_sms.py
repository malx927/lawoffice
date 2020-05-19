#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
client = AcsClient('', '', 'cn-hangzhou')

request = CommonRequest()
request.set_accept_format('json')
request.set_domain('dysmsapi.aliyuncs.com')
request.set_method('POST')
request.set_protocol_type('https')
request.set_version('2017-05-25')
request.set_action_name('SendSms')

request.add_query_param('RegionId', "cn-hangzhou")
request.add_query_param('PhoneNumbers', "")
request.add_query_param('SignName', "")
request.add_query_param('TemplateCode', "")
request.add_query_param('TemplateParam', "{code:'723456'}")

response = client.do_action_with_exception(request)
print(response)
# b'{"Message":"OK","RequestId":"8AA5EEA5-256F-49A0-8278-9DBCD1EBC074","BizId":"637000889871963323^0","Code":"OK"}'