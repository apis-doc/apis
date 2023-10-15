from main.utils.redis_utils import RedisUtil
from django.conf import settings

rd = RedisUtil(pwd=settings.REDIS_HOST)
