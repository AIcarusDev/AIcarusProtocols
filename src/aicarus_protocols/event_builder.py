# src/aicarus_protocols/event_builder.py
"""AIcarus-Message-Protocol v1.6.0 - Event 构建器.

提供快速创建各种标准事件对象的方法.
"""

import time
import uuid
from typing import Any

from .conversation_info import ConversationInfo
from .event import Event
from .seg import Seg, SegBuilder
from .user_info import UserInfo


class EventBuilder:
    """Event 构建器，提供快速创建各种事件的方法.

    Methods:
        generate_event_id() -> str: 生成唯一的事件ID.
        get_current_timestamp() -> float: 获取当前Unix毫秒时间戳.
        create_message_event(
            event_type: str,
            bot_id: str,
            message_id: str,
            content_segs: list[Seg],
            user_info: UserInfo | None = None,
            conversation_info: ConversationInfo | None = None,
            **kwargs: Any,
        ) -> Event: 创建消息事件.
        create_action_response_event(
            response_type: str,
            original_event: Event,
            status_code: int | None = None,
            message: str | None = None,
            data: dict[str, Any] | None = None,
        ) -> Event: 创建动作响应事件.
    """

    @staticmethod
    def generate_event_id() -> str:
        """生成唯一的事件ID.

        Returns:
            str: 生成的唯一事件ID，格式为 UUID4 字符串.
        """
        return str(uuid.uuid4())

    @staticmethod
    def get_current_timestamp() -> float:
        """获取当前Unix毫秒时间戳.

        Returns:
            float: 当前时间的 Unix 毫秒时间戳.
        """
        return time.time() * 1000

    @staticmethod
    def create_message_event(
        event_type: str,
        bot_id: str,
        message_id: str,
        content_segs: list[Seg],
        user_info: UserInfo | None = None,
        conversation_info: ConversationInfo | None = None,
        **kwargs: Any,
    ) -> Event:
        """创建消息事件。event_type 应为 "message.{platform}.{...}" 格式.

        Args:
            event_type (str): 事件类型，格式为 "message.{platform}.{...}".
            bot_id (str): 机器人在该平台上的 ID.
            message_id (str): 消息的唯一标识符.
            content_segs (list[Seg]): 消息内容的 Seg 列表.
            user_info (UserInfo | None): 与事件相关的用户信息.
            conversation_info (ConversationInfo | None): 事件发生的会话信息.
            **kwargs: 其他额外参数，将添加到消息元数据中.

        Returns:
            Event: 创建的消息事件对象.
        """
        metadata_seg = SegBuilder.message_metadata(message_id, **kwargs)
        all_content = [metadata_seg, *content_segs]

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
        status_code: int | None = None,
        message: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> Event:
        """创建动作响应事件.

        Args:
            response_type (str): 响应类型，例如 "success", "error" 等.
            original_event (Event): 原始动作事件，用于提取平台和其他信息.
            status_code (int | None): 响应状态码，默认为 None.
            message (str | None): 响应消息，默认为 None.
            data (dict[str, Any] | None): 响应数据，默认为 None.

        Returns:
            Event: 创建的动作响应事件对象.
        """
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
