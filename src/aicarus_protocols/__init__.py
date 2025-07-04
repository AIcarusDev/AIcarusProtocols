# src/aicarus_protocols/__init__.py
"""
AIcarus-Message-Protocol v1.6.0 Python 实现
本模块根据 AIcarus Message Protocol version 1.6.0 定义了数据结构。
"""

# 核心数据结构
from .user_info import UserInfo
from .conversation_info import ConversationInfo
from .seg import Seg
from .event import Event

# 构建器和常量
from .seg import SegBuilder
from .event_builder import EventBuilder
from .constants import PROTOCOL_VERSION, ConversationType, EventTypePrefix
from .event_type import EventType, validate_event_type

# 工具函数
from .utils import extract_text_from_content, find_seg_by_type, filter_segs_by_type

__version__ = "1.6.0"
__all__ = [
    # 核心数据结构
    "Event",
    "UserInfo",
    "ConversationInfo",
    "Seg",
    # 构建器
    "SegBuilder",
    "EventBuilder",
    # 常量
    "PROTOCOL_VERSION",
    "ConversationType",
    "EventTypePrefix",
    # 事件类型系统
    "EventType",
    "validate_event_type",
    # 工具函数
    "extract_text_from_content",
    "find_seg_by_type",
    "filter_segs_by_type",
]
