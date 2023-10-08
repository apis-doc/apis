# --*--*--*--*--*--*- Create by bh at 2023/10/3 10:53 -*--*--*--*--*--*--
import logging
import json
from django.conf import settings
from main.utils.common import contains


class Log(object):

    def __init__(self, name, aes_key=settings.SECRET_KEY):
        self._log = logging.getLogger(name)
        self._aes_key = aes_key[:32]

    def info(self, dt: any, encrypt=False, key_word='None'):
        self.put('info', self.encrypt(dt, key_word=key_word) if encrypt else dt)

    def encrypt(self, log_data: object, key_word=''):
        """
        记录敏感信息: 采用与mysql数据库相同的算法，便于解密
        """
        return log_data
        # todo python3.9 encrypt method

    def put(self, level, msg):
        attr_name = level.lower()
        if not hasattr(self._log, attr_name):
            if settings.DEBUG:
                raise Exception(f"{self._log.name} has not {attr_name}")
            return None
        msg = msg if not self.has_sensitive_key(msg) else self.encrypt(msg, key_word='put')
        if not isinstance(msg, str):
            msg = json.dumps(msg, sort_keys=True, ensure_ascii=True, separators=(', ', ': '))
        getattr(self._log, attr_name)(msg)

    def has_sensitive_key(self, msg):
        # 为了全匹配，key->'key'
        encrypt_keys = settings.ENCRYPT_KEYS
        return contains(msg, [f"'{key}'" for key in encrypt_keys])
