# --*--*--*--*--*--*- Create by bh at 2023/10/5 15:54 -*--*--*--*--*--*--
from main.daos import pro_dao, api_dao, prm_dao, req_log_dao
from main.servers.DataAction import DataActionView
from django.views import View
from main.servers.Err import ClientErr
from main.utils.decorates.request_to_response import request_to_response, allow_anonymous_user_access
from main.utils.common import choices_to_dict
from main.models.ApiModules import MethodType


class ProjectDataAction(View):

    @request_to_response
    def post(self, request):
        server = DataActionView(request, pro_dao, unique_fs=('code',))
        server.params['create_by'] = request.user.username
        return server.create()

    @request_to_response
    def get(self, request):
        return DataActionView(request, pro_dao).page()

    @request_to_response
    def put(self, request):
        return DataActionView(request, pro_dao, unique_fs=('code',)).update()

    @request_to_response
    def delete(self, request):
        return ClientErr(msg='未开放该功能')


class ApiDataAction(View):

    @request_to_response
    def post(self, request):
        server = DataActionView(request, api_dao)
        server.params['create_by'] = request.user.username
        method = server.params.pop('method', 0)
        if not isinstance(method, int):
            server.params['method'] = choices_to_dict(MethodType, key_is_filed=False).get(method, 15)
        return server.create()

    @request_to_response
    def get(self, request):
        return DataActionView(request, api_dao).page()

    @request_to_response
    def put(self, request):
        server = DataActionView(request, api_dao)
        server.params['update_by'] = request.user.username
        return server.update()

    @request_to_response
    def delete(self, request):
        return ClientErr(msg='未开放该功能')


class ParamDataAction(View):

    @request_to_response
    def post(self, request):
        server = DataActionView(request, prm_dao)
        server.params['create_by'] = request.user.username
        return server.create()

    @request_to_response
    def get(self, request):
        return DataActionView(request, prm_dao).page()

    @request_to_response
    def put(self, request):
        return DataActionView(request, prm_dao).update()

    @request_to_response
    def delete(self, request):
        return ClientErr(msg='未开放该功能')


class ApiLogDataAction(View):

    @request_to_response
    def get(self, request):
        return DataActionView(request, req_log_dao).page()

    @request_to_response
    def put(self, request):
        return ClientErr(msg='未开放该功能')

    @request_to_response
    def delete(self, request):
        return ClientErr(msg='未开放该功能')
