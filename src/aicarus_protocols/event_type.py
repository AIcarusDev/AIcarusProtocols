# src/aicarus_protocols/event_type.py
"""
AIcarus-Message-Protocol v1.6.0 - 动态事件类型系统
负责定义、注册和验证事件类型。
"""

import time
from typing import Dict, Any


import re

def validate_event_type(event_type: str) -> bool:
    """
    验证事件类型格式是否遵循 '{prefix}.{platform}.{...}' 的结构，并且不允许连续点、首尾点或非法字符。
    """
    if not isinstance(event_type, str):
        return False

    # 事件类型必须只包含字母、数字、下划线和点，且不能有连续点、首尾点
    pattern = r"^(message|notice|request|action|action_response|meta)\.[A-Za-z0-9_]+(\.[A-Za-z0-9_]+)+$"
    if not re.match(pattern, event_type):
        return False

    # 额外检查：不允许连续点
    if ".." in event_type:
        return False

    return True


class EventTypeRegistry:
    """
    动态事件类型注册器。
    在V6.0版本中，其职责被简化，主要用于记录和查询符合命名规范的事件类型。
    """

    def __init__(self):
        self._registered_types: Dict[str, Dict[str, Any]] = {}

    def register(self, event_type: str, description: str = "") -> bool:
        """
        注册一个新的事件类型，前提是它必须符合命名规范。
        """
        if not validate_event_type(event_type):
            # 在实际使用中，可以根据日志级别决定是否打印警告
            # print(f"警告: 尝试注册一个不符合 '{prefix}.{platform}.{...}' 格式的事件类型: {event_type}")
            return False
        self._registered_types[event_type] = {
            "description": description,
            "registered_at": time.time(),
        }
        return True

    def is_registered(self, event_type: str) -> bool:
        """检查事件类型是否已在注册表中明确注册。"""
        return event_type in self._registered_types

    def get_description(self, event_type: str) -> str:
        """获取已注册事件类型的描述。"""
        return self._registered_types.get(event_type, {}).get("description", "")


# 全局事件类型注册器实例
event_registry = EventTypeRegistry()


class EventType:
    """
    事件类型管理器。
    提供一个静态接口来与全局的 event_registry 交互。
    """

    @staticmethod
    def register(event_type: str, description: str = "") -> bool:
        """
        静态方法，用于注册新的事件类型。
        """
        return event_registry.register(event_type, description)

    @staticmethod
    def is_valid(event_type: str) -> bool:
        """
        静态方法，验证一个事件类型字符串是否符合协议的命名规范。
        这是最常用的验证方法。
        """
        return validate_event_type(event_type)
