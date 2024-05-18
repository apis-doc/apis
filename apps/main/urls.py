# --*--*--*--*--*--*- Create by bh at 2023/10/5 15:44 -*--*--*--*--*--*--
from django.conf.urls import url
from main.views.ReqLogAdd import put_request_log, put_iteration_request
from main.views.ApiDataActions import (
    ProjectDataAction, ApiDataAction, ApiLogDataAction, ParamDataAction, NoticeAction, ReleaseAction
)
from main.views.UserActions import UserDataAction, GroupDataAction, UserConfigAction
from main.views.other_views import JsonParseParam, HomeStaticAction
from main.views.AuthViews import AuthView

urlpatterns = [
    url(r'^api/put/$', put_request_log, name='添加接口写入信息'),
    url(r'^api/itera/$', put_iteration_request, name='修改接口写入信息'),

    url(r'^project$', ProjectDataAction.as_view(), name='项目管理'),
    url(r'^notice$', NoticeAction.as_view(), name='收藏管理'),
    url(r'^api$', ApiDataAction.as_view(), name='接口管理'),
    url(r'^release$', ReleaseAction.as_view(), name='发布管理'),

    url(r'^param$', ParamDataAction.as_view(), name='参数管理'),
    url(r'^req_log$', ApiLogDataAction.as_view(), name='请求记录管理'),

    url(r'^user$', UserDataAction.as_view(), name='用户管理'),
    url(r'^uconfig$', UserConfigAction.as_view(), name='用户配置管理'),

    url(r'^group$', GroupDataAction.as_view(), name='请求记录管理'),

    url(r'^auth$', AuthView.as_view(), name='授權管理'),
    url(r'^parse$', JsonParseParam.as_view(), name='json'),
    url(r'^home_static$', HomeStaticAction.as_view(), name='首页内容统计'),
    # todo 首页内容展示, 接口文档菜单生成

]

urlpatterns += [
    # url('test/', put_request_log),
]
