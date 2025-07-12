"""AIcarus-Message-Protocol v1.6.0 - ConversationInfo 对象定义.

用于描述会话信息的数据结构.
"""

from dataclasses import asdict, dataclass
from typing import Any, Optional


@dataclass
class ConversationInfo:
    """2.3. ConversationInfo 对象.

    用于描述会话信息.

    Attributes:
        conversation_id (str): 会话唯一ID（必需字段）.
        type (str): 会话类型（必需字段），如 "private", "group", "channel".
        name (str | None): 会话名称.
        parent_id (str | None): 父级会话ID（如频道下的子频道）.
        extra (dict[str, Any] | None): 额外信息，用于存储其他元数据.

    Methods:
        to_dict() -> dict[str, Any]: 将 ConversationInfo 实例转换为字典，排除 None 值.
        from_dict(data: dict[str, Any] | None) -> Optional[ConversationInfo]: 从字典
            创建 ConversationInfo 实例.
    """

    conversation_id: str  # 会话唯一ID（必需字段）
    type: str  # 会话类型（必需字段），如 "private", "group", "channel"
    name: str | None = None  # 会话名称
    parent_id: str | None = None  # 父级会话ID（如频道下的子频道）
    extra: dict[str, Any] | None = None  # 额外信息

    def to_dict(self) -> dict[str, Any]:
        """将 ConversationInfo 实例转换为字典，排除 None 值.

        Returns:
            dict[str, Any]: 包含会话信息的字典表示.
        """
        return {k: v for k, v in asdict(self).items() if v is not None}

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> Optional["ConversationInfo"]:
        """从字典创建 ConversationInfo 实例.

        Args:
            data (dict[str, Any] | None): 包含会话信息的字典，可能为 None.

        Returns:
            Optional[ConversationInfo]: 创建的 ConversationInfo 实例或 None.
        """
        if data is None:
            return None
        # 移除 platform 的读取
        return cls(
            conversation_id=data.get("conversation_id", "unknown_conversation"),
            type=data.get("type", "unknown"),
            name=data.get("name"),
            parent_id=data.get("parent_id"),
            extra=data.get("extra"),
        )
