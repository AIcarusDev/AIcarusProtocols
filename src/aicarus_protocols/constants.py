# src/aicarus_protocols/constants.py
"""AIcarus-Message-Protocol v1.6.0 - 协议常量."""

# 协议版本
PROTOCOL_VERSION = "1.6.0"


class ConversationType:
    """会话类型常量定义.

    定义了不同类型的会话，用于标识消息的来源和目标.

    Attributes:
        PRIVATE (str): 私聊会话类型.
        GROUP (str): 群组会话类型.
        CHANNEL (str): 频道会话类型.
        UNKNOWN (str): 未知会话类型.
    """

    PRIVATE = "private"
    GROUP = "group"
    CHANNEL = "channel"
    UNKNOWN = "unknown"


class EventTypePrefix:
    """事件类型前缀常量，定义基础的事件分类.

    Attributes:
        MESSAGE (str): 消息事件类型前缀.
        NOTICE (str): 通知事件类型前缀.
        REQUEST (str): 请求事件类型前缀.
        ACTION (str): 动作事件类型前缀.
    """

    MESSAGE = "message"
    NOTICE = "notice"
    REQUEST = "request"
    ACTION = "action"
    ACTION_RESPONSE = "action_response"
    META = "meta"
