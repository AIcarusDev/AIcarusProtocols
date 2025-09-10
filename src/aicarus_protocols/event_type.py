# src/aicarus_protocols/event_type.py
"""AIcarus-Message-Protocol v1.6.0 - 动态事件类型系统.

负责定义、注册和验证事件类型.
"""

import re
import time
from typing import Any


def validate_event_type(event_type: str) -> bool:
    """验证一个事件类型字符串是否符合协议的命名规范.

    事件类型必须以 "message", "notice", "request", "action", "action_response" 或 "meta" 开头，
    并且后面跟随一个或多个由点分隔的标识符，标识符只能包含字母、数字、下划线和点.

    Args:
        event_type (str): 要验证的事件类型字符串.

    Returns:
        bool: 如果事件类型符合规范，返回 True；否则返回 False.
    """
    if not isinstance(event_type, str):
        return False

    # 事件类型必须只包含字母、数字、下划线和点，且不能有连续点、首尾点
    pattern = (
        r"^(message|notice|request|action|action_response|meta|system)\.[A-Za-z0-9_]+(\.[A-Za-z0-9_]+)*$"
    )
    if not re.match(pattern, event_type):
        return False

    # 额外检查：不允许连续点
    return ".." not in event_type


class EventTypeRegistry:
    """动态事件类型注册器.

    在V1.6.0版本中，其职责被简化，主要用于记录和查询符合命名规范的事件类型.

    Attributes:
        _registered_types (dict[str, dict[str, Any]]): 存储已注册事件类型的字典，
            键为事件类型字符串，值为包含描述和注册时间的字典.

    Methods:
        register(event_type: str, description: str = "") -> bool: 注册一个新的事件类型，
            前提是它必须符合命名规范.
        is_registered(event_type: str) -> bool: 检查事件类型是否已在注册表中明确注册.
        get_description(event_type: str) -> str: 获取已注册事件类型的描述.
    """

    def __init__(self) -> None:
        self._registered_types: dict[str, dict[str, Any]] = {}

    def register(self, event_type: str, description: str = "") -> bool:
        """注册一个新的事件类型，前提是它必须符合命名规范.

        Args:
            event_type (str): 要注册的事件类型字符串.
            description (str): 事件类型的描述信息.

        Returns:
            bool: 如果注册成功返回 True，否则返回 False.
        """
        if not validate_event_type(event_type):
            # 在实际使用中，可以根据日志级别决定是否打印警告
            return False
        self._registered_types[event_type] = {
            "description": description,
            "registered_at": time.time(),
        }
        return True

    def is_registered(self, event_type: str) -> bool:
        """检查事件类型是否已在注册表中明确注册.

        Args:
            event_type (str): 要检查的事件类型字符串.

        Returns:
            bool: 如果事件类型已注册，返回 True；否则返回 False.
        """
        return event_type in self._registered_types

    def get_description(self, event_type: str) -> str:
        """获取已注册事件类型的描述.

        Args:
            event_type (str): 要获取描述的事件类型字符串.

        Returns:
            str: 事件类型的描述，如果未找到则返回空字符串.
        """
        return self._registered_types.get(event_type, {}).get("description", "")


# 全局事件类型注册器实例
event_registry = EventTypeRegistry()


class EventType:
    """事件类型管理器.

    提供一个静态接口来与全局的 event_registry 交互.

    Attributes:
        event_registry (EventTypeRegistry): 全局事件类型注册器实例，用于注册和查询事件类型.

    Methods:
        register(event_type: str, description: str = "") -> bool: 静态方法，用于注册新的事件类型.
        is_valid(event_type: str) -> bool: 静态方法，验证一个事件类型字符串是否符合协议的命名规范.
    """

    @staticmethod
    def register(event_type: str, description: str = "") -> bool:
        """静态方法，用于注册新的事件类型.

        Args:
            event_type (str): 要注册的事件类型字符串.
            description (str): 事件类型的描述信息.

        Returns:
            bool: 如果注册成功返回 True，否则返回 False.
        """
        return event_registry.register(event_type, description)

    @staticmethod
    def is_valid(event_type: str) -> bool:
        """静态方法，验证一个事件类型字符串是否符合协议的命名规范.

        这是最常用的验证方法.

        Args:
            event_type (str): 要验证的事件类型字符串.

        Returns:
            bool: 如果事件类型符合规范，返回 True；否则返回 False.
        """
        return validate_event_type(event_type)
