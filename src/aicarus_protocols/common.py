"""
AIcarus-Message-Protocol v1.5.1 - 通用工具和类型定义
提供协议相关的常量、工具函数和构建器。
"""

from typing import Dict, Any, List, Optional
import uuid
import time
from .event import Event
from .seg import Seg, SegBuilder
from .user_info import UserInfo
from .conversation_info import ConversationInfo


# 协议版本
PROTOCOL_VERSION = "1.5.1"


def validate_event_type(event_type: str) -> bool:
    """验证事件类型格式是否正确。"""
    valid_prefixes = [
        "message.",
        "notice.",
        "request.",
        "action.",
        "action_response.",
        "meta.",
    ]
    return any(event_type.startswith(prefix) for prefix in valid_prefixes)


# 事件类型系统
class EventTypePrefix:
    """事件类型前缀常量，定义基础的事件分类。"""

    MESSAGE = "message"
    NOTICE = "notice"
    REQUEST = "request"
    ACTION = "action"
    ACTION_RESPONSE = "action_response"
    META = "meta"


class EventTypeRegistry:
    """
    动态事件类型注册器，支持运行时注册新的事件类型。
    支持平台特定的事件类型架构和智能推荐。
    """

    def __init__(self):
        self._registered_types = {}
        self._platform_types = {}
        self._platform_schemas = {}  # 平台事件类型架构
        self._type_suggestions = {}  # 事件类型智能推荐缓存
        # 注册核心事件类型
        self._register_core_types()

    def _register_core_types(self):
        """注册最基础的核心事件类型。"""
        # 仅注册最基础的、跨平台通用的事件类型
        core_types = {
            "message.send": "发送消息（通用）",
            "message.receive": "接收消息（通用）",
            "notice.member_change": "成员变更通知（通用）",
            "notice.message_update": "消息更新通知（通用）",
            "request.authorization": "授权请求（通用）",
            "action.send": "发送动作（通用）",
            "action.manage": "管理动作（通用）",
            "action_response.success": "动作执行成功",
            "action_response.failure": "动作执行失败",
            "meta.lifecycle": "生命周期事件",
            "meta.heartbeat": "心跳事件",
        }

        for event_type, description in core_types.items():
            self.register_type(event_type, description, "core")

    def register_type(
        self, event_type: str, description: str = "", platform: str = "core"
    ) -> bool:
        """
        注册新的事件类型。

        Args:
            event_type: 事件类型字符串，如 "message.qq.poke"
            description: 事件类型描述
            platform: 所属平台，默认为 "core"（核心标准类型）

        Returns:
            bool: 注册是否成功
        """
        if not validate_event_type(event_type):
            return False

        self._registered_types[event_type] = {
            "description": description,
            "platform": platform,
            "registered_at": time.time(),
        }

        # 按平台分组
        if platform not in self._platform_types:
            self._platform_types[platform] = []
        if event_type not in self._platform_types[platform]:
            self._platform_types[platform].append(event_type)

        # 清理相关的推荐缓存
        self._clear_suggestion_cache(platform)

        return True

    def register_platform_types(
        self, platform: str, types_mapping: Dict[str, str]
    ) -> List[str]:
        """
        批量注册平台特定的事件类型。

        Args:
            platform: 平台名称，如 "qq", "discord", "wechat"
            types_mapping: 事件类型映射，{event_type: description}

        Returns:
            List[str]: 成功注册的事件类型列表
        """
        registered = []
        for event_type, description in types_mapping.items():
            if self.register_type(event_type, description, platform):
                registered.append(event_type)
        return registered

    def register_platform_schema(self, platform: str, schema: Dict[str, Any]) -> bool:
        """
        注册平台事件类型架构。

        Args:
            platform: 平台名称
            schema: 事件类型架构，包含类型定义、验证规则、转换映射等
                   例如：{
                       "types": {...},
                       "validation_rules": {...},
                       "type_mapping": {...},
                       "capabilities": [...]
                   }

        Returns:
            bool: 注册是否成功
        """
        self._platform_schemas[platform] = {
            "schema": schema,
            "registered_at": time.time(),
            "version": schema.get("version", "1.0.0"),
        }

        # 如果架构中包含事件类型定义，自动注册这些类型
        if "types" in schema:
            self.register_platform_types(platform, schema["types"])

        return True

    def suggest_event_type(
        self, platform: str, action: str, context: str = ""
    ) -> List[str]:
        """
        基于平台、动作和上下文智能推荐事件类型。

        Args:
            platform: 平台名称
            action: 动作描述，如 "send_message", "kick_user"
            context: 上下文信息，如 "group", "private"

        Returns:
            List[str]: 推荐的事件类型列表，按相关性排序
        """
        cache_key = f"{platform}:{action}:{context}"
        if cache_key in self._type_suggestions:
            return self._type_suggestions[cache_key]

        suggestions = []
        platform_types = self.get_platform_types(platform)

        # 基于动作和上下文进行匹配
        for event_type in platform_types:
            score = self._calculate_type_relevance(event_type, action, context)
            if score > 0:
                suggestions.append((event_type, score))

        # 按相关性排序并返回事件类型列表
        suggestions.sort(key=lambda x: x[1], reverse=True)
        result = [event_type for event_type, _ in suggestions]

        # 缓存结果
        self._type_suggestions[cache_key] = result
        return result

    def _calculate_type_relevance(
        self, event_type: str, action: str, context: str
    ) -> float:
        """计算事件类型与动作/上下文的相关性评分。"""
        score = 0.0
        event_parts = event_type.split(".")

        # 动作匹配
        if action.lower() in event_type.lower():
            score += 0.5

        # 上下文匹配
        if context and context.lower() in event_type.lower():
            score += 0.3

        # 前缀匹配（message/action/notice等）
        action_prefixes = {
            "send": ["message", "action"],
            "receive": ["message"],
            "kick": ["action"],
            "ban": ["action"],
            "add": ["request", "action"],
            "join": ["notice", "request"],
            "leave": ["notice"],
        }

        for keyword, prefixes in action_prefixes.items():
            if keyword in action.lower() and any(
                prefix in event_parts[0] for prefix in prefixes
            ):
                score += 0.2

        return score

    def _clear_suggestion_cache(self, platform: str = None):
        """清理推荐缓存。"""
        if platform:
            # 清理特定平台的缓存
            keys_to_remove = [
                k for k in self._type_suggestions.keys() if k.startswith(f"{platform}:")
            ]
            for key in keys_to_remove:
                del self._type_suggestions[key]
        else:
            # 清理所有缓存
            self._type_suggestions.clear()

    def is_registered(self, event_type: str) -> bool:
        """检查事件类型是否已注册。"""
        return event_type in self._registered_types

    def get_description(self, event_type: str) -> str:
        """获取事件类型描述。"""
        return self._registered_types.get(event_type, {}).get("description", "")

    def get_platform_types(self, platform: str) -> List[str]:
        """获取指定平台的所有事件类型。"""
        return self._platform_types.get(platform, [])

    def get_platform_schema(self, platform: str) -> Dict[str, Any]:
        """获取平台事件类型架构。"""
        return self._platform_schemas.get(platform, {}).get("schema", {})

    def get_all_types(self) -> Dict[str, Dict[str, Any]]:
        """获取所有已注册的事件类型。"""
        return self._registered_types.copy()

    def get_types_by_prefix(self, prefix: str) -> List[str]:
        """获取指定前缀的所有事件类型。"""
        return [
            event_type
            for event_type in self._registered_types.keys()
            if event_type.startswith(prefix + ".")
        ]

    def get_platforms(self) -> List[str]:
        """获取所有已注册的平台列表。"""
        return list(self._platform_types.keys())

    def validate_event_for_platform(self, event_type: str, platform: str) -> bool:
        """验证事件类型是否适用于指定平台。"""
        platform_schema = self.get_platform_schema(platform)
        if not platform_schema:
            # 如果没有架构定义，允许所有符合基本格式的事件类型
            return validate_event_type(event_type)

        # 根据平台架构进行验证
        validation_rules = platform_schema.get("validation_rules", {})
        if validation_rules:
            return self._validate_by_rules(event_type, validation_rules)

        # 检查是否在平台支持的类型列表中
        return event_type in self.get_platform_types(platform)

    def _validate_by_rules(self, event_type: str, rules: Dict[str, Any]) -> bool:
        """根据验证规则检查事件类型。"""
        # 这里可以实现复杂的验证逻辑
        # 例如：正则表达式匹配、长度限制、格式要求等
        if "pattern" in rules:
            import re

            return bool(re.match(rules["pattern"], event_type))

        if "allowed_prefixes" in rules:
            return any(
                event_type.startswith(prefix) for prefix in rules["allowed_prefixes"]
            )

        return True


