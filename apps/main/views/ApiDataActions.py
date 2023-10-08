# --*--*--*--*--*--*- Create by bh at 2023/10/5 15:54 -*--*--*--*--*--*--
from main.daos import pro_dao, api_dao, prm_dao, req_log_dao
from main.servers.DataAction import DataActionView
from django.views import View
from main.servers.Err import ClientErr
from main.utils.decorates.request_to_response import request_to_response, allow_anonymous_user_access


class ProjectDataAction(View):
    allow_anonymous_user_access.add('post')
    allow_anonymous_user_access.add('get')
    allow_anonymous_user_access.add('put')

    @request_to_response
    def post(self, request):
        server = DataActionView(request, pro_dao, unique_fs=('code',))
        return server.create()

    @request_to_response
    def get(self, request):
        return DataActionView(request, pro_dao).page()

    @request_to_response
    def put(self, request):
        return DataActionView(request, pro_dao).update()

    @request_to_response
    def delete(self, request):
        return ClientErr(msg='未开放该功能')


class ApiDataAction(View):
    allow_anonymous_user_access.add('post')
    allow_anonymous_user_access.add('get')
    allow_anonymous_user_access.add('put')

    @request_to_response
    def post(self, request):
        pass
        return dict()

    @request_to_response
    def get(self, request):
        return DataActionView(request, api_dao).page()

    @request_to_response
    def put(self, request):
        return DataActionView(request, api_dao).update()

    @request_to_response
    def delete(self, request):
        return ClientErr(msg='未开放该功能')


class ParamDataAction(View):
    allow_anonymous_user_access.add('post')
    allow_anonymous_user_access.add('get')
    allow_anonymous_user_access.add('put')

    @request_to_response
    def post(self, request):
        pass
        return dict()

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
    allow_anonymous_user_access.add('get')

    @request_to_response
    def get(self, request):
        return DataActionView(request, req_log_dao).page()

    @request_to_response
    def put(self, request):
        return ClientErr(msg='未开放该功能')

    @request_to_response
    def delete(self, request):
        return ClientErr(msg='未开放该功能')
