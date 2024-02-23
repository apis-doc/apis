# --*--*--*--*--*--*- Create by bh at 2023/10/7 17:52 -*--*--*--*--*--*--
from proxy.views import proxy_view
from main.utils.decorates.request_to_response import load_request_data
from main.utils.common import choice_value, json_str
from main.models import RequestLog, Api, Params
from main.models.ApiModules import MethodType
from main.views.other_views import get_json_data
from main.views.ApiDataActions import creates


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
        log.status_code = rsp.status_code
        log.save(update_fields=('rsp', 'status_code'))
        return rsp


def put_iteration_request(request):
    """
    接口迭代
        新复制一份接口数据, 并修改原接口状态为已迭代-3
         并按照新的请求和返回示例重新生成对应接口的参数
         匹配数据库中原参数与新参数, 复制其人为编辑字段的值
     """
    req_data = load_request_data(request)
    redirect_url = req_data.pop('redirect', '')
    api_id = req_data.pop('api-id', 0)
    if not (redirect_url and api_id):
        raise Exception('[apis]iteration: The parameter api-id or redirect is missing!')
    origins = (Api.objects.filter(origin__id=api_id, ).order_by('-update_time')
               or Api.objects.filter(id=api_id))
    if not origins:
        raise Exception('[api]The log cannot be found by api-lid.')
    try:
        rsp = proxy_view(request, redirect_url)
    except Exception as e:
        raise Exception(f'[apis]proxy api: {str(e)}')
    uris = redirect_url.replace('//', '').split('/')
    interface_id = req_data.get('method', '')
    # todo: login, user
    # 重新赋值接口并从原接口复制接口其他字段
    origin = origins[0]
    origin.state = 3
    origin.save(update_fields=['state'])
    new = Api.objects.create(**{
        'content_type': request.META.get('CONTENT_TYPE', ''),
        'api_type': 0 if interface_id else 1,
        'path': redirect_url.replace('//', '').replace(uris[0], ''),
        'req_example': req_data,
        'rsp_example': rsp.content.decode(),
        'state': 4, 'origin_id': api_id, 'update_by': '接口变更',
        'api_method': interface_id, 'owner_id': origin.owner_id,
        'method': choice_value(MethodType, match=request.method, default=0),
    })
    copy_fds = ['api_name', 'describe', 'version', 'Attentions', 'note', 'maintainer',
                'is_login', 'require_auth']
    for field in copy_fds:
        if not hasattr(new, field.split('__')[0]):
            continue
        setattr(new, field, getattr(origin, field))
    new.save(update_fields=copy_fds)
    # 重新生成参数
    if req_data:
        creates(get_json_data(req_data), new.id, 'request', '接口生成')
    if rsp.content:
        creates(get_json_data(json_str(rsp.content.decode())), new.id, 'response', '接口生成')
    # 复制参数的人为编辑字段值
    new_params = Params.objects.filter(owner_id=new.id, is_service=True).values('code', 'id', 'parent__code',
                                                                                'own_type')
    old_params = Params.objects.filter(
        name__isnull=False, code__in=[obj['code'] for obj in new_params]
    ).exclude(name__exact='').values('code', 'parent__code', 'name', 'own_type', 'is_require', 'is_null', 'id',
                                     'note').order_by('id')  # id 排序的话, 会取最新的结果
    for pid, upt_data in copy_fields_from_db(new_params, old_params).items():
        Params.objects.filter(id=pid).update(**upt_data)
    return rsp


def copy_fields_from_db(new, old):
    def dicts(objs):
        ret = {}
        for obj in objs:
            ret[f"{obj['code']}-{obj['own_type']}-{obj['parent__code']}"] = obj
        return ret

    params = {}
    new, old_match_all = dicts(new), dicts(old)
    old_match_name = {obj['code']: obj for obj in old}
    for key, param in new.items():
        field_name = key.split('-')[0]
        pid = param['id']
        if key in old_match_all.keys():
            values = old_match_all.get(key)
            params[pid] = {
                'name': values.get('name'),
                'is_require': values.get('is_require'),
                'is_null': values.get('is_null'),
                'note': values.get('note'),
            }
        elif field_name in old_match_name.keys():
            params[pid] = {'name': old_match_name[field_name].get('name', '')}
    return params
