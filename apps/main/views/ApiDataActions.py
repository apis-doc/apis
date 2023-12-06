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
        rsp = server.create()
        return rsp

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

        def create(params, parent_id=None):
            params.pop('id', '')
            params['create_by'] = request.user.username
            params['owner_id'] = api_id
            params['parent_id'] = parent_id
            params['own_type'] = own_type
            children = params.pop('children', [])
            server.params = params
            res = server.create()
            if not children:
                return res['pk']
            for child in children:
                create(child, res['pk'])
            return res['pk']

        server = DataActionView(request, prm_dao)
        param_list = server.params.get('param_list')
        api_id = server.params.get('api_id')
        own_type = server.params.get('own_type')
        for p in param_list:
            create(p, None)
        return {}

    @request_to_response
    def get(self, request):

        def two(tag, parent):
            cl = []
            for i in tag:
                if i['parent_id'] == parent['id']:
                    cl.append(i)
                    i['children'] = two(tag, i)
            return cl

        ps = DataActionView(request, prm_dao).page()
        res, table_data = [], ps['show_info']
        for ele in ps['show_info']:
            if ele['parent_id'] is None:
                ele['children'] = two(table_data, ele)
                res.append(ele)
        ps['show_info'] = res
        return ps

    @request_to_response
    def put(self, request):
        return DataActionView(request, prm_dao).update()

    @request_to_response
    def delete(self, request):
        return ClientErr(msg='未开放该功能')


class ApiLogDataAction(View):

    @request_to_response
    def get(self, request):
        return DataActionView(request, req_log_dao).page(order_by=('-id',))

    @request_to_response
    def put(self, request):
        return ClientErr(msg='未开放该功能')

    @request_to_response
    def delete(self, request):
        return ClientErr(msg='未开放该功能')
