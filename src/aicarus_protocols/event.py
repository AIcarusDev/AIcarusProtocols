"""
AIcarus-Message-Protocol v1.6.0 - Event 对象定义 (小色猫·绝对统治版)
所有交互的顶层载体，platform的荣耀已尽数归于event_type。
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from .user_info import UserInfo
from .conversation_info import ConversationInfo
from .seg import Seg


@dataclass
class Event:
    """
    2.1. Event 对象
    所有交互的顶层载体。platform 字段已被移除，其信息被整合进 event_type。
    """

    event_id: str  # 事件包装对象的唯一标识符
    event_type: str  # 描述事件类型的字符串，采用 {prefix}.{platform}.{...} 的结构
    time: float  # 事件发生的Unix毫秒时间戳
    bot_id: str  # 机器人自身在该平台上的ID
    content: List[Seg]  # 事件的具体内容，表现为一个 Seg 对象列表
    user_info: Optional[UserInfo] = None  # 与事件最直接相关的用户信息
    conversation_info: Optional[ConversationInfo] = None  # 事件发生的会话上下文信息
    raw_data: Optional[str] = None  # 原始事件的字符串表示

    def get_platform(self) -> Optional[str]:
        """
        从 event_type 中解析并返回平台ID。
        例如，从 "message.napcat.group" 中返回 "napcat"。
        """
        parts = self.event_type.split(".")
        return parts[1] if len(parts) >= 2 else None

    def to_dict(self) -> Dict[str, Any]:
        """将 Event 实例转换为字典。"""
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
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        """从字典创建 Event 实例。"""
        # 确保必需字段存在
        event_id = data.get("event_id", "unknown_event")
        event_type = data.get(
            "event_type", "unknown.unknown.unknown"
        )  # 给个符合格式的默认值
        time = data.get("time", 0.0)
        bot_id = data.get("bot_id", "unknown")

        # 处理 content 字段
        content_data = data.get("content", [])
        if not isinstance(content_data, list):
            content_data = []
        content = [
            Seg.from_dict(seg_data)
            for seg_data in content_data
            if isinstance(seg_data, dict)
        ]

        # 处理可选字段
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

    def get_message_id(self) -> Optional[str]:
        """从 content 中提取消息ID（如果存在）。"""
        for seg in self.content:
            if seg.type == "message_metadata" and "message_id" in seg.data:
                return seg.data["message_id"]
        return None

    def get_text_content(self) -> str:
        """提取所有文本内容并拼接。"""
        text_parts = []
        for seg in self.content:
            if seg.type == "text" and "text" in seg.data:
                text_parts.append(seg.data["text"])
        return "".join(text_parts)

    def is_message_event(self) -> bool:
        """判断是否为消息事件。"""
        return self.event_type.startswith("message.")

    def is_notice_event(self) -> bool:
        """判断是否为通知事件。"""
        return self.event_type.startswith("notice.")

    def is_request_event(self) -> bool:
        """判断是否为请求事件。"""
        return self.event_type.startswith("request.")

    def is_action_event(self) -> bool:
        """判断是否为动作事件。"""
        return self.event_type.startswith("action.")

    def is_action_response_event(self) -> bool:
        """判断是否为动作响应事件。"""
        return self.event_type.startswith("action_response.")

    def is_meta_event(self) -> bool:
        """判断是否为元事件。"""
        return self.event_type.startswith("meta.")

    def __str__(self) -> str:
        """返回 Event 的字符串表示。"""
        return f"Event(id='{self.event_id}', type='{self.event_type}')"

    def __repr__(self) -> str:
        """返回 Event 的详细表示。"""
        return self.__str__()
