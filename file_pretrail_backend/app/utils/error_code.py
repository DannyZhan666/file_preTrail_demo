from enum import Enum


class ErrorCode(Enum):
    SUCCESS = 0, "ok", ""
    PARAMS_ERROR = 400, "请求参数错误", "参数验证失败"
    NULL_ERROR = 401, "请求数据为空", "请求数据不可为空"
    ACC_PWD_ERROR = 402, "账号密码错误", "账号或密码错误"
    NOT_LOGIN = 4010, "未登录", "用户未登录"
    NO_AUTH = 4011, "无权限", "用户无权限访问"
    SYSTEM_ERROR = 5000, "系统错误", "系统内部错误"

    def __init__(self, code, msg, description):
        self.code = code
        self.msg = msg
        self.description = description

    def get_code(self):
        return self.code

    def get_msg(self):
        return self.msg

    def get_description(self):
        return self.description
