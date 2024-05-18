# --*--*--*--*--*--*- Create by bh at 2023/10/5 15:54 -*--*--*--*--*--*--
from main.daos import pro_dao, api_dao, prm_dao, req_log_dao, ntc_dao, rla_dao
from main.servers.DataAction import DataActionView
from django.views import View
from main.servers.Err import ClientErr
from main.utils.decorates.request_to_response import request_to_response, allow_anonymous_user_access, load_request_data
from main.utils.common import choices_to_dict
from main.models.ApiModules import MethodType
from django.conf import settings
from datetime import datetime


class ProjectDataAction(View):

    @request_to_response
    def post(self, request):
        server = DataActionView(request, pro_dao, unique_fs=('code',))
        server.params['create_by'] = request.user.username
        return server.create()

    @request_to_response
    def get(self, request):
        ret_pjt, pids = dict(), set()
        rsp = DataActionView(request, pro_dao).page()
        if rsp['count'] <= 0:
            return rsp
        for project in rsp['show_info']:
            pids.add(project['id'])
        notice_ids = ntc_dao.query(
            {'userId': request.user.id, 'projectId__in': pids, 'is_valid': True}
        ).values_list('projectId', flat=True)
        for project in rsp['show_info']:
            is_noticed = False
            if project['id'] in notice_ids:
                is_noticed = True
            project['is_noticed'] = is_noticed
        return rsp

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
        server = DataActionView(request, api_dao)
        state = server.params.get('state', '')
        # 迭代记录查询, 大概率从迭代历史页面过来的请求
        if state and state == 'iterator':
            server.params['state'] = settings.ITERATOR_STATES
            return server.page()
        # 指定状态查询, 此时不会自动去除已迭代接口
        if state:
            return server.page()
        # 接口查询页面默认去掉已经迭代的接口, 除非用户指定查询状态
        if server.params.get('is_state_not_equal_3', True):
            return server.page(extra={'where': ['state != 3']})
        return server.page()

    @request_to_response
    def put(self, request):
        server = DataActionView(request, api_dao)
        server.params['update_by'] = request.user.username
        return server.update()

    @request_to_response
    def delete(self, request):
        return ClientErr(msg='未开放该功能')


def creates(objs_dicts, api_id, own_type, create_by):
    def create(params, parent_id=None):
        params.pop('id', '')
        params['create_by'] = create_by
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

    server = DataActionView(None, prm_dao, params='pass')
    for p in objs_dicts:
        create(p, None)


class ParamDataAction(View):

    @request_to_response
    def post(self, request):
        params = load_request_data(request)
        creates(params.get('param_list'), params.get('api_id'), params.get('own_type'), request.user.username)
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


class NoticeAction(View):

    @request_to_response
    def post(self, request):
        """关注/重新关注: 考虑到重复关注前的发布读取状态, 目前维护一条记录"""
        server = DataActionView(request, ntc_dao)
        notices = ntc_dao.query({'userId': request.user.id, 'projectId': server.params['projectId']})
        if notices.exists():
            notices.update(is_valid=True, update_time=datetime.now(), project_name=server.params['project_name'])
            return {'state': 'activated'}
        server.params = {
            'userId': request.user.id,
            'projectId': server.params['projectId'],
            'project_name': server.params['project_name'],
            'is_valid': True
        }
        server.create()
        return {'state': 'activated'}

    @request_to_response
    def get(self, request):
        return DataActionView(request, pro_dao).page()

    @request_to_response
    def put(self, request):
        """已读, 未读状态在发布接口维护"""
        server = DataActionView(request, ntc_dao)
        ntc_dao.query({
            'userId': request.user.id,
            'projectId': server.params['projectId'],
            'is_valid': True
        }).update(is_read=True, update_time=datetime.now())
        return dict()

    @request_to_response
    def delete(self, request):
        """取消关注"""
        server = DataActionView(request, ntc_dao)
        notices = ntc_dao.query({'userId': request.user.id, 'projectId': server.params['projectId']})
        # todo update_time
        notices.update(is_valid=False, update_time=datetime.now())
        return dict()


class ReleaseAction(View):

    @request_to_response
    def get(self, request):
        return DataActionView(request, rla_dao).page()

    @request_to_response
    def post(self, request):
        """发布: 创建发布历史, 并更新已读状态"""
        allow_public_states, public_state, down_state = (0, 4, 5), 2, 1
        server, user = DataActionView(request, rla_dao), request.user
        api_id = server.params['apiId']
        # 校验接口状态, 更新接口状态
        apis = api_dao.query({'id': api_id})
        if len(apis) < 1:
            raise ClientErr(f'未查询到该接口({api_id})的信息, 请稍后重试')
        api = apis[0]
        if api.state == public_state:
            raise ClientErr(f'该接口已发布')
        if api.state not in allow_public_states and api.state != down_state:
            raise ClientErr(f'该接口的状态({api.id}/{api.state})不能处于服务中, 请检查后重试')
        if api.state in allow_public_states:
            api.state = public_state
            api.save()
        # 创建发布记录
        name = f'{user.first_name}{user.last_name}'
        server.params['api_name'] = api.api_name
        server.params['api_describe'] = api.describe
        server.params['projectId'] = api.owner_id
        server.params['by'] = f'{name}({user.username})'
        server.create()
        # 重置已读状态
        ntc_dao.query({
            'projectId': server.params['projectId'], 'is_read': True,
        }).update(is_read=False)
        return dict()

    @request_to_response
    def put(self, request):
        return ClientErr(msg='未开放该功能')

    @request_to_response
    def delete(self, request):
        raise ClientErr(msg='未开放该功能')
