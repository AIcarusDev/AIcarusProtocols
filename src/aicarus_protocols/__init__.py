# src/aicarus_protocols/__init__.py
"""AIcarus-Message-Protocol v1.6.0 Python 实现.

本模块根据 AIcarus Message Protocol version 1.6.0 定义了数据结构.
"""

# 核心数据结构
from .constants import PROTOCOL_VERSION, ConversationType, EventTypePrefix
from .conversation_info import ConversationInfo
from .event import Event
from .event_builder import EventBuilder
from .event_type import EventType, validate_event_type

# 构建器和常量
from .seg import Seg, SegBuilder
from .user_info import UserInfo

# 工具函数
from .utils import extract_text_from_content, filter_segs_by_type, find_seg_by_type

__version__ = "1.6.0"
__all__ = [
    "PROTOCOL_VERSION",
    "ConversationInfo",
    "ConversationType",
    "Event",
    "EventBuilder",
    "EventType",
    "EventTypePrefix",
    "Seg",
    "SegBuilder",
    "UserInfo",
    "extract_text_from_content",
    "filter_segs_by_type",
    "find_seg_by_type",
    "validate_event_type",
]
