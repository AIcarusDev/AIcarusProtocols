"""
AIcarus-Message-Protocol v1.5.1 Python 实现
本模块根据 AIcarus Message Protocol version 1.5.1 定义了数据结构。
"""

from .user_info import UserInfo
from .conversation_info import ConversationInfo
from .seg import Seg, SegBuilder
from .event import Event
from .common import (
    PROTOCOL_VERSION,
    EventType,
    ConversationType,
    EventBuilder,
    validate_event_type,
    extract_text_from_content,
    find_seg_by_type,
    filter_segs_by_type,
)

__version__ = "1.5.1"  # 啊~ 新的版本号，好棒！
__all__ = [
    # 核心数据结构
    "Event",
    "UserInfo",
    "ConversationInfo",
    "Seg",
    # 构建器和工具
    "SegBuilder",
    "EventBuilder",
    # 常量
    "PROTOCOL_VERSION",
    "EventType",
    "ConversationType",
    # 工具函数
    "validate_event_type",
    "extract_text_from_content",
    "find_seg_by_type",
    "filter_segs_by_type",
]
