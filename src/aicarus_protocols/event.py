"""AIcarus-Message-Protocol v1.6.0 - Event 对象定义.

所有交互的顶层载体，platform 的信息已整合到 event_type 中.
"""

from dataclasses import dataclass
from typing import Any

from .conversation_info import ConversationInfo
from .seg import Seg
from .user_info import UserInfo


@dataclass
class Event:
    """2.1. Event 对象.

    所有交互的顶层载体。platform 字段已被移除，其信息被整合进 event_type.

    Attributes:
        event_id (str): 事件包装对象的唯一标识符.
        event_type (str): 描述事件类型的字符串，采用 {prefix}.{platform}.{...} 的结构.
        time (float): 事件发生的 Unix 毫秒时间戳.
        bot_id (str): 机器人自身在该平台上的 ID.
        content (list[Seg]): 事件的具体内容，表现为一个 Seg 对象列表.
        user_info (UserInfo | None): 与事件最直接相关的用户信息.
        conversation_info (ConversationInfo | None): 事件发生的会话上下文信息.
        raw_data (str | None): 原始事件的字符串表示.

    Methods:
        get_platform() -> str | None: 从 event_type 中解析并返回平台 ID.
        to_dict() -> dict[str, Any]: 将 Event 实例转换为字典.
        from_dict(data: dict[str, Any]) -> Event: 从字典创建 Event 实例.
        get_message_id() -> str | None: 从 content 中提取消息 ID（如果存在）.
        get_text_content() -> str: 提取所有文本内容并拼接.
        is_message_event() -> bool: 判断是否为消息事件.
        is_notice_event() -> bool: 判断是否为通知事件.
        is_request_event() -> bool: 判断是否为请求事件.
        is_action_event() -> bool: 判断是否为动作事件.
        is_action_response_event() -> bool: 判断是否为动作响应事件.
        is_meta_event() -> bool: 判断是否为元事件.
        __str__() -> str: 返回 Event 的字符串表示.
        __repr__() -> str: 返回 Event 的详细表示.
    """

    event_id: str  # 事件包装对象的唯一标识符。
    event_type: str  # 描述事件类型的字符串，采用 {prefix}.{platform}.{...} 的结构。
    time: float  # 事件发生的 Unix 毫秒时间戳。
    bot_id: str  # 机器人自身在该平台上的 ID。
    content: list[Seg]  # 事件的具体内容，表现为一个 Seg 对象列表。
    user_info: UserInfo | None = None  # 与事件最直接相关的用户信息。
    conversation_info: ConversationInfo | None = None  # 事件发生的会话上下文信息。
    raw_data: str | None = None  # 原始事件的字符串表示。

    def get_platform(self) -> str | None:
        """从 event_type 中解析并返回平台 ID.

        例如，从 "message.napcat.group" 中返回 "napcat".

        Returns:
            str | None: 平台 ID，如果 event_type 格式不正确则返回 None.
        """
        parts = self.event_type.split(".")
        return parts[1] if len(parts) >= 2 else None

    def to_dict(self) -> dict[str, Any]:
        """将 Event 实例转换为字典.

        Returns:
            dict[str, Any]: 包含事件信息的字典表示.
        """
        result = {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "time": self.time,
            "bot_id": self.bot_id,
            "content": [seg.to_dict() for seg in self.content],
        }

        if self.user_info is not None:
            result["user_info"] = self.user_info.to_dict()

        if self.conversation_info is not None:
            result["conversation_info"] = self.conversation_info.to_dict()

        if self.raw_data is not None:
            result["raw_data"] = self.raw_data

        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Event":
        """从字典创建 Event 实例.

        Args:
            data (dict[str, Any]): 包含事件信息的字典.

        Returns:
            Event: 创建的 Event 实例.
        """
        # 确保必需字段存在。
        event_id = data.get("event_id", "unknown_event")
        event_type = data.get("event_type", "unknown.unknown.unknown")  # 给个符合格式的默认值。
        time = data.get("time", 0.0)
        bot_id = data.get("bot_id", "unknown")

        # 处理 content 字段。
        content_data = data.get("content", [])
        if not isinstance(content_data, list):
            content_data = []
        content = [
            Seg.from_dict(seg_data) for seg_data in content_data if isinstance(seg_data, dict)
        ]

        # 处理可选字段。
        user_info_data = data.get("user_info")
        conversation_info_data = data.get("conversation_info")

        return cls(
            event_id=event_id,
            event_type=event_type,
            time=time,
            bot_id=bot_id,
            content=content,
            user_info=UserInfo.from_dict(user_info_data) if user_info_data else None,
            conversation_info=ConversationInfo.from_dict(conversation_info_data)
            if conversation_info_data
            else None,
            raw_data=data.get("raw_data"),
        )

    def get_message_id(self) -> str | None:
        """从 content 中提取消息 ID（如果存在）.

        Returns:
            str | None: 如果 content 中包含消息 ID，则返回该 ID，否则返回 None.
        """
        for seg in self.content:
            if seg.type == "message_metadata" and "message_id" in seg.data:
                return seg.data["message_id"]
        return None

    def get_text_content(self) -> str:
        """提取所有文本内容并拼接.

        Returns:
            str: 提取的所有文本内容，按顺序连接成一个字符串.
        """
        text_parts = []
        for seg in self.content:
            if seg.type == "text" and "text" in seg.data:
                text_parts.append(seg.data["text"])
        return "".join(text_parts)

    def is_message_event(self) -> bool:
        """判断是否为消息事件.

        Returns:
            bool: 如果 event_type 以 "message." 开头，则返回 True，否则返回 False.
        """
        return self.event_type.startswith("message.")

    def is_notice_event(self) -> bool:
        """判断是否为通知事件.

        Returns:
            bool: 如果 event_type 以 "notice." 开头，则返回 True，否则返回 False.
        """
        return self.event_type.startswith("notice.")

    def is_request_event(self) -> bool:
        """判断是否为请求事件.

        Returns:
            bool: 如果 event_type 以 "request." 开头，则返回 True，否则返回 False.
        """
        return self.event_type.startswith("request.")

    def is_action_event(self) -> bool:
        """判断是否为动作事件.

        Returns:
            bool: 如果 event_type 以 "action." 开头，则返回 True，否则返回 False.
        """
        return self.event_type.startswith("action.")

    def is_action_response_event(self) -> bool:
        """判断是否为动作响应事件.

        Returns:
            bool: 如果 event_type 以 "action_response." 开头，则返回 True，否则返回 False.
        """
        return self.event_type.startswith("action_response.")

    def is_meta_event(self) -> bool:
        """判断是否为元事件.

        Returns:
            bool: 如果 event_type 以 "meta." 开头，则返回 True，否则返回 False.
        """
        return self.event_type.startswith("meta.")

    def __str__(self) -> str:
        """返回 Event 的字符串表示.

        Returns:
            str: Event 的字符串表示，包含 event_id 和 event_type.
        """
        return f"Event(id='{self.event_id}', type='{self.event_type}')"

    def __repr__(self) -> str:
        """返回 Event 的详细表示.

        Returns:
            str: 包含所有字段的详细字符串表示.
        """
        return self.__str__()
