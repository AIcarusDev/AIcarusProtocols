# src/aicarus_protocols/constants.py
"""
AIcarus-Message-Protocol v1.6.0 - 协议常量
"""

# 协议版本
PROTOCOL_VERSION = "1.6.0"


class ConversationType:
    """会话类型常量定义。"""

    PRIVATE = "private"
    GROUP = "group"
    CHANNEL = "channel"
    UNKNOWN = "unknown"


class EventTypePrefix:
    """事件类型前缀常量，定义基础的事件分类。"""

    MESSAGE = "message"
    NOTICE = "notice"
    REQUEST = "request"
    ACTION = "action"
    ACTION_RESPONSE = "action_response"
    META = "meta"