# 全局事件类型注册器实例
event_registry = EventTypeRegistry()


class EventType:
    """
    动态事件类型管理器。
    支持运行时注册平台特定事件类型，避免硬编码限制。
    """

    # 仅保留最基础的核心事件类型作为示例
    _CORE_TYPES = {
        # 基础消息事件
        "MESSAGE_SEND": "message.send",  # 通用发送消息
        "MESSAGE_RECEIVE": "message.receive",  # 通用接收消息
        # 基础通知事件
        "NOTICE_MEMBER_CHANGE": "notice.member_change",  # 通用成员变更
        "NOTICE_MESSAGE_UPDATE": "notice.message_update",  # 通用消息更新
        # 基础请求事件
        "REQUEST_AUTHORIZATION": "request.authorization",  # 通用授权请求
        # 基础动作事件
        "ACTION_SEND": "action.send",  # 通用发送动作
        "ACTION_MANAGE": "action.manage",  # 通用管理动作
        # 动作响应事件
        "ACTION_RESPONSE_SUCCESS": "action_response.success",
        "ACTION_RESPONSE_FAILURE": "action_response.failure",
        # 元事件
        "META_LIFECYCLE": "meta.lifecycle",
        "META_HEARTBEAT": "meta.heartbeat",
    }

    def __init__(self):
        # 动态添加核心类型为类属性
        for attr_name, event_type in self._CORE_TYPES.items():
            setattr(self, attr_name, event_type)

    @classmethod
    def register(
        cls, event_type: str, description: str = "", platform: str = "core"
    ) -> bool:
        """注册新的事件类型。"""
        return event_registry.register_type(event_type, description, platform)

    @classmethod
    def register_platform_schema(cls, platform: str, schema: Dict[str, Any]) -> bool:
        """
        注册平台事件类型架构。

        Args:
            platform: 平台名称
            schema: 事件类型架构定义

        Returns:
            bool: 注册是否成功
        """
        return event_registry.register_platform_schema(platform, schema)

    @classmethod
    def is_valid(cls, event_type: str) -> bool:
        """检查事件类型是否有效。"""
        return event_registry.is_registered(event_type) or validate_event_type(
            event_type
        )

    @classmethod
    def get_all_by_platform(cls, platform: str) -> List[str]:
        """获取指定平台的所有事件类型。"""
        return event_registry.get_platform_types(platform)

    @classmethod
    def get_all_by_prefix(cls, prefix: str) -> List[str]:
        """获取指定前缀的所有事件类型。"""
        return event_registry.get_types_by_prefix(prefix)

    @classmethod
    def get_platform_schema(cls, platform: str) -> Dict[str, Any]:
        """获取平台事件类型架构。"""
        return event_registry.get_platform_schema(platform)

    @classmethod
    def suggest_event_type(
        cls, platform: str, action: str, context: str = ""
    ) -> List[str]:
        """
        基于平台、动作和上下文智能推荐事件类型。

        Args:
            platform: 平台名称
            action: 动作描述
            context: 上下文信息

        Returns:
            List[str]: 推荐的事件类型列表
        """
        return event_registry.suggest_event_type(platform, action, context)


