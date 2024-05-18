# --*--*--*--*--*--*- Create by bh at 2023/10/5 14:12 -*--*--*--*--*--*--
from main.models import *
from main.daos.base_dao import Dao

pro_dao = Dao(model=Project, contains=('name', 'maintainer', 'note', 'create_by'))
api_dao = Dao(
    model=Api,
    contains=('interface_id', 'api_name', 'describe', 'Attentions', 'note', 'maintainer'),
    startswith=('path',)
)
prm_dao = Dao(model=Params, contains=('note',), startswith=('code',))
req_log_dao = Dao(
    model=RequestLog,
    contains=('interface_id', 'req', 'rsp'),
    startswith=('path',),
)

user_dao = Dao(
    model=User,
    contains=('first_name', 'last_name'),
    startswith=('username',)
)
gup_dao = Dao(
    model=Group,
    contains=('name',)
)
pms_dao = Dao(
    model=Permission,
    contains=('name',)
)

ntc_dao = Dao(
    model=Notice,
)

rla_dao = Dao(
    model=Release, startswith=('content',)
)

uc_dao = Dao(
    model=UserConfig,
)
