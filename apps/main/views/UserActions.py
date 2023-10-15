# --*--*--*--*--*--*- Create by bh at 2023/10/9 19:03 -*--*--*--*--*--*--
from main.daos import user_dao, gup_dao, pms_dao
from main.servers.DataAction import DataActionView
from django.views import View
from main.servers.Err import ClientErr
from main.utils.decorates.request_to_response import request_to_response, allow_anonymous_user_access


class UserDataAction(View):

    @request_to_response
    def post(self, request):
        server = DataActionView(request, user_dao, unique_fs=('username',))
        server.params['is_staff'] = False
        return server.create()

    @request_to_response
    def get(self, request):
        return DataActionView(request, user_dao).page(
            dt_range={'is_superuser': False, 'id': request.user.id}
        )

    @request_to_response
    def put(self, request):
        server = DataActionView(request, user_dao, unique_fs=('username',))
        if server.params.get('id') != request.user.id:
            raise ClientErr(msg='搭你跟前版本不支持修改其他用戶的信息')
        return server.update()

    @request_to_response
    def delete(self, request):
        server = DataActionView(request, user_dao)
        server.params['is_active'] = False
        if server.params.get('id') != request.user.id:
            raise ClientErr(msg='搭你跟前版本不支持修改其他用戶的信息')
        return server.update()


class GroupDataAction(View):

    @request_to_response
    def post(self, request):
        server = DataActionView(request, gup_dao, unique_fs=('name',))
        server.params['is_staff'] = False
        return server.create()

    @request_to_response
    def get(self, request):
        return DataActionView(request, gup_dao).page()

    @request_to_response
    def put(self, request):
        return DataActionView(request, gup_dao, unique_fs=('name',)).update()

    @request_to_response
    def delete(self, request):
        raise ClientErr(msg='该功能未开放')
