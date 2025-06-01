"""
AIcarus-Message-Protocol v1.2.0 Python 定义。
本脚本根据 AIcarus Message Protocol version 1.2.0 定义了数据结构。
所有注释和面向用户的输出信息均使用中文。
"""

from dataclasses import dataclass, field, asdict, fields as dataclass_fields
from typing import List, Optional, Union, Dict, Any
import json # 用于示例输出

# ---------------------------------------------------------------------------
# 2. 核心数据结构 (依据 AIcarus-Message-Protocol v1.2.0)
# ---------------------------------------------------------------------------

@dataclass
class GroupInfo:
    """
    2.5. GroupInfo 对象
    用于描述群组信息。
    """
    platform: Optional[str] = None # 平台标识，如 "qq"
    group_id: Optional[str] = None # 群组唯一ID
    group_name: Optional[str] = None # 群组名称

    def to_dict(self) -> Dict[str, Any]:
        """将 GroupInfo 实例转换为字典，排除 None 值。"""
        return {k: v for k, v in asdict(self).items() if v is not None}

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["GroupInfo"]:
        """从字典创建 GroupInfo 实例。"""
        if data is None:
            return None
        # 确保所有预期的键都从data中获取，如果键不存在，则默认为None
        return cls(
            platform=data.get("platform"),
            group_id=data.get("group_id"),
            group_name=data.get("group_name"),
        )

@dataclass
class UserInfo:
    """
    2.4. UserInfo 对象
    用于描述用户信息。
    """
    platform: Optional[str] = None # 平台标识
    user_id: Optional[str] = None # 用户唯一ID
    user_nickname: Optional[str] = None # 用户昵称
    user_cardname: Optional[str] = None # 用户在群组中的名片/备注
    user_titlename: Optional[str] = None # 用户在群组中的头衔
    permission_level: Optional[str] = None # 用户在当前上下文（如群组）中的权限级别
    role: Optional[str] = None # (可选, 映射 OneBot sender.role) 用户在群组中的角色
    level: Optional[str] = None # (可选, 映射 OneBot sender.level) 用户等级字符串
    sex: Optional[str] = None # (可选, 映射 OneBot sender.sex) 用户性别
    age: Optional[int] = None # (可选, 映射 OneBot sender.age) 用户年龄
    area: Optional[str] = None # (可选, 映射 OneBot sender.area) 用户地区
    additional_data: Optional[Dict[str, Any]] = field(default_factory=dict) # 用于存储平台特有的、协议未明确定义的其他用户相关信息

    def to_dict(self) -> Dict[str, Any]:
        """将 UserInfo 实例转换为字典，排除 None 值。
           确保 additional_data 在非空时被包含。
        """
        res = {}
        for f in dataclass_fields(self):
            value = getattr(self, f.name)
            if value is not None:
                if f.name == "additional_data" and not value: # 不包含空的 additional_data
                    continue
                res[f.name] = value
        return res


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
            additional_data=data.get("additional_data", {}), # 确保默认为空字典
        )

