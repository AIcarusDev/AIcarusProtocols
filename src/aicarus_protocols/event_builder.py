# src/aicarus_protocols/event_builder.py
"""
AIcarus-Message-Protocol v1.6.0 - Event 构建器
提供快速创建各种标准事件对象的方法。
"""

import uuid
import time
from typing import Dict, Any, List, Optional

from .event import Event
from .seg import Seg, SegBuilder
from .user_info import UserInfo
from .conversation_info import ConversationInfo


class EventBuilder:
    """Event 构建器，提供快速创建各种事件的方法。"""

    @staticmethod
    def generate_event_id() -> str:
        """生成唯一的事件ID。"""
        return str(uuid.uuid4())

    @staticmethod
    def get_current_timestamp() -> float:
        """获取当前Unix毫秒时间戳。"""
        return time.time() * 1000

    @staticmethod
    def create_message_event(
        event_type: str,
        bot_id: str,
        message_id: str,
        content_segs: List[Seg],
        user_info: Optional[UserInfo] = None,
        conversation_info: Optional[ConversationInfo] = None,
        **kwargs,
    ) -> Event:
        """创建消息事件。event_type 应为 "message.{platform}.{...}" 格式。"""
        metadata_seg = SegBuilder.message_metadata(message_id, **kwargs)
        all_content = [metadata_seg] + content_segs

        return Event(
            event_id=EventBuilder.generate_event_id(),
            event_type=event_type,
            time=EventBuilder.get_current_timestamp(),
            bot_id=bot_id,
            content=all_content,
            user_info=user_info,
            conversation_info=conversation_info,
        )

    @staticmethod
    def create_action_response_event(
        response_type: str,  # e.g., "success"
        original_event: Event,
        status_code: Optional[int] = None,
        message: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Event:
        """创建动作响应事件。"""
        original_platform = original_event.get_platform() or "unknown"
        response_event_type = f"action_response.{original_platform}.{response_type}"

        response_data = {
            "original_event_id": original_event.event_id,
            "original_action_type": original_event.event_type,
        }
        if status_code is not None:
            response_data["status_code"] = status_code
        if message is not None:
            response_data["message"] = message
        if data is not None:
            response_data["data"] = data

        response_seg = Seg(type=response_event_type, data=response_data)

        return Event(
            event_id=EventBuilder.generate_event_id(),
            event_type=response_event_type,
            time=EventBuilder.get_current_timestamp(),
            bot_id=original_event.bot_id,
            content=[response_seg],
        )

    # ... 可以根据需要添加其他 create_*_event 方法，都移除 platform 参数 ...
