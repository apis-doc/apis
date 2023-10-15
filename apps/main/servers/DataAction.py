# --*--*--*--*--*--*- Create by bh at 2023/10/5 15:23 -*--*--*--*--*--*--
import datetime
from main.daos import Dao
from main.servers.Err import ClientErr, UnknownErr
from django.conf import settings as conf
from django.db.utils import IntegrityError


class DataActionView(object):
    def __init__(self, request, dao: Dao, unique_fs=None):
        self.params = request.request_data
        self.user = request.user

        self.dao = dao
        self.pk_name = self.dao.pk_name()
        self.unique_fs = unique_fs or tuple()

    def is_repeat(self, **fields) -> list:
        fields = fields or self.dao.verbose_names(*self.unique_fs)
        err_msg = []
        for field_name in fields.keys():
            value = self.params.get(field_name)
            pks = self.dao.query({field_name: value}).values_list(self.pk_name, flat=True)
            if pks and pks[0] != self.params.get(self.pk_name):
                verbose_name = fields.get(field_name, field_name)
                err_msg.append(f'{verbose_name}({value})')
        if err_msg:
            raise ClientErr(msg=f'{"、".join(err_msg)}重复')
        return err_msg

    def exist_foreign(self):
        # Implement me
        return None

    def delete(self, obj_id=None, range_query=None, **_) -> dict:
        obj_id = obj_id or self.params.get(self.pk_name)
        if not object:
            raise ClientErr(msg=f'未传入主键标识({self.pk_name})，请刷新后重试')
        objs = self.dao.query({self.pk_name: obj_id})
        if not objs:
            raise ClientErr(msg=f'数据({obj_id})不存在或已经删除，请刷新后重试')
        if range_query and not objs.filter(**range_query):
            raise ClientErr(msg=f'删除失败，数据({obj_id})不在您的操作范围内')
        obj = objs[0]
        if hasattr(obj, 'delete_time'):
            obj.delete_time = datetime.datetime.now()
            obj.save()
        else:
            self.dao.manage.filter(**self.params).delete()
        return dict()

    def create(self, **_) -> dict:
        for fun in [self.is_repeat, self.exist_foreign]:
            fun()
        try:
            self.dao.manage.create(**self.dao.params(self.params))
        except IntegrityError as e:
            self.db_error(e)
        return dict()

    def page(self, is_display=False, dt_range=None, **kwargs) -> dict:
        page_index = int(self.params.get('page_number', 1))
        offset = int(self.params.get('page_size', 2))
        start = (page_index - 1) * offset
        end = page_index * offset
        filter_params = self.dao.where(self.params)
        print('page->where: ', filter_params)
        dt_range = dt_range or dict()
        filter_params.update(**dt_range)  # 数据权限
        objs = self.dao.manage.filter(**filter_params)
        if kwargs.get('extra'):
            objs = objs.extra(**kwargs.get('extra'))
        if kwargs.get('values'):
            objs = objs.values(*kwargs.get('values'))
        else:
            objs = objs.values()
        if is_display:
            return {'show_info': self.display_foreign_fields(objs[start:end]), 'count': objs.count()}
        return {'show_info': tuple(objs[start:end]), 'count': objs.count()}

    def detail(self, **_) -> dict:
        pk_value = self.params.pop(self.pk_name, '')
        objs = self.dao.query({self.pk_name: pk_value})
        if not objs:
            raise ClientErr(msg=f'该数据({pk_value})不存在或已被删除，请刷新后重试')
        return objs.values()[0]

    def update(self, range_query=None, **_) -> dict:
        pk_value = self.params.get(self.pk_name, '')
        if not pk_value:
            raise ClientErr(msg=f'未传入标识主键({self.pk_name})，请刷新后重试')
        for check_fun in [self.is_repeat, self.exist_foreign]:
            check_fun()
        try:
            filters = {'delete_time': None, self.pk_name: pk_value}
            if range_query:  # 只能操作自己权限范围内的数据
                filters.update(**range_query)
            self.dao.query(filters).update(**self.dao.params(self.params))
        except IntegrityError as e:
            self.db_error(e)
        return dict()

    def db_error(self, e: Exception):
        """处理数据库异常: Attention: 当前数据库是mysql"""
        err_msg = str(e)
        if err_msg.find('1062') > 0 and err_msg.find('Duplicate') > 0 and err_msg.find('PRIMARY') > 0:
            pk_field_name = self.dao.verbose_names(self.pk_name).get(self.pk_name)
            raise ClientErr(msg=f'主键标识({pk_field_name})重复, 请核对后重试')
        raise UnknownErr(detail=err_msg)

    def display_foreign_fields(self, objs):
        """获取外键字段的显示字段：将复杂、冗长的外键字段转换为定义的显示字段给前端"""
        ret = []
        for obj in objs:
            new = {}
            for field, value in obj.items():
                if field in conf.FOREIGN_FIELDS.keys():
                    field = conf.FOREIGN_FIELDS[field]
                new[field] = value
            ret.append(new)
        return ret