@dataclass
class Seg:
    """
    2.3. Seg 对象 (通用信息单元)
    AIcarus-Message-Protocol 定义的 `Seg` 对象是构成消息内容、通知详情、请求参数和动作指令的基本单元。
    """
    type: str # 片段类型
    data: Union[str, List["Seg"], Dict[str, Any]] # 片段数据

    def to_dict(self) -> Dict[str, Any]:
        """将 Seg 实例转换为字典。"""
        result_data: Any
        if self.type == "seglist" and isinstance(self.data, list):
            # 确保列表中的所有元素都是 Seg 对象，并调用它们的 to_dict 方法
            result_data = [item.to_dict() if isinstance(item, Seg) else item for item in self.data]
        elif isinstance(self.data, (str, dict)): # 允许 data 是字符串或字典
            result_data = self.data
        else:
            # 对于其他未预期的 data 类型，进行回退处理或抛出错误
            # print(f"警告: Seg 类型 '{self.type}' 的 data 字段类型未预期: {type(self.data)}")
            result_data = str(self.data) # 简单转换为字符串

        return {"type": self.type, "data": result_data}

    @classmethod
    def from_dict(cls, data_dict: Dict[str, Any]) -> "Seg":
        """从字典创建 Seg 实例。"""
        seg_type = data_dict.get("type", "unknown") # 如果类型缺失，默认为 'unknown'
        raw_seg_data = data_dict.get("data")
        processed_seg_data: Union[str, List["Seg"], Dict[str, Any]]

        if seg_type == "seglist":
            if isinstance(raw_seg_data, list):
                # 确保列表中的每个元素都是字典，才尝试用 Seg.from_dict 转换
                processed_seg_data = [Seg.from_dict(item) for item in raw_seg_data if isinstance(item, dict)]
            else:
                # print(f"警告: Seg 类型 'seglist' 期望列表类型数据，实际得到 {type(raw_seg_data)}。默认为空列表。")
                processed_seg_data = []
        elif seg_type == "text": # 文本类型的 data 应该是字符串
            if isinstance(raw_seg_data, str):
                processed_seg_data = raw_seg_data
            else:
                # print(f"警告: Seg 类型 'text' 期望字符串类型数据，实际得到 {type(raw_seg_data)}。默认为空字符串。")
                processed_seg_data = str(raw_seg_data) if raw_seg_data is not None else ""
        else:  # 对于其他所有类型 (如 image, face, notification:*, request:*, action:*)，data 通常是字典
            if isinstance(raw_seg_data, dict):
                processed_seg_data = raw_seg_data
            elif raw_seg_data is None: # 某些 Seg 的 data 字段可能是可选的，用空字典表示
                 processed_seg_data = {}
            else: # 如果不是字典也不是None，则可能存在问题
                # print(f"警告: Seg 类型 '{seg_type}' 期望字典类型数据，实际得到 {type(raw_seg_data)}。默认为空字典。")
                processed_seg_data = {} # 或者根据具体情况决定如何处理
        
        return cls(type=seg_type, data=processed_seg_data)


@dataclass
class BaseMessageInfo:
    """
    2.2. BaseMessageInfo 对象 (用于 MessageBase.message_info)
    此对象包含了所有交互类型共享的元数据。
    """
    platform: str # 平台标识
    bot_id: str # 机器人自身ID
    interaction_purpose: str # 交互意图
    time: float # 事件发生的Unix毫秒时间戳

    message_id: Optional[str] = None # 平台消息ID或事件ID
    group_info: Optional[GroupInfo] = None # 群组信息
    user_info: Optional[UserInfo] = None # 用户信息
    additional_config: Optional[Dict[str, Any]] = field(default_factory=dict) # 附加配置

    # 特定于 interaction_purpose = "user_message" 的额外字段
    message_type: Optional[str] = None # 消息类型 ("private", "group")
    sub_type: Optional[str] = None # 消息子类型
    font: Optional[str] = None # 字体信息
    anonymity_info: Optional[Dict[str, Any]] = None # 匿名消息信息, 例如: {"id": Optional[int], "name": str, "flag": str}

    def to_dict(self) -> Dict[str, Any]:
        """将 BaseMessageInfo 实例转换为字典，排除 None 值。"""
        result = {}
        for f in dataclass_fields(self):
            value = getattr(self, f.name)
            if value is not None:
                # 不包含空的 additional_config 或 anonymity_info
                if f.name == "additional_config" and not value:
                    continue
                if f.name == "anonymity_info" and not value:
                    continue
                
                if isinstance(value, (GroupInfo, UserInfo)): # 嵌套对象也转换为字典
                    result[f.name] = value.to_dict()
                else:
                    result[f.name] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseMessageInfo":
        """从字典创建 BaseMessageInfo 实例。"""
        # 确保 platform, bot_id, interaction_purpose, time 具有默认值或从 data 中获取
        platform = data.get("platform", "unknown_platform")
        bot_id = data.get("bot_id", "unknown_bot_id")
        interaction_purpose = data.get("interaction_purpose", "unknown_purpose")
        time = data.get("time", 0.0)

        group_info_data = data.get("group_info")
        user_info_data = data.get("user_info")
        
        return cls(
            platform=platform,
            bot_id=bot_id,
            interaction_purpose=interaction_purpose,
            time=time,
            message_id=data.get("message_id"),
            group_info=GroupInfo.from_dict(group_info_data) if group_info_data else None,
            user_info=UserInfo.from_dict(user_info_data) if user_info_data else None,
            additional_config=data.get("additional_config", {}), # 确保默认为空字典
            message_type=data.get("message_type"),
            sub_type=data.get("sub_type"),
            font=data.get("font"),
            anonymity_info=data.get("anonymity_info"),
        )