class ConversationType:
    """会话类型常量定义。"""

    PRIVATE = "private"
    GROUP = "group"
    CHANNEL = "channel"


class EventBuilder:
    """Event 构建器，提供快速创建各种事件的方法。"""

    @staticmethod
    def generate_event_id() -> str:
        """生成唯一的事件ID。"""
        return str(uuid.uuid4())

    @staticmethod
    def get_current_timestamp() -> float:
        """获取当前Unix毫秒时间戳。"""
        return time.time() * 1000

    @staticmethod
    def create_message_event(
        event_type: str,
        platform: str,
        bot_id: str,
        message_id: str,
        content_segs: List[Seg],
        user_info: Optional[UserInfo] = None,
        conversation_info: Optional[ConversationInfo] = None,
        **kwargs,
    ) -> Event:
        """创建消息事件。"""
        # 将消息元数据作为第一个 Seg
        metadata_seg = SegBuilder.message_metadata(message_id, **kwargs)
        all_content = [metadata_seg] + content_segs

        return Event(
            event_id=EventBuilder.generate_event_id(),
            event_type=event_type,
            time=EventBuilder.get_current_timestamp(),
            platform=platform,
            bot_id=bot_id,
            content=all_content,
            user_info=user_info,
            conversation_info=conversation_info,
        )

    @staticmethod
    def create_notice_event(
        notice_type: str,
        platform: str,
        bot_id: str,
        user_info: Optional[UserInfo] = None,
        conversation_info: Optional[ConversationInfo] = None,
        **notice_data,
    ) -> Event:
        """创建通知事件。"""
        notice_seg = SegBuilder.notice(notice_type, **notice_data)

        return Event(
            event_id=EventBuilder.generate_event_id(),
            event_type=f"notice.{notice_type}",
            time=EventBuilder.get_current_timestamp(),
            platform=platform,
            bot_id=bot_id,
            content=[notice_seg],
            user_info=user_info,
            conversation_info=conversation_info,
        )

    @staticmethod
    def create_request_event(
        request_type: str,
        platform: str,
        bot_id: str,
        user_info: Optional[UserInfo] = None,
        conversation_info: Optional[ConversationInfo] = None,
        **request_data,
    ) -> Event:
        """创建请求事件。"""
        request_seg = SegBuilder.request(request_type, **request_data)

        return Event(
            event_id=EventBuilder.generate_event_id(),
            event_type=f"request.{request_type}",
            time=EventBuilder.get_current_timestamp(),
            platform=platform,
            bot_id=bot_id,
            content=[request_seg],
            user_info=user_info,
            conversation_info=conversation_info,
        )

    @staticmethod
    def create_action_event(
        action_type: str,
        platform: str,
        bot_id: str,
        content: List[Seg],
        user_info: Optional[UserInfo] = None,
        conversation_info: Optional[ConversationInfo] = None,
    ) -> Event:
        """创建动作事件。"""
        return Event(
            event_id=EventBuilder.generate_event_id(),
            event_type=f"action.{action_type}",
            time=EventBuilder.get_current_timestamp(),
            platform=platform,
            bot_id=bot_id,
            content=content,
            user_info=user_info,
            conversation_info=conversation_info,
        )

    @staticmethod
    def create_action_response_event(
        response_type: str,
        platform: str,
        bot_id: str,
        original_event_id: str,
        original_action_type: str,
        status_code: Optional[int] = None,
        message: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Event:
        """创建动作响应事件。"""
        response_data = {
            "original_event_id": original_event_id,
            "original_action_type": original_action_type,
        }
        if status_code is not None:
            response_data["status_code"] = status_code
        if message is not None:
            response_data["message"] = message
        if data is not None:
            response_data["data"] = data
        response_seg = SegBuilder.action_response(response_type, **response_data)

        return Event(
            event_id=EventBuilder.generate_event_id(),
            event_type=f"action_response.{response_type}",
            time=EventBuilder.get_current_timestamp(),
            platform=platform,
            bot_id=bot_id,
            content=[response_seg],
        )

    @staticmethod
    def create_meta_event(
        meta_type: str, platform: str, bot_id: str, **meta_data
    ) -> Event:
        """创建元事件。"""
        meta_seg = Seg(type=f"meta.{meta_type}", data=meta_data)

        return Event(
            event_id=EventBuilder.generate_event_id(),
            event_type=f"meta.{meta_type}",
            time=EventBuilder.get_current_timestamp(),
            platform=platform,
            bot_id=bot_id,
            content=[meta_seg],
        )


def extract_text_from_content(content: List[Seg]) -> str:
    """从 content 中提取所有文本内容。"""
    text_parts = []
    for seg in content:
        if seg.type == "text" and "text" in seg.data:
            text_parts.append(seg.data["text"])
    return "".join(text_parts)


def find_seg_by_type(content: List[Seg], seg_type: str) -> Optional[Seg]:
    """在 content 中查找指定类型的第一个 Seg。"""
    for seg in content:
        if seg.type == seg_type:
            return seg
    return None


def filter_segs_by_type(content: List[Seg], seg_type: str) -> List[Seg]:
    """在 content 中查找指定类型的所有 Seg。"""
    return [seg for seg in content if seg.type == seg_type]
