"""
AIcarus-Message-Protocol v1.4.0 - Seg 对象定义
通用信息单元，是构成所有类型事件的原子构建块。
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Seg:
    """
    2.4. Seg 对象 (通用信息单元)
    AIcarus-Message-Protocol 定义的通用信息单元，是构成所有类型事件的基本单元。
    """

    type: str  # Seg 类型
    data: Dict[str, Any]  # Seg 数据

    def to_dict(self) -> Dict[str, Any]:
        """将 Seg 实例转换为字典。"""
        return {"type": self.type, "data": self.data}

    @classmethod
    def from_dict(cls, data_dict: Dict[str, Any]) -> "Seg":
        """从字典创建 Seg 实例。"""
        seg_type = data_dict.get("type", "unknown")
        seg_data = data_dict.get("data", {})

        # 确保 data 是字典类型
        if not isinstance(seg_data, dict):
            seg_data = {"value": seg_data} if seg_data is not None else {}

        return cls(type=seg_type, data=seg_data)

    def __str__(self) -> str:
        """返回 Seg 的字符串表示。"""
        return f"Seg(type='{self.type}', data={self.data})"

    def __repr__(self) -> str:
        """返回 Seg 的详细表示。"""
        return self.__str__()


# 常用的 Seg 创建辅助函数
class SegBuilder:
    """Seg 构建器，提供常用 Seg 类型的快速创建方法。"""

    @staticmethod
    def text(text: str) -> Seg:
        """创建文本 Seg。"""
        return Seg(type="text", data={"text": text})

    @staticmethod
    def at(user_id: str, display_name: str = "") -> Seg:
        """创建 @ 用户 Seg。"""
        return Seg(type="at", data={"user_id": user_id, "display_name": display_name})

    @staticmethod
    def image(url: str = "", file_id: str = "", **kwargs) -> Seg:
        """创建图片 Seg。"""
        data = {"url": url, "file_id": file_id}
        data.update(kwargs)
        return Seg(type="image", data=data)

    @staticmethod
    def reply(message_id: str) -> Seg:
        """创建回复 Seg。"""
        return Seg(type="reply", data={"message_id": message_id})

    @staticmethod
    def face(face_id: str) -> Seg:
        """创建表情 Seg。"""
        return Seg(type="face", data={"id": face_id})

    @staticmethod
    def message_metadata(message_id: str, **kwargs) -> Seg:
        """创建消息元数据 Seg。"""
        data = {"message_id": message_id}
        data.update(kwargs)
        return Seg(type="message_metadata", data=data)

    @staticmethod
    def notice(notice_type: str, **kwargs) -> Seg:
        """创建通知类型 Seg。"""
        return Seg(type=f"notice.{notice_type}", data=kwargs)

    @staticmethod
    def request(request_type: str, **kwargs) -> Seg:
        """创建请求类型 Seg。"""
        return Seg(type=f"request.{request_type}", data=kwargs)

    @staticmethod
    def action(action_type: str, **kwargs) -> Seg:
        """创建动作类型 Seg。"""
        return Seg(type=f"action.{action_type}", data=kwargs)

    @staticmethod
    def action_response(response_type: str, **kwargs) -> Seg:
        """创建动作响应类型 Seg。"""
        return Seg(type=f"action_response.{response_type}", data=kwargs)
