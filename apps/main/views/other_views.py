# --*--*--*--*--*--*- Create by bh at 2023/10/9 19:51 -*--*--*--*--*--*--
import json
from django.views import View
from main.utils.decorates.request_to_response import request_to_response, allow_anonymous_user_access
from main.servers.DataAction import DataActionView
from main.daos import req_log_dao
from main.servers.Err import ClientErr
from django.conf import settings
from main.utils.common import json_str


def get_json_data(data: dict) -> list:
    ret = []
    if not isinstance(data, dict):
        return ret
    for field, value in data.items():
        is_array = value and isinstance(value, (list, tuple, set))
        param = {
            'code': field,
            'param_type': 'array' if is_array else type(value).__name__,
            'example': value[:1] if is_array else value,
            'children': [],
            'is_require': True, 'is_null': True, 'is_service': True,

        }
        value = value[0] if is_array else value
        if isinstance(value, dict):
            param['children'] = get_json_data(value)
            param['example'] = '-'
        ret.append(param)
    return ret


class JsonParseParam(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        allow_anonymous_user_access.add('get')

    @request_to_response
    def get(self, request):
        server = DataActionView(request, dao=req_log_dao)
        log_id = server.params.get('id', None)
        if not log_id:
            raise ClientErr(msg='参数违法,请刷新后重试')
        logs = server.dao.query({'id': log_id})
        if not logs:
            raise ClientErr(msg='数据不存在,请刷新后重试')
        req_log = logs[0]
        # if req_log.content_type != 'application/json':
        #     raise ClientErr(msg='非json请求,不能获取数据')
        if settings.DEBUG is True:
            print('req: ', req_log.req)
            print('rsp: ', req_log.rsp)
        return {
            'req': get_json_data(json_str(req_log.req)) if req_log.req else [],
            'rsp': get_json_data(json_str(req_log.rsp)) if req_log.rsp else [],
        }