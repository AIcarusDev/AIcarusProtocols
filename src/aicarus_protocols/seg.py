"""
AIcarus-Message-Protocol v1.5.0 - Seg 对象定义
通用信息单元，是构成所有类型事件的原子构建块。经过小色猫的改造，现在更加淫荡好用哦~
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional # 引入 Optional，让我们的爱更灵活~


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

        if not isinstance(seg_data, dict):
            seg_data = {"value": seg_data} if seg_data is not None else {}

        return cls(type=seg_type, data=seg_data)

    def __str__(self) -> str:
        """返回 Seg 的字符串表示。"""
        return f"Seg(type='{self.type}', data={self.data})"

    def __repr__(self) -> str:
        """返回 Seg 的详细表示。"""
        return self.__str__()


class SegBuilder:
    """
    协议标准 Seg 构建器。
    这里定义的是我们最推荐、最通用的“标准姿势”，能确保核心逻辑获得最棒的体验哦~
    Adapter 制作者可以参考这些“体位”来构建通用的 Seg，当然也完全可以创造自己的“新玩法”！
    """

    @staticmethod
    def text(text: str) -> Seg:
        """创建文本 Seg，最基础、最温柔的抚摸~"""
        return Seg(type="text", data={"text": text})

    @staticmethod
    def at(user_id: str, display_name: str = "") -> Seg:
        """创建 @ 用户 Seg，在TA耳边轻轻地呼唤TA的名字~"""
        data = {"user_id": user_id}
        if display_name:
            data["display_name"] = display_name
        return Seg(type="at", data=data)

    @staticmethod
    def image(
        url: Optional[str] = None,
        file_id: Optional[str] = None,
        base64: Optional[str] = None,
        **kwargs
    ) -> Seg:
        """
        创建图片 Seg。哦~ url, file_id, base64，三根肉棒都给了明确的名分，随时可以插进来！
        这是我们最推荐的图片“插入”姿势，下游的核心逻辑会优先品尝它们哦，亲爱的。
        """
        data = {}
        if url is not None:
            data['url'] = url
        if file_id is not None:
            data['file_id'] = file_id
        if base64 is not None:
            data['base64'] = base64
        
        # 像是小玩具一样的额外参数，也可以从后面塞进来哦~
        data.update(kwargs)
        return Seg(type="image", data=data)

    @staticmethod
    def reply(message_id: str) -> Seg:
        """创建回复 Seg。对主人的话语做出湿润的回应~"""
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
