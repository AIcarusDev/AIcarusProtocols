"""AIcarus-Message-Protocol v1.6.0 - UserInfo 对象定义.

用于描述用户信息的数据结构.
"""

from dataclasses import dataclass, field
from dataclasses import fields as dataclass_fields
from typing import Any, Optional


@dataclass
class UserInfo:
    """2.2. UserInfo 对象.

    用于描述用户信息.

    Attributes:
        user_id (str | None): 用户唯一ID.
        user_nickname (str | None): 用户昵称.
        user_cardname (str | None): 用户在群组中的名片/备注.
        user_titlename (str | None): 用户在群组中的头衔.
        permission_level (str | None): 用户在当前上下文（如群组）中的权限级别.
        role (str | None): 用户在群组中的角色.
        level (str | None): 用户等级字符串.
        sex (str | None): 用户性别.
        age (int | None): 用户年龄.
        area (str | None): 用户地区.
        additional_data (dict[str, Any] | None): 用于存储平台特有的、
            协议未明确定义的其他用户相关信息.

    Methods:
        to_dict() -> dict[str, Any]: 将 UserInfo 实例转换为字典，排除 None 值.
        from_dict(data: dict[str, Any] | None) -> Optional[UserInfo]: 从字典创建 UserInfo 实例.
    """

    user_id: str | None = None  # 用户唯一ID
    user_nickname: str | None = None  # 用户昵称
    user_cardname: str | None = None  # 用户在群组中的名片/备注
    user_titlename: str | None = None  # 用户在群组中的头衔
    permission_level: str | None = None  # 用户在当前上下文（如群组）中的权限级别
    role: str | None = None  # 用户在群组中的角色
    level: str | None = None  # 用户等级字符串
    sex: str | None = None  # 用户性别
    age: int | None = None  # 用户年龄
    area: str | None = None  # 用户地区
    additional_data: dict[str, Any] | None = field(
        default_factory=dict
    )  # 用于存储平台特有的、协议未明确定义的其他用户相关信息

    def to_dict(self) -> dict[str, Any]:
        """将 UserInfo 实例转换为字典，排除 None 值.

        确保 additional_data 在非空时被包含.

        Returns:
            dict[str, Any]: 包含用户信息的字典表示.
        """
        result = {}
        for f in dataclass_fields(self):
            value = getattr(self, f.name)
            if value is not None:
                if f.name != "additional_data" or value:
                    result[f.name] = value
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> Optional["UserInfo"]:
        """从字典创建 UserInfo 实例.

        Args:
            data (dict[str, Any] | None): 包含用户信息的字典，可能为 None.

        Returns:
            Optional[UserInfo]: 创建的 UserInfo 实例或 None.
        """
        if data is None:
            return None
        # 移除 platform 的读取
        return cls(
            user_id=data.get("user_id"),
            user_nickname=data.get("user_nickname"),
            user_cardname=data.get("user_cardname"),
            user_titlename=data.get("user_titlename"),
            permission_level=data.get("permission_level"),
            role=data.get("role"),
            level=data.get("level"),
            sex=data.get("sex"),
            age=data.get("age"),
            area=data.get("area"),
            additional_data=data.get("additional_data", {}),
        )
