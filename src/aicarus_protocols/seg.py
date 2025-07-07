"""
AIcarus-Message-Protocol v1.5.1 - Seg 对象定义
通用信息单元，是构成所有类型事件的原子构建块。
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class Seg:
    """
    2.4. Seg 对象 (通用信息单元)
    AIcarus-Message-Protocol 定义的通用信息单元，是构成所有类型事件的基本单元。
    """

    type: str  # Seg 类型，例如 "text", "image" 等
    data: Dict[str, Any]  # Seg 数据，包含 Seg 的具体内容

    def to_dict(self) -> Dict[str, Any]:
        """
        将 Seg 实例转换为字典。
        Returns:
            Dict[str, Any]: 包含 Seg 信息的字典。
        """
        return {"type": self.type, "data": self.data}

    @classmethod
    def from_dict(cls, data_dict: Dict[str, Any]) -> "Seg":
        """
        从字典创建 Seg 实例。
        Args:
            data_dict (Dict[str, Any]): 包含 Seg 信息的字典。
        Returns:
            Seg: 从字典创建的 Seg 实例。
        """
        seg_type = data_dict.get("type", "unknown")
        seg_data = data_dict.get("data", {})

        if not isinstance(seg_data, dict):
            seg_data = {"value": seg_data} if seg_data is not None else {}

        return cls(type=seg_type, data=seg_type, data=seg_data)

    def __str__(self) -> str:
        """
        返回 Seg 的字符串表示。
        Returns:
            str: Seg 的字符串表示。
        """
        return f"Seg(type='{self.type}', data={self.data})"

    def __repr__(self) -> str:
        """
        返回 Seg 的详细表示。
        Returns:
            str: Seg 的详细表示。
        """
        return self.__str__()


class SegBuilder:
    """
    协议标准 Seg 构建器。
    定义了最推荐、最通用的构建 Seg 的方式，能确保核心逻辑获得最佳体验。
    Adapter 开发者可以参考这些来构建通用的 Seg，也可以根据自身需求进行扩展。
    """

    @staticmethod
    def text(text: str) -> Seg:
        """
        创建文本 Seg。
        Args:
            text (str): 文本内容。
        """
        return Seg(type="text", data={"text": text})

    @staticmethod
    def at(user_id: str, display_name: str = "") -> Seg:
        """
        创建 @ 用户 Seg。
        Args:
            user_id (str): 用户 ID。
            display_name (str): 显示名称 (可选)。
        """
        data = {"user_id": user_id}
        if display_name:
            data["display_name"] = display_name
        return Seg(type="at", data=data)

    @staticmethod
    def image(
        url: Optional[str] = None,
        file_id: Optional[str] = None,
        base64: Optional[str] = None,
        summary: Optional[str] = None,
        **kwargs,
    ) -> Seg:
        """
        创建图片 Seg。

        参数:
            url (Optional[str]): 图片 URL。
            file_id (Optional[str]): 文件 ID。
            base64 (Optional[str]): Base64 编码的图片数据。
            summary (Optional[str]): 图片摘要。
            kwargs: 额外参数。
        """
        data = {}
        if url is not None:
            data["url"] = url
        if file_id is not None:
            data["file_id"] = file_id
        if base64 is not None:
            data["base64"] = base64
        if summary is not None:
            data["summary"] = summary

        # 允许传入额外的参数
        data.update(kwargs)
        return Seg(type="image", data=data)

    @staticmethod
    def reply(message_id: str) -> Seg:
        """
        创建回复 Seg。
        Args:
            message_id (str): 消息 ID。
        """
        return Seg(type="reply", data={"message_id": message_id})

    @staticmethod
    def face(face_id: str) -> Seg:
        """
        创建表情 Seg。
        Args:
            face_id (str): 表情 ID。
        """
        return Seg(type="face", data={"id": face_id})

    @staticmethod
    def message_metadata(message_id: str, **kwargs) -> Seg:
        """
        创建消息元数据 Seg。

        参数:
            message_id (str): 消息 ID。
            kwargs: 额外参数。
        """
        data = {"message_id": message_id}
        data.update(kwargs)
        return Seg(type="message_metadata", data=data)

    @staticmethod
    def notice(notice_type: str, **kwargs) -> Seg:
        """
        创建通知类型 Seg。

        参数:
            notice_type (str): 通知类型。
            kwargs: 额外参数。
        """
        return Seg(type=f"notice.{notice_type}", data=kwargs)

    @staticmethod
    def request(request_type: str, **kwargs) -> Seg:
        """
        创建请求类型 Seg。

        参数:
            request_type (str): 请求类型。
            kwargs: 额外参数。
        """
        return Seg(type=f"request.{request_type}", data=kwargs)

    @staticmethod
    def action(action_type: str, **kwargs) -> Seg:
        """
        创建动作类型 Seg。

        参数:
            action_type (str): 动作类型。
            kwargs: 额外参数。
        """
        return Seg(type=f"action.{action_type}", data=kwargs)

    @staticmethod
    def action_response(response_type: str, **kwargs) -> Seg:
        """
        创建动作响应类型 Seg。

        参数:
            response_type (str): 响应类型。
            kwargs: 额外参数。
        """
        return Seg(type=f"action_response.{response_type}", data=kwargs)
