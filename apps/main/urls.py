# --*--*--*--*--*--*- Create by bh at 2023/10/5 15:44 -*--*--*--*--*--*--
from django.conf.urls import url

from main.views.ApiDataActions import ProjectDataAction

urlpatterns = [
    # url(r'^main/gateway/$', include('main.urls'), name='统一接口管理'),
    url('project/add|page|get|update/', ProjectDataAction.as_view(), name='项目管理'),
]
