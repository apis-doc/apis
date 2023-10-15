# --*--*--*--*--*--*- Create by bh at 2023/10/5 15:26 -*--*--*--*--*--*--


class Err(Exception):
    def __init__(self, code='1000', msg='', detail=''):
        super().__init__(Err, )
        self.code = code
        self.msg = msg
        self.detail = detail


class ClientErr(Err):

    def __init__(self, msg, code='4000', detail=''):
        default_msg = msg or '访问端错误,请仔细核对流程后重试'
        super().__init__(code=code, msg=default_msg, detail=detail)


class ServerErr(Err):
    def __init__(self, msg, code='5000', detail=''):
        default_msg = msg or '服务端错误, 请稍后重试'
        super().__init__(code=code, msg=default_msg, detail=detail)


class UnknownErr(Err):
    def __init__(self, code='9999', detail=''):
        super().__init__(code, '未知错误,请稍后重试', detail=detail)
