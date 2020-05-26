from django.shortcuts import render

# Create your views here.
#
# class HostQrCodeView(View):
#     def get(self, request, *args, **kwargs):
#         orderid = request.GET.get("orderid", None)
#         flag = request.GET.get("flag", None)
#         try:
#             order = HostingOrder.objects.get(pk=orderid)
#             if len(order.code) == 0:
#                 code = '{0}{1}'.format(datetime.datetime.now().strftime('%Y%m%d'), random.randint(1000, 10000))
#                 order.code = code
#                 order.save(update_fields=['code'])
#             else:
#                 code = order.code
#
#             host = request.get_host()
#             path = reverse('hosting-qrcode-ack')
#             url = "http://{0}{1}?code={2}&flag={3}".format(host, path, code, flag)
#
#             image = create_qrcode( url )
#             f = BytesIO()
#             image.save(f, "PNG")
#         except HostingOrder.DoesNotExist as ex:
#             return HttpResponse(json.dumps({"success":"false"}))
#
#         return HttpResponse(f.getvalue())