@dataclass
class MessageBase:
    """
    2.1. MessageBase 对象
    所有交互的顶层载体。
    """
    message_info: BaseMessageInfo # 消息/事件元信息
    message_segment: Seg  # 消息/事件内容，通常此 Seg 类型为 "seglist"
    raw_message: Optional[str] = None # 原始消息/事件数据 (例如JSON字符串)

    def to_dict(self) -> Dict[str, Any]:
        """将 MessageBase 实例转换为字典。"""
        res = {
            "message_info": self.message_info.to_dict(),
            "message_segment": self.message_segment.to_dict(),
        }
        if self.raw_message is not None:
            res["raw_message"] = self.raw_message
        return res

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MessageBase":
        """从字典创建 MessageBase 实例。"""
        # 确保 message_info 和 message_segment 即使在 data 中缺失，也能被正确初始化
        message_info_data = data.get("message_info")
        if message_info_data is None:
            # print("警告: MessageBase.from_dict 收到空的 'message_info'，将使用默认值初始化 BaseMessageInfo。")
            # 提供一个最小化的默认 BaseMessageInfo 字典结构
            message_info_data = {
                "platform": "default_platform",
                "bot_id": "default_bot_id",
                "interaction_purpose": "unknown",
                "time": 0.0,
                "additional_config": {"protocol_version": "1.2.0"} # 假设默认协议版本
            }
        
        message_segment_data = data.get("message_segment")
        if message_segment_data is None:
            # print("警告: MessageBase.from_dict 收到空的 'message_segment'，将使用默认的空 seglist。")
            message_segment_data = {"type": "seglist", "data": []}

        return cls(
            message_info=BaseMessageInfo.from_dict(message_info_data),
            message_segment=Seg.from_dict(message_segment_data),
            raw_message=data.get("raw_message"),
        )

