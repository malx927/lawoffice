

def get_openid_from_header(request):
    openid = request.META.get('HTTP_OPENID', '')
    return openid
