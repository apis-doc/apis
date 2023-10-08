# --*--*--*--*--*--*- Create by bh at 2023/10/7 17:52 -*--*--*--*--*--*--
from proxy.views import proxy_view
from main.utils.decorates.request_to_response import load_request_data
from main.models import RequestLog


def put_request_log(request):
    req_data = load_request_data(request)
    redirect_url = req_data.pop('redirect', '')
    if not redirect_url:
        raise Exception('[apis]put api: not redirect url!')
    uris = redirect_url.replace('//', '').split('/')
    api_uri, suffix = '/'.join(uris[1:]), '/' if '/'.endswith(redirect_url) else ''
    path = '/' + api_uri + suffix
    interface_id = req_data.get('method', '')
    log_data = {
        'method': request.method,
        'content_type': request.META.get('CONTENT_TYPE', ''),
        'api_type': 0 if interface_id else 1,
        'interface_id': interface_id,
        'path': path,
        'req': req_data,
    }
    # todo: login, user
    log = RequestLog.objects.create(**log_data)
    try:
        rsp = proxy_view(request, redirect_url)
    except Exception as e:
        log.err = str(e)
        log.save(update_fields=('rsp',))
        raise Exception('[apis]put api: proxy request!')
    else:
        log.rsp = rsp.content.decode()
        print(type(rsp))
        log.status_code = rsp.status_code
        log.save(update_fields=('rsp', 'status_code'))
        return rsp
