# --*--*--*--*--*--*- Created by bh at 2022/5/20 14:08 -*--*--*--*--*--*--
# nohup tail -f request.log >>all.log 2>&1 &
import datetime
import logging
import os

from django.conf import settings


def request_handler(handler='request'):
    if settings.DEBUG:
        return [handler, 'console']
    return [handler]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'long_handle_time': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(settings.BASE_DIR, 'logs/long_handle_time.log'),
            'maxBytes': 1024 * 1024 * 30,
            'backupCount': 2,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        '500': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(settings.BASE_DIR, 'logs/500.log'),
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 2,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'request': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(settings.BASE_DIR, 'logs/request.log'),
            'when': 'MIDNIGHT',
            'interval': 1,
            'backupCount': 7,
            # 'atTime': datetime.time(0, 0, 0, 0),
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'task': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(settings.BASE_DIR, 'logs/task.log'),
            'maxBytes': 1024 * 1024 * 100,  # 100
            'backupCount': 2,  # 备份分数
            'formatter': 'verbose',  # 采用verbose为格式器
            'encoding': 'utf-8',
        },
        'web': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(settings.BASE_DIR, 'logs/web.log'),
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'error': {  # 按照大小轮转
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(settings.BASE_DIR, 'logs/error.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 3,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'task': {  # 定时任务|?|2
            'handlers': ['task'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',  # change debug level as appropiate'propagate':False,
        },
        'django.db.backends': {  # When debug is True, the sql log is printed to the console.
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        '500': {  # When debug is True, the sql log is printed to the console.
            'handlers': request_handler(handler='500'),
            'propagate': True,
            'level': 'DEBUG',
        },
        'request': {
            # 之所以不用 500 方式处理是因为这样对程序来说更简单, 不用在每个请求中都调用一次filter
            'handlers': request_handler(),
            'level': 'INFO',
            'propagate': True,
        },
        'long_time': {
            'handlers': ['long_handle_time'],
            'level': 'INFO',
            'propagate': True,
        },
        'web': {  # 运行日志|50M|3
            'handlers': ['web'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'error_record': {  # 错误日志|10M|3
            'handlers': ['error'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}

ENCRYPT_KEYS = (
    'password', 'token', 'COOKIE',
    'id_card', 'sfzmhm',
    'phone', 'sjh', 'lxdh',
    'address',
)

# 不记录到日志的请求-包含匹配到的suburi即可
ignore_log_request = (
    '__debug__',
    '/js/',
    '/css/',
    '/favio/',
)

# 需要加密请求体、返回体、其他数据的请求
encrypt_req_request = (  # 未启用
    'login/',
)
encrypt_rsp_request = ()

# 超时记录开关
is_log_long_time_request = True
long_time = 5

# 超长忽略数据
is_ignore_long_request = True
long_req_length = 1000
long_str = '数据过长，已忽略'

# 请求日志中将记录的数据体
log_req_keys = {
    'META': ('HTTP_USER_AGENT',),
}


def add_coloring_to_emit_ansi(fn):
    # add methods we need to the class
    def new(*args):
        level_no = args[1].levelno
        # fatal-red
        if level_no >= 50:
            color = '\x1b[31m'  # red
        # error-red
        elif level_no >= 40:
            # color = '\x1b[35m'  # pink
            color = '\x1b[31m'  # red
        # warning-yellow
        elif level_no >= 30:
            color = '\x1b[33m'  # yellow
        # info-green
        elif level_no >= 20:
            color = '\x1b[32m'  # green
        # debug-blue
        elif level_no >= 10:
            # color = '\x1b[30m'  # 白
            color = '\x1b[34m'  # 蓝
            # color = '\x1b[32m'  # green
            # color = '\x1b[37m'  # 灰
            # color = '\x1b[35m'  # pink
        else:
            color = '\x1b[0m'  # normal
        try:
            args[1].msg = color + args[1].msg + '\x1b[0m'  # normal
        except Exception as e:
            if settings.DEBUG:
                print('add_coloring_to_emit_ansi warning: ', e)
        return fn(*args)

    return new


logging.StreamHandler.emit = add_coloring_to_emit_ansi(logging.StreamHandler.emit)
