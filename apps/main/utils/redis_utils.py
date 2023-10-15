# --*--*--*--*--*--*- Create by bh at 2023/10/14 14:09 -*--*--*--*--*--*--
import redis
import json
from django.conf import settings as rc


class RedisUtil(object):
    """Attention: 用起来有点麻烦，待升级"""

    def __init__(self, port=rc.REDIS_PORT, host=rc.REDIS_HOST, db=rc.REDIS_DB, pwd=None):
        self._port = port
        self._host = host
        self._db = db
        self._pwd = pwd
        self._prefix = rc.XMMC
        self.r = self.get_redis()

    def update_or_create(self, key: str, value, add=None):
        """
        仅更新或创建redis中name对应的value. 从第一次set开始计算过期时间.
        :param key: redis config中的key
        :param value:
        :param add: redis.name 拼接的字符串
        :return:
        """
        create_ex = None
        name = self.name(key, add)
        update_ex = self.r.ttl(name)
        # https://redis.io/commands/ttl/
        ex = create_ex if update_ex <= 0 else update_ex
        return self.set(key, value, ex, add)

    def set(self, key: str, value, ex=None, add=None):
        if ex is None:
            # 默认过期时间从当前时间开始计算
            ex = self.config(key).get('ex', 3)
        return self.r.set(self.name(key, add), value, ex)

    def get(self, key, add=None):
        return self.r.get(self.name(key, add))

    def incrby(self, key: str, amount=None, add=None):
        return self.r.incrby(self.name(key, add), amount=amount)

    def config(self, key):
        return rc.REDISCONF.get(key.upper(), {})

    def name(self, key: str, add=None) -> str:
        """
        :param key: redis配置项中的key
        :param add: redis set 参数key中的拼接的不固定字符串
        :return2.0.0: redis set 参数key
        :return1.0.0: (key对应的redis配置:如ex等，redis set 参数key)
        """
        config = self.config(key)
        eles = [self._prefix, config.get('suffix', 'unnamed')]
        if add is not None:
            eles.append(add)
        return '.'.join(eles)

    def get_redis(self, use_pool=True):
        kwrgs = {
            'host': self._host,
            'port': self._port,
            'db': self._db,
            'decode_responses': True,
            'password': self._pwd,
        }
        # 支持 password 为None，代表没有密码, decode_responses=True, 配置取出数据是字符串
        if use_pool:
            return redis.Redis(connection_pool=redis.ConnectionPool(**kwrgs))
        return redis.Redis(**kwrgs)


class RedisEncrypt(object):

    def __init__(self, key=None, redis_obj=None):
        self.redis = redis_obj if redis_obj else RedisUtil()
        self._key = key if key else rc.SECRET_KEY[:32]

    def push(self, redis_key, value, encrypt_func, push_func='set', redis_kwargs=None, json_kwargs=None):
        if not value:
            return
        redis_kwargs = redis_kwargs or dict()
        json_kwargs = json_kwargs or dict()
        value = json.dumps(value, **json_kwargs)
        encrypt_value = encrypt_func(self._key, value)
        return getattr(self.redis, push_func)(redis_key, encrypt_value, **redis_kwargs)

    def get(self, redis_key, decrypt_func, add=None):
        redis_value = self.redis.get(redis_key, add=add)
        if not redis_value:
            return None
        decrypt_value = decrypt_func(self._key, redis_value)
        return json.loads(decrypt_value)
