# --*--*--*--*--*--*- Create by bh at 2023/10/5 18:35 -*--*--*--*--*--*--
import datetime
import json
import traceback

from django.conf import settings
from django.http import HttpRequest
from django.http import JsonResponse

from main.servers.Err import ClientErr, ServerErr
from main.utils.logs import error


def load_request_data(request: HttpRequest) -> dict:
    req_data = dict()
    if request.body:
        try:
            req_data = json.loads(request.body)
        except Exception as e:
            raise ClientErr(msg=e)
    req_data.update(**request.POST)
    get_transfer = {'True': True, 'False': False}
    for key, value in request.GET.items():
        req_data[key] = value
        if not isinstance(value, str):
            continue
        if value in get_transfer.keys():
            req_data[key] = get_transfer[value]
        if value.find(',') > 0:
            req_data[key] = value.split(',')
        try:
            req_data[key] = json.loads(value.replace("'", '"'))
        except Exception as e:
            print(f'load request json string: {key}|{value}| {e}')
    if settings.DEBUG:
        print(f'load_request_data: {req_data}')
    return req_data


allow_anonymous_user_access = set()


# 允许匿名用户访问
def clear_anonymous_access():
    allow_anonymous_user_access.clear()


def request_to_response(function):
    """
    对请求进行判定，筛选，以及返回。
    """

    def wrap(*args, **_):

        resp = {
            'code': '1000', 'data': {}, 'msg': '',
        }
        request = args[1]  # 获取request
        req_data, interface = load_request_data(request), request.path
        request.request_data = req_data
        try:
            # todo 参数校验
            if request.method.lower() not in allow_anonymous_user_access:
                # login
                pass
            args = list(args)
            args[1] = request
            resp.update(data=function(*args))
        except ClientErr as e:
            resp['code'] = e.code
            resp['msg'] = e.msg
        except ServerErr as e:
            resp['code'] = e.code
            resp['msg'] = e.msg
            error.warn(f'---> Gateway-ServerErr, e: {e}, req_data-{req_data}\nargs: {args}\n{e.detail}')
        except Exception as e:
            if settings.DEBUG:
                print(f'gateway err，req-{request.path}, data-{req_data}')
                traceback.print_exc()
            error.info(
                f'--->{request.META["req-id"]} Gateway-Err: {e}, req_data-{req_data}\n'
                f'args: {args}\n{traceback.format_exc()}'
            )
            resp['code'] = '9999'
            resp['msg'] = '服务内部异常，请稍后重新尝试! '
        finally:
            clear_anonymous_access()
            resp['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return JsonResponse(resp, json_dumps_params={'ensure_ascii': False})

    return wrap
