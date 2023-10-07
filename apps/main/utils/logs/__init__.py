# --*--*--*--*--*--*- Create by bh at 2023/10/3 10:53 -*--*--*--*--*--*--
from main.utils.logs.log_server import Log

web = Log(name='web')
error = Log(name='error_record')
task = Log(name='task')
req_log = Log(name='request')
exception = Log(name='500')
long = Log(name='long_time')
