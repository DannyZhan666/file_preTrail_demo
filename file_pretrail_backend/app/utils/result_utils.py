from app.utils.error_code import ErrorCode
from app.schemas.response import BaseResponse, T


class ResultUtils:
    @staticmethod
    def success(data) -> BaseResponse:
        """
        成功返回
        :param data: 返回的数据
        :return: BaseResponse
        """
        return BaseResponse[T](code=200, data=data, msg="ok")

    @staticmethod
    def error(error_code: ErrorCode) -> BaseResponse:
        """
        失败返回（基于 ErrorCode）
        :param error_code: 错误代码
        :return: BaseResponse
        """
        return BaseResponse[T](code=error_code.get_code(), data=None, msg=error_code.get_msg(),
                               description=error_code.get_description())

    @staticmethod
    def error_with_details(code: int, msg: str, description: str) -> BaseResponse:
        """
        自定义错误返回（通过传入 code, msg, description）
        :param code: 错误代码
        :param msg: 错误消息
        :param description: 错误描述
        :return: BaseResponse
        """
        return BaseResponse[T](code=code, data=None, msg=msg, description=description)

    @staticmethod
    def error_with_custom_error_code(error_code: ErrorCode, msg: str, description: str) -> BaseResponse:
        """
        自定义错误返回（基于 ErrorCode 和自定义 msg, description）
        :param error_code: 错误代码
        :param msg: 错误消息
        :param description: 错误描述
        :return: BaseResponse
        """
        return BaseResponse[T](code=error_code.get_code(), data=None, msg=msg, description=description)

    @staticmethod
    def error_with_custom_description(error_code: ErrorCode, description: str) -> BaseResponse:
        """
        自定义错误描述返回（基于 ErrorCode 和自定义 description）
        :param error_code: 错误代码
        :param description: 错误描述
        :return: BaseResponse
        """
        return BaseResponse[T](code=error_code.get_code(), data=None, msg=error_code.get_msg(), description=description)
