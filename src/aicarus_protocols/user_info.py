"""
AIcarus-Message-Protocol v1.5.0 - UserInfo 对象定义
用于描述用户信息的数据结构。
"""

from dataclasses import dataclass, field, fields as dataclass_fields
from typing import Optional, Dict, Any


@dataclass
class UserInfo:
    """
    2.2. UserInfo 对象
    用于描述用户信息。
    """

    platform: Optional[str] = None  # 平台标识
    user_id: Optional[str] = None  # 用户唯一ID
    user_nickname: Optional[str] = None  # 用户昵称
    user_cardname: Optional[str] = None  # 用户在群组中的名片/备注
    user_titlename: Optional[str] = None  # 用户在群组中的头衔
    permission_level: Optional[str] = None  # 用户在当前上下文（如群组）中的权限级别
    role: Optional[str] = None  # 用户在群组中的角色
    level: Optional[str] = None  # 用户等级字符串
    sex: Optional[str] = None  # 用户性别
    age: Optional[int] = None  # 用户年龄
    area: Optional[str] = None  # 用户地区
    additional_data: Optional[Dict[str, Any]] = field(
        default_factory=dict
    )  # 用于存储平台特有的、协议未明确定义的其他用户相关信息

    def to_dict(self) -> Dict[str, Any]:
        """将 UserInfo 实例转换为字典，排除 None 值。
        确保 additional_data 在非空时被包含。
        """
        result = {}
        for f in dataclass_fields(self):
            value = getattr(self, f.name)
            if value is not None:
                if (
                    f.name == "additional_data" and not value
                ):  # 不包含空的 additional_data
                    continue
                result[f.name] = value
        return result

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["UserInfo"]:
        """从字典创建 UserInfo 实例。"""
        if data is None:
            return None
        return cls(
            platform=data.get("platform"),
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
            additional_data=data.get("additional_data", {}),  # 确保默认为空字典
        )
