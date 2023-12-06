# --*--*--*--*--*--*- Create by bh at 2023/10/5 14:27 -*--*--*--*--*--*--
import datetime
from django.db.models import ForeignKey


class Dao(object):

    def __init__(self, model, using='default', contains=None, startswith=None):
        self._md = model
        self.manage = self._md.objects if using == 'default' else self._md.objects.using(using)
        self._contains = contains or ()
        self._startswith = startswith or ()
        self.meta = self._md._meta

    def query(self, req_data, is_delete=True):
        if is_delete:
            req_data['delete_time'] = None
        return self.manage.filter(**self.params(origin=req_data))

    def params(self, origin: dict, update=False) -> dict:
        ret = dict()
        if update:
            origin['update_time'] = datetime.datetime.now()
        for field, value in origin.items():
            md_key = field.replace('_id', '').split('__')[0]
            if not hasattr(self._md, md_key):
                continue
            if field in self.foreign_keys() and isinstance(value, (int, str)):
                field = f'{field}_id'
            ret[field] = value
        return ret

    def where(self, origin: dict, equal=None) -> dict:
        equal = equal or ('username', 'password', 'id', 'det_site_id')
        ret = dict() if not hasattr(self._md, 'delete_time') else dict(delete_time=None)
        for key, value in origin.items():
            if not value and not isinstance(value, bool) and value is not 0:
                continue
            # $外键_id, $外键__外键model属性
            md_key = key.replace('_id', '').split('__')[0]
            if not hasattr(self._md, md_key):
                continue
            ret_key = key
            # Process the original field value. The field name does not correspond to the value
            if key in self.foreign_keys() and isinstance(value, (int, str)):
                key = f'{key}_id'
            if key in self._contains:
                ret_key = f'{key}__contains'
            elif key in self._startswith:
                ret_key = f'{key}__istartswith'
            # It is mutually exclusive with fuzzy matching
            if isinstance(value, (list, set, tuple)):
                if key.endswith('time'):
                    ret_key = f'{key}__range'
                else:
                    ret_key = f'{key}__in'
            # default, like '$value%',when not start_with
            if not self._startswith and isinstance(value, str):
                if key in origin.keys() and key not in equal:  # <== key = f'{key}_id'
                    ret_key = f'{key}__istartswith'
            ret[ret_key] = value
        return ret

    def foreign_keys(self) -> list:
        return [f.name for f in self.meta.local_fields if isinstance(f, ForeignKey)]

    def pk_name(self) -> str:
        return self.meta.pk.name

    def fields(self):
        return [f.attname for f in self.meta.concrete_fields]

    def verbose_names(self, *args):
        ret = dict()
        for field_name in args:
            for field in self.meta.local_fields:
                if field_name == field.name:
                    ret[field_name] = field.verbose_name
                    break
        return ret
