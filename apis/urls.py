"""apis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls import static, url

urlpatterns = [
    # 接口管理
    url(settings.PROJECT_NAME + '/', include('main.urls')),
]

urlpatterns += [
    # admin
    path(settings.PROJECT_NAME + '/admin/', admin.site.urls),
    # static: 高版本中有的可以手动配置, 但要注意官方文档中写明的生产环境下是否开放.
    re_path(
        # r'^apis/static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}
        rf'{settings.PROJECT_NAME}/static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}
    ),
]
