import datetime
import traceback
import uuid
import json
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from main.utils.logs import req_log, exception, long
from apis.conf.log_settings import (
    log_req_keys, is_log_long_time_request, long_time, ignore_log_request, encrypt_req_request,
    encrypt_rsp_request, long_req_length
)
from main.utils.common import contains


class ErrorLogMiddleware(MiddlewareMixin):
    """异常处理-500"""

    def process_exception(self, request, _):
        """
        :param request:
        :param _: exception
        :return:
        """
        # You can look for other values based on the req-id(uuid) in the META
        exception.put('except', request_default_info(request))


def get_user_req_info(request):
    def get(obj, k):
        null = f"{k}=None"
        if isinstance(obj, dict):
            return obj.get(k, null)
        return null if not hasattr(obj, k) else getattr(obj, k)

    default = []
    for key in log_req_keys.keys():
        _obj = request
        for attr in key.split('.'):
            _obj = get(_obj, attr)
        default += [get(_obj, key) for key in log_req_keys.get(key, list)]
    return default


class RequestLogMiddleware(MiddlewareMixin):

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.start_time = None  # 程序开始运行时间
        self.end_time = None  # 程序结束运行时间

    def process_request(self, request):
        self.start_time = datetime.datetime.now()  # Program start time
        request.META['req-id'] = str(uuid.uuid4())
        return None

    def process_response(self, request, response):
        try:
            if contains(request.path, ignore_log_request):
                return response

            # 程序结束运行时间
            self.end_time = datetime.datetime.now()
            run_time = (self.end_time - self.start_time).total_seconds()

            request_info = request_default_info(request)
            user_req_info = get_user_req_info(request)

            # response_data
            rsp_data = response.content.decode()
            rsp_data = json.loads(rsp_data) if isinstance(response, JsonResponse) else rsp_data
            if len(str(rsp_data)) > long_req_length:
                rsp_data = 'long_req_length'
            elif contains(request.path, encrypt_rsp_request):
                rsp_data = req_log.encrypt(rsp_data)

            # 记录请求日志
            handle_info = [str(response.status_code), str(rsp_data), str(run_time)]
            if response.status_code == 200 and isinstance(rsp_data, dict) and int(rsp_data.get('code', '0')) < 5000:
                log_level = 'info'
            elif response.status_code >= 500:
                log_level = 'error'
            else:
                log_level = 'warn'
            req_log.put(log_level, f"{' | '.join(request_info + handle_info + user_req_info)}")

            # 超长请求记录日志
            if is_log_long_time_request and int(run_time) >= long_time:
                long.info('---'.join(request_info))
        except Exception as e:
            if settings.DEBUG:
                print(f"process_response: {e}")
            exception.info(request.META['req-id'] + traceback.format_exc())

        return response


def request_default_info(request):
    schema = request.scheme
    server = request.META.get('HTTP_HOST', 'HTTP_HOST')
    path = request.path
    method = request.method
    req_id = request.META.get('req-id')

    access_ip = request.META.get('REMOTE_ADDR')

    user = 'AnonymousUser'
    if hasattr(request, 'user') and request.user.is_authenticated:
        user = str(request.user.username)

    # todo request data
    request_data = 'request_data'
    if contains(request.path, encrypt_req_request):
        request_data = req_log.encrypt(request_data)

    return [req_id, f"{schema}://{server}{path}", method, access_ip, user, request_data]
