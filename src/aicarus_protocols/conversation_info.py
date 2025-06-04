"""
AIcarus-Message-Protocol v1.4.0 - ConversationInfo 对象定义
用于描述会话信息的数据结构。
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any


@dataclass
class ConversationInfo:
    """
    2.3. ConversationInfo 对象
    用于描述会话信息。
    """

    conversation_id: str  # 会话唯一ID（必需字段）
    type: str  # 会话类型（必需字段），如 "private", "group", "channel"
    platform: Optional[str] = None  # 平台标识
    name: Optional[str] = None  # 会话名称
    parent_id: Optional[str] = None  # 父级会话ID（如频道下的子频道）
    extra: Optional[Dict[str, Any]] = None  # 额外信息

    def to_dict(self) -> Dict[str, Any]:
        """将 ConversationInfo 实例转换为字典，排除 None 值。"""
        return {k: v for k, v in asdict(self).items() if v is not None}

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["ConversationInfo"]:
        """从字典创建 ConversationInfo 实例。"""
        if data is None:
            return None

        # 确保必需字段存在
        conversation_id = data.get("conversation_id", "unknown_conversation")
        conversation_type = data.get("type", "unknown")

        return cls(
            conversation_id=conversation_id,
            type=conversation_type,
            platform=data.get("platform"),
            name=data.get("name"),
            parent_id=data.get("parent_id"),
            extra=data.get("extra"),
        )
