# --*--*--*--*--*--*- Create by bh at 2023/10/4 10:36 -*--*--*--*--*--*--
from django.db import models

ContentType = (
    (0, 'application/json'), (1, 'text/html'), (2, 'multipart/form-data'), (3, 'text/plain'),
    (4, 'application/xml'), (5, 'application/x-www-form-urlencoded'),
)


class Project(models.Model):
    code = models.CharField(max_length=12, verbose_name='编码')
    name = models.CharField(max_length=30, default='', verbose_name='名称')
    maintainer = models.CharField(max_length=80, default='', verbose_name='维护人')
    note = models.TextField(default='', verbose_name='备注')

    port = models.CharField(max_length=6, verbose_name='端口')
    host = models.CharField(max_length=18, default='127.0.0.1', verbose_name='IP')

    encrypt_mode = models.TextField(default='无', verbose_name='加密方式')
    sign_mode = models.TextField(default='无', verbose_name='签名方式')

    create_by = models.CharField(max_length=15, default='', verbose_name='创建人')
    create_time = models.DateTimeField(auto_created=True, auto_now=False, auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name
        db_table = 'projects'

    def __str__(self):
        return self.name


class Api(models.Model):
    owner = models.ForeignKey(to=Project, on_delete=models.PROTECT, verbose_name='所属项目')

    path = models.CharField(max_length=50, db_index=True, verbose_name='uri')
    interface_id = models.CharField(max_length=30, default='', verbose_name='method-接口标识')
    api_type = models.IntegerField(default=0, verbose_name='接口类型', choices=(
        (0, 'GateWay'), (1, 'restful'), (3, 'other')
    ))
    method = models.IntegerField(default=0, verbose_name='请求类型', choices=(
        (0, 'POST'), (1, 'GET'), (2, 'DELETE'), (3, 'PUT')
    ))
    # https://www.runoob.com/http/http-content-type.html
    content_type = models.IntegerField(default=0, verbose_name='请求体类型', choices=ContentType)
    api_name = models.CharField(max_length=50, verbose_name='接口名称')
    describe = models.CharField(max_length=500, default='', verbose_name='描述')
    version = models.CharField(max_length=6, default='1.0.0', verbose_name='版本')
    state = models.IntegerField(default=0, verbose_name='状态', choices=(
        (0, '服务中'), (1, '已下线'), (3, '已迭代'), (4, '开发中'), (5, '迭代中-新接口并行服务中')
    ))
    Attentions = models.CharField(max_length=800, default='', verbose_name='注意项')
    note = models.TextField(default='', verbose_name='备注')
    maintainer = models.CharField(max_length=150, default='', verbose_name='维护人')

    is_login = models.BooleanField(default=True, verbose_name='是否需要登录')
    require_auth = models.CharField(max_length=60, default='', verbose_name='权限')

    req_example = models.TextField(default='', verbose_name='请求示例')
    rsp_example = models.TextField(default='', verbose_name='返回示例')

    create_time = models.DateTimeField(auto_created=True, auto_now=False, auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_created=False, auto_now=True, verbose_name='更新时间')
    create_by = models.CharField(max_length=15, default='', verbose_name='创建人')
    update_by = models.CharField(max_length=15, default='', verbose_name='更新人')

    class Meta:
        verbose_name = '接口'
        verbose_name_plural = verbose_name
        db_table = 'apis'

    def __str__(self):
        suffix = f'({self.method})' if self.method else ''
        return f'{self.path}{suffix}'


class Params(models.Model):
    code = models.CharField(max_length=30, verbose_name='参数代码')
    name = models.CharField(max_length=50, verbose_name='参数名称')
    param_type = models.IntegerField(default=0, verbose_name='参数类型', choices=(
        (0, 'str'), (1, 'integer'), (2, 'boolean'), (3, 'datetime'), (4, 'array'), (5, 'object')
    ))
    is_require = models.BooleanField(default=False, verbose_name='是否必传')
    is_null = models.BooleanField(default=True, verbose_name='是否可为空')
    example = models.CharField(max_length=30, default='', verbose_name='示例')
    note = models.CharField(max_length=300, default='', verbose_name='备注')

    is_service = models.BooleanField(default=True, db_index=True, verbose_name='是否服务中')
    owner = models.ForeignKey(to=Api, on_delete=models.PROTECT, verbose_name='所属接口')

    create_time = models.DateTimeField(auto_created=True, auto_now=False, auto_now_add=True, verbose_name='创建时间')
    # updated_at = models.DateTimeField(auto_created=False, auto_now=True, verbose_name='更新时间')
    create_by = models.CharField(max_length=15, default='', verbose_name='创建人')

    # update_by = models.CharField(max_length=15, default='', verbose_name='更新人')

    class Meta:
        verbose_name = '参数'
        verbose_name_plural = verbose_name
        db_table = 'params'

    def __str__(self):
        return f'{self.name}({self.code})'


class RequestLog(models.Model):
    """记录调用方的请求, 该表会作为接口的数据源"""
    path = models.CharField(max_length=50, db_index=True, verbose_name='uri')
    interface_id = models.CharField(max_length=30, default='', verbose_name='method-接口标识')
    api_type = models.IntegerField(default=0, verbose_name='接口类型', choices=(
        (0, 'GateWay'), (1, 'restful'), (3, 'other')
    ))
    method = models.CharField(max_length=8, default='', verbose_name='请求类型')
    content_type = models.CharField(max_length=30, default='', verbose_name='请求体类型')
    req = models.TextField(default='', verbose_name='请求示例')
    rsp = models.TextField(default='', verbose_name='返回示例')
    err = models.TextField(default='', verbose_name='异常信息')
    status_code = models.IntegerField(default=0, verbose_name='状态码')
    create_time = models.DateTimeField(auto_created=True, auto_now=False, auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '接口库表'
        verbose_name_plural = verbose_name
        db_table = 'request_logs'
