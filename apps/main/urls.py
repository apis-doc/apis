# --*--*--*--*--*--*- Create by bh at 2023/10/5 15:44 -*--*--*--*--*--*--
from django.conf.urls import url
from main.views.ReqLogAdd import put_request_log
from main.views.ApiDataActions import ProjectDataAction, ApiDataAction, ApiLogDataAction

urlpatterns = [
    url(r'^api/put/$', put_request_log, name='添加接口写入信息'),
    url(r'^project$', ProjectDataAction.as_view(), name='项目管理'),
    url(r'^api$', ApiDataAction.as_view(), name='接口管理'),
    url(r'^param$', ApiDataAction.as_view(), name='参数管理'),
    url(r'^req_log$', ApiLogDataAction.as_view(), name='请求记录管理'),
]

urlpatterns += [
    # url('test/', put_request_log),
]
