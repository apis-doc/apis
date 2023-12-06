# --*--*--*--*--*--*- Create by bh at 2023/10/9 19:50 -*--*--*--*--*--*--
from django.views import View
from main.utils.decorates.request_to_response import request_to_response, allow_anonymous_user_access, load_request_data
from main.servers.Err import ClientErr
from main.daos import user_dao
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import check_password
from main.models.ApiModules import MethodType, ApiType, ParamType, ApiState
from main.utils.common import display_choices


class AuthView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        allow_anonymous_user_access.add('post')

    @request_to_response
    def post(self, request):
        return self.login(request)

    @request_to_response
    def get(self, request):
        return self.get_info(request)

    @request_to_response
    def put(self, request):
        online, req_data = request.user, load_request_data(request)
        if not check_password(req_data.get('password'), online.password):
            raise ClientErr('密码验证失败,请重新尝试')
        online.set_password(req_data.get('new'))
        online.save()
        return dict()

    @request_to_response
    def delete(self, request):
        return self.logout(request)

    def login(self, request):
        req_data = load_request_data(request)
        username = req_data.get('username', '')
        password = req_data.get('password', '')
        if not (username and password):
            raise ClientErr(msg='用户名或密码为空,请检查后重试')
        users = user_dao.query({'username': username})
        if not users:
            raise ClientErr(msg='用户名错误,请确认无误后重试')
        user = users[0]
        if authenticate(request, username=username, password=password) is None:
            raise ClientErr(msg='密码错误,请确认无误后重试')
        if user.is_active is not True:
            raise ClientErr(msg='您的账户已被冻结,请联系管理员解锁')
        login(request, user)
        return dict()

    def logout(self, request):
        logout(request)
        return dict()

    def get_info(self, request):
        online = request.user or None
        user_info = {
            'username': online.username if online else '-',
            'id': online.id if online else 0,
            'name': online.get_full_name() if online else ''
        }
        return {
            'user': user_info,
            'api_type': display_choices(ApiType),
            'param_type': display_choices(ParamType),
            'api_state': display_choices(ApiState),
            'method_type': display_choices(MethodType),
        }