# ---------------------------------------------------------------------------
# (概念性路由和处理器部分已移除，将由 core 和 adapter 模块分别实现)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 示例用法 (保持用于独立测试 base.py)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 示例 1: 创建用户消息对象并转换为字典
    print("--- 示例 1: 创建用户消息 ---")
    user_msg_info = BaseMessageInfo(
        platform="qq",
        bot_id="10001",
        message_id="platform_msg_789",
        time=1678886400123.0,
        group_info=GroupInfo(platform="qq", group_id="group123", group_name="测试群"),
        user_info=UserInfo(
            platform="qq", user_id="user_sender_456", user_nickname="李四",
            user_cardname="群里的李四", permission_level="member", role="member",
            additional_data={"constellation": "aries", "custom_badge": "vip"} # 星座: 白羊座, 自定义徽章: vip
        ),
        interaction_purpose="user_message",
        message_type="group",
        sub_type="normal",
        additional_config={"protocol_version": "1.2.0"}
    )
    msg_segments_list = [ # 明确这是一个 Seg 对象的列表
        Seg(type="text", data="你好 "),
        Seg(type="at", data={"user_id": "user_zhangsan_001", "display_name": "@张三"}),
        Seg(type="image", data={"url": "http://example.com/image.jpg", "file_id": "qq_image_abc"})
    ]
    user_message_obj = MessageBase(
        message_info=user_msg_info,
        message_segment=Seg(type="seglist", data=msg_segments_list), # message_segment 是一个类型为 seglist 的 Seg
        raw_message="你好 @张三 [CQ:image,file=...]"
    )
    user_message_dict = user_message_obj.to_dict()
    print("用户消息 (字典格式):")
    print(json.dumps(user_message_dict, indent=2, ensure_ascii=False))

    # 测试从字典转换回对象
    reconstructed_user_message = MessageBase.from_dict(user_message_dict)
    print("\n从字典重构的用户消息对象:")
    print(reconstructed_user_message)
    assert reconstructed_user_message.message_info.user_info.additional_data == {"constellation": "aries", "custom_badge": "vip"}
    assert reconstructed_user_message.message_segment.type == "seglist"
    if isinstance(reconstructed_user_message.message_segment.data, list) and \
       len(reconstructed_user_message.message_segment.data) > 0 and \
       isinstance(reconstructed_user_message.message_segment.data[0], Seg):
        assert reconstructed_user_message.message_segment.data[0].type == "text"
    else:
        print("警告: 重构后的 message_segment.data 结构不符合预期。")


    # 示例 3: 平台通知 (群文件上传) - 来自字典
    print("\n--- 示例 3: 平台通知 (文件上传) ---")
    file_upload_event_dict = {
      "message_info": {
        "platform": "qq",
        "bot_id": "10001",
        "message_id": "event_id_upload_xyz",
        "time": 1678886400234.0,
        "group_info": {
          "platform": "qq",
          "group_id": "group123",
          "group_name": "测试群"
        },
        "user_info": {
          "platform": "qq",
          "user_id": "uploader_789",
          "user_nickname": "文件上传君",
          "permission_level": "member"
        },
        "interaction_purpose": "platform_notification",
        "additional_config": {"protocol_version": "1.2.0"}
      },
      "message_segment": { # 通知也使用 seglist 包装其描述性 Seg
        "type": "seglist", 
        "data": [
          {
            "type": "notification:group_file_uploaded",
            "data": {
              "file_info": {
                "id": "file_abc_123",
                "name": "重要文档.docx",
                "size": 102400,
                "busid": 102
              },
              "uploader_user_info": { 
                "platform": "qq",
                "user_id": "uploader_789",
                "user_nickname": "文件上传君"
              }
            }
          }
        ]
      }
    }
    reconstructed_notification = MessageBase.from_dict(file_upload_event_dict)
    print("文件上传通知 (重构对象):")
    print(reconstructed_notification)
    if isinstance(reconstructed_notification.message_segment.data, list) and \
       len(reconstructed_notification.message_segment.data) > 0 and \
       isinstance(reconstructed_notification.message_segment.data[0], Seg) and \
       isinstance(reconstructed_notification.message_segment.data[0].data, dict):
        assert reconstructed_notification.message_segment.data[0].type == "notification:group_file_uploaded"
        assert reconstructed_notification.message_segment.data[0].data['file_info']['name'] == "重要文档.docx"
    else:
        print("警告: 重构后的 notification.message_segment.data 结构不符合预期。")

    print("\n--- 测试 UserInfo (最少数据) ---")
    min_user_info_dict = {"user_id": "test_user", "additional_data": {"test":1}}
    min_user_info = UserInfo.from_dict(min_user_info_dict)
    if min_user_info:
        print(json.dumps(min_user_info.to_dict(), indent=2, ensure_ascii=False))
        assert min_user_info.to_dict()["additional_data"]["test"] == 1

    print("\n--- 测试空的 additional_data 和 additional_config 不应出现在 to_dict 输出中 ---")
    test_user_info_empty_add = UserInfo(user_id="test_empty", additional_data={})
    print("UserInfo with empty additional_data:", json.dumps(test_user_info_empty_add.to_dict(), indent=2, ensure_ascii=False))
    assert "additional_data" not in test_user_info_empty_add.to_dict()
    
    test_msg_info_empty_add_conf = BaseMessageInfo(
        platform="test", bot_id="bot1", interaction_purpose="user_message", time=123.0,
        additional_config={}
    )
    print("BaseMessageInfo with empty additional_config:", json.dumps(test_msg_info_empty_add_conf.to_dict(), indent=2, ensure_ascii=False))
    assert "additional_config" not in test_msg_info_empty_add_conf.to_dict()

    print("\n--- 测试 from_dict 对缺失 message_info 和 message_segment 的处理 ---")
    minimal_dict = {}
    reconstructed_minimal = MessageBase.from_dict(minimal_dict)
    print("从空字典重构的 MessageBase:")
    print(json.dumps(reconstructed_minimal.to_dict(), indent=2, ensure_ascii=False))
    assert reconstructed_minimal.message_info is not None
    assert reconstructed_minimal.message_segment.type == "seglist"
    assert reconstructed_minimal.message_segment.data == []

    dict_missing_segment = {"message_info": user_msg_info.to_dict()}
    reconstructed_missing_segment = MessageBase.from_dict(dict_missing_segment)
    print("\n从缺失 message_segment 的字典重构的 MessageBase:")
    print(json.dumps(reconstructed_missing_segment.to_dict(), indent=2, ensure_ascii=False))
    assert reconstructed_missing_segment.message_segment.type == "seglist"
    assert reconstructed_missing_segment.message_segment.data == []

