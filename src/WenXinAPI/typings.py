"""
包含项目所需自定义类型的模块
"""
from enum import Enum, unique


@unique
class ENGINE(Enum):
    """
    对话引擎枚举类
    """
    ERNIE_BOT = "ERNIE-Bot"
    ERNIE_BOT_TURBO = "ERNIE-Bot-turbo"
    BLOOMZ_7B = "BLOOMZ-7B"


@unique
class ENDPOINT(Enum):
    """
    请求终点枚举类
    """
    ERNIE_BOT = "completions"
    ERNIE_BOT_TURBO = "eb-instant"
    BLOOMZ_7B = "bloomz_7b1"


@unique
class ROLE(Enum):
    """
    对话角色枚举类
    """
    USER = "user"
    ASSISTANT = "assistant"


class ChatBotError(Exception):
    """
    所有机器人错误的基类
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ActionsError(ChatBotError):
    """
    ChatBotError的子类，代表行为错误
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class AuthenticationError(ChatBotError):
    """
    ChatBotError的子类，代表验证错误
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class APIConnectionError(ChatBotError):
    """
    ChatBotError的子类，代表API连接错误
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ResponseError(ChatBotError):
    """
    ChatBotError的子类，代表响应错误
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NotAllowRunningError(ChatBotError):
    """
    ChatBotError的子类，代表不允许运行错误
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)




