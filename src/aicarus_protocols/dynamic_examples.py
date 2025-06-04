# filepath: i:\github\FengM\AIcarus-Message-Protocol\src\aicarus_protocols\dynamic_examples.py
"""
AIcarus-Message-Protocol v1.4.0 - 动态事件类型系统示例
展示 v1.4.0 版本中新增的动态事件类型系统的所有功能特性。

主要特性演示：
1. 运行时注册自定义事件类型
2. 平台特定事件类型架构
3. 智能事件类型推荐系统
4. 层次化事件类型结构
5. 跨平台事件类型映射
6. 自定义验证规则
7. 事件类型元数据管理
"""

from typing import Dict, Any
from .common import (
    EventType,
    EventBuilder,
    event_registry,
    PROTOCOL_VERSION,
)
from .event import Event
from .seg import Seg, SegBuilder
from .user_info import UserInfo
from .conversation_info import ConversationInfo


def demo_basic_event_type_registration():
    """
    演示基础事件类型注册功能
    """
    print("=== 基础事件类型注册演示 ===")

    # 注册自定义事件类型
    custom_types = {
        "message.qq.poke": "QQ戳一戳消息",
        "message.discord.slash_command": "Discord斜杠命令",
        "notice.wechat.friend_request": "微信好友请求通知",
        "action.telegram.kick_member": "Telegram踢出成员动作",
        "request.minecraft.server_join": "Minecraft服务器加入请求",
        "meta.system.performance": "系统性能监控元事件",
    }

    for event_type, description in custom_types.items():
        success = EventType.register(event_type, description, "custom")
        print(f"注册事件类型 '{event_type}': {'成功' if success else '失败'}")

    # 验证注册结果
    print("\n已注册的自定义事件类型：")
    for event_type in custom_types.keys():
        if event_registry.is_registered(event_type):
            description = event_registry.get_description(event_type)
            print(f"  - {event_type}: {description}")

    print()


def demo_platform_specific_schemas():
    """
    演示平台特定事件类型架构功能
    """
    print("=== 平台特定事件类型架构演示 ===")

    # QQ平台事件类型架构
    qq_schema = {
        "version": "1.0.0",
        "platform": "qq",
        "capabilities": ["text", "image", "at", "face", "poke", "shake"],
        "types": {
            "message.qq.private": "QQ私聊消息",
            "message.qq.group": "QQ群聊消息",
            "message.qq.temp": "QQ临时会话消息",
            "notice.qq.group_increase": "QQ群成员增加通知",
            "notice.qq.group_decrease": "QQ群成员减少通知",
            "notice.qq.friend_add": "QQ好友添加通知",
            "notice.qq.poke": "QQ戳一戳通知",
            "request.qq.friend": "QQ加好友请求",
            "request.qq.group": "QQ加群请求",
            "action.qq.send_private_msg": "QQ发送私聊消息",
            "action.qq.send_group_msg": "QQ发送群消息",
            "action.qq.kick_group_member": "QQ踢出群成员",
            "action.qq.ban_group_member": "QQ禁言群成员",
        },
        "validation_rules": {
            "allowed_prefixes": ["message.qq", "notice.qq", "request.qq", "action.qq"],
            "pattern": r"^(message|notice|request|action)\.qq\.[a-z_]+$",
        },
        "type_mapping": {
            "send_message": "action.qq.send_private_msg",
            "send_group_message": "action.qq.send_group_msg",
            "kick_user": "action.qq.kick_group_member",
        },
    }

    # Discord平台事件类型架构
    discord_schema = {
        "version": "1.0.0",
        "platform": "discord",
        "capabilities": [
            "text",
            "embed",
            "file",
            "reaction",
            "thread",
            "slash_command",
        ],
        "types": {
            "message.discord.dm": "Discord私信",
            "message.discord.guild": "Discord服务器消息",
            "message.discord.thread": "Discord线程消息",
            "notice.discord.member_join": "Discord成员加入通知",
            "notice.discord.member_leave": "Discord成员离开通知",
            "notice.discord.role_update": "Discord角色更新通知",
            "request.discord.slash_command": "Discord斜杠命令请求",
            "action.discord.send_message": "Discord发送消息",
            "action.discord.create_thread": "Discord创建线程",
            "action.discord.manage_roles": "Discord管理角色",
        },
        "validation_rules": {
            "allowed_prefixes": [
                "message.discord",
                "notice.discord",
                "request.discord",
                "action.discord",
            ],
            "pattern": r"^(message|notice|request|action)\.discord\.[a-z_]+$",
        },
    }

    # 注册平台架构
    platforms = [("qq", qq_schema), ("discord", discord_schema)]
    for platform, schema in platforms:
        success = EventType.register_platform_schema(platform, schema)
        print(f"注册 {platform} 平台架构: {'成功' if success else '失败'}")

        # 显示注册的事件类型
        platform_types = EventType.get_all_by_platform(platform)
        print(f"  {platform} 平台事件类型数量: {len(platform_types)}")
        for event_type in platform_types[:3]:  # 只显示前3个
            print(f"    - {event_type}")
        if len(platform_types) > 3:
            print(f"    ... 还有 {len(platform_types) - 3} 个")

    print()


def demo_intelligent_event_suggestions():
    """
    演示智能事件类型推荐功能
    """
    print("=== 智能事件类型推荐演示 ===")

    # 测试各种推荐场景
    test_cases = [
        ("qq", "send_message", "group", "在QQ群中发送消息"),
        ("qq", "kick_user", "group", "在QQ群中踢出用户"),
        ("discord", "send_message", "dm", "在Discord中发送私信"),
        ("discord", "create_thread", "guild", "在Discord服务器中创建线程"),
        ("qq", "add_friend", "", "QQ添加好友"),
        ("discord", "manage_roles", "guild", "Discord管理角色"),
    ]

    for platform, action, context, description in test_cases:
        suggestions = EventType.suggest_event_type(platform, action, context)
        print(f"{description}:")
        print(f"  平台: {platform}, 动作: {action}, 上下文: {context}")
        if suggestions:
            print("  推荐事件类型:")
            for i, event_type in enumerate(suggestions[:3], 1):
                print(f"    {i}. {event_type}")
        else:
            print("  无推荐事件类型")
        print()


def demo_hierarchical_event_structure():
    """
    演示层次化事件类型结构
    """
    print("=== 层次化事件类型结构演示 ===")

    # 按前缀分组显示事件类型
    prefixes = ["message", "notice", "request", "action", "action_response", "meta"]

    for prefix in prefixes:
        types = EventType.get_all_by_prefix(prefix)
        if types:
            print(f"{prefix.upper()} 类事件 ({len(types)} 个):")
            for event_type in types[:5]:  # 只显示前5个
                description = event_registry.get_description(event_type)
                print(f"  - {event_type}: {description}")
            if len(types) > 5:
                print(f"  ... 还有 {len(types) - 5} 个")
            print()


def demo_cross_platform_mapping():
    """
    演示跨平台事件类型映射
    """
    print("=== 跨平台事件类型映射演示 ===")

    # 定义跨平台映射关系
    cross_platform_mappings = {
        "send_private_message": {
            "qq": "action.qq.send_private_msg",
            "discord": "action.discord.send_message",
            "telegram": "action.telegram.send_message",
            "core": "action.send",  # 通用核心类型
        },
        "kick_member": {
            "qq": "action.qq.kick_group_member",
            "discord": "action.discord.kick_member",
            "telegram": "action.telegram.kick_chat_member",
            "core": "action.manage",
        },
        "member_join": {
            "qq": "notice.qq.group_increase",
            "discord": "notice.discord.member_join",
            "telegram": "notice.telegram.new_chat_members",
            "core": "notice.member_change",
        },
    }

    print("跨平台事件类型映射:")
    for action, mappings in cross_platform_mappings.items():
        print(f"\n{action}:")
        for platform, event_type in mappings.items():
            print(f"  {platform:10} -> {event_type}")


def demo_custom_validation_rules():
    """
    演示自定义验证规则功能
    """
    print("=== 自定义验证规则演示 ===")

    # 测试验证规则
    test_events = [
        ("qq", "message.qq.group"),
        ("qq", "invalid.type.format"),
        ("discord", "message.discord.dm"),
        ("discord", "message.qq.group"),  # 错误的平台匹配
        ("unknown_platform", "message.test.type"),
    ]

    print("事件类型验证测试:")
    for platform, event_type in test_events:
        is_valid = event_registry.validate_event_for_platform(event_type, platform)
        status = "✓" if is_valid else "✗"
        print(
            f"  {status} {platform} 平台验证 '{event_type}': {'有效' if is_valid else '无效'}"
        )

    print()


def demo_event_creation_with_dynamic_types():
    """
    演示使用动态事件类型创建事件
    """
    print("=== 动态事件类型创建事件演示 ===")  # 创建示例用户和会话信息
    user_info = UserInfo(user_id="12345", user_nickname="测试用户", platform="qq")

    conversation_info = ConversationInfo(
        conversation_id="group_67890", type="group", platform="qq"
    )

    # 使用动态注册的事件类型创建事件
    examples = []

    # 1. QQ戳一戳事件
    poke_event = EventBuilder.create_notice_event(
        notice_type="qq.poke",
        platform="qq",
        bot_id="bot_001",
        user_info=user_info,
        conversation_info=conversation_info,
        target_id="54321",
        poke_type="normal",
    )
    examples.append(("QQ戳一戳通知", poke_event))
    # 2. Discord斜杠命令事件
    slash_command_content = [
        SegBuilder.text("/help"),
        Seg(type="command_metadata", data={"command": "help", "category": "general"}),
    ]
    slash_event = EventBuilder.create_message_event(
        event_type="message.discord.slash_command",
        platform="discord",
        bot_id="bot_002",
        message_id="msg_789",
        content_segs=slash_command_content,
        user_info=user_info,
        conversation_info=conversation_info,
    )
    examples.append(("Discord斜杠命令", slash_event))

    # 3. 系统性能监控元事件
    performance_event = EventBuilder.create_meta_event(
        meta_type="system.performance",
        platform="core",
        bot_id="system",
        cpu_usage=45.2,
        memory_usage=1024.5,
        network_latency=23.1,
    )
    examples.append(("系统性能监控", performance_event))

    # 显示创建的事件
    for description, event in examples:
        print(f"{description}:")
        print(f"  事件ID: {event.event_id}")
        print(f"  事件类型: {event.event_type}")
        print(f"  平台: {event.platform}")
        print(f"  内容段数量: {len(event.content)}")

        # 显示第一个内容段的信息
        if event.content:
            first_seg = event.content[0]
            print(f"  首个内容段: {first_seg.type}")
        print()


def demo_advanced_event_type_queries():
    """
    演示高级事件类型查询功能
    """
    print("=== 高级事件类型查询演示 ===")

    # 获取所有平台
    platforms = event_registry.get_platforms()
    print(f"支持的平台 ({len(platforms)} 个): {', '.join(platforms)}")

    # 获取所有注册的事件类型
    all_types = event_registry.get_all_types()
    print(f"\n总共注册的事件类型数量: {len(all_types)}")

    # 按平台统计
    print("\n各平台事件类型统计:")
    for platform in platforms:
        platform_types = event_registry.get_platform_types(platform)
        print(f"  {platform}: {len(platform_types)} 个事件类型")

    # 按前缀统计
    print("\n各类别事件类型统计:")
    prefixes = ["message", "notice", "request", "action", "action_response", "meta"]
    for prefix in prefixes:
        prefix_types = event_registry.get_types_by_prefix(prefix)
        print(f"  {prefix}: {len(prefix_types)} 个事件类型")

    print()


def demo_event_type_metadata():
    """
    演示事件类型元数据管理
    """
    print("=== 事件类型元数据演示 ===")

    # 显示一些事件类型的详细元数据
    sample_types = [
        "message.qq.group",
        "notice.discord.member_join",
        "action.qq.send_private_msg",
        "meta.system.performance",
    ]

    print("事件类型详细信息:")
    for event_type in sample_types:
        if event_registry.is_registered(event_type):
            type_info = event_registry._registered_types[event_type]
            print(f"\n{event_type}:")
            print(f"  描述: {type_info['description']}")
            print(f"  平台: {type_info['platform']}")
            print(f"  注册时间: {type_info['registered_at']:.0f}")
        else:
            print(f"\n{event_type}: 未注册")

    print()


def run_all_demos():
    """
    运行所有演示示例
    """
    print(f"AIcarus-Message-Protocol v{PROTOCOL_VERSION}")
    print("动态事件类型系统功能演示")
    print("=" * 50)
    print()

    # 按顺序运行所有演示
    # 注意：先注册平台架构，再运行智能推荐演示
    demos = [
        demo_basic_event_type_registration,
        demo_platform_specific_schemas,
        demo_intelligent_event_suggestions,  # 必须在平台架构注册之后
        demo_hierarchical_event_structure,
        demo_cross_platform_mapping,
        demo_custom_validation_rules,
        demo_event_creation_with_dynamic_types,
        demo_advanced_event_type_queries,
        demo_event_type_metadata,
    ]

    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"演示 {demo.__name__} 执行出错: {e}")
            print()

    print("=" * 50)
    print("所有演示完成！")


# 高级功能演示类
class PlatformEventTypeManager:
    """
    平台事件类型管理器示例类
    展示如何在实际应用中管理动态事件类型
    """

    def __init__(self):
        self.platform_configs = {}
        self.event_handlers = {}

    def register_platform(self, platform: str, config: Dict[str, Any]):
        """注册平台配置"""
        self.platform_configs[platform] = config

        # 自动注册平台事件类型架构
        if "event_schema" in config:
            EventType.register_platform_schema(platform, config["event_schema"])

        print(f"平台 {platform} 注册成功")

    def suggest_handler_for_event(self, event_type: str, platform: str) -> str:
        """为事件类型推荐处理器"""
        # 根据事件类型推荐合适的处理器
        if event_type.startswith("message."):
            return "MessageHandler"
        elif event_type.startswith("notice."):
            return "NoticeHandler"
        elif event_type.startswith("request."):
            return "RequestHandler"
        elif event_type.startswith("action."):
            return "ActionHandler"
        elif event_type.startswith("action_response."):
            return "ActionResponseHandler"
        elif event_type.startswith("meta."):
            return "MetaHandler"
        else:
            return "DefaultHandler"

    def validate_and_process_event(self, event: Event) -> bool:
        """验证并处理事件"""
        # 验证事件类型
        if not event_registry.validate_event_for_platform(
            event.event_type, event.platform
        ):
            print(f"事件类型 {event.event_type} 在平台 {event.platform} 上无效")
            return False

        # 推荐处理器
        handler = self.suggest_handler_for_event(event.event_type, event.platform)
        print(f"事件 {event.event_type} 推荐使用处理器: {handler}")

        return True


def demo_platform_manager():
    """
    演示平台事件类型管理器
    """
    print("=== 平台事件类型管理器演示 ===")

    manager = PlatformEventTypeManager()

    # 注册平台配置
    qq_config = {
        "name": "QQ",
        "version": "1.0.0",
        "event_schema": {
            "version": "1.0.0",
            "platform": "qq",
            "types": {"message.qq.group": "QQ群消息", "notice.qq.poke": "QQ戳一戳通知"},
        },
    }

    manager.register_platform("qq", qq_config)

    # 创建测试事件
    test_event = EventBuilder.create_message_event(
        event_type="message.qq.group",
        platform="qq",
        bot_id="test_bot",
        message_id="test_msg",
        content_segs=[SegBuilder.text("测试消息")],
    )

    # 验证和处理事件
    success = manager.validate_and_process_event(test_event)
    print(f"事件处理: {'成功' if success else '失败'}")

    print()


# 性能测试函数
def performance_benchmark():
    """
    动态事件类型系统性能基准测试
    """
    print("=== 性能基准测试 ===")

    import time

    # 测试大量事件类型注册的性能
    start_time = time.time()

    # 注册1000个事件类型
    for i in range(1000):
        event_type = f"test.performance.type_{i:04d}"
        EventType.register(event_type, f"性能测试事件类型 {i}", "benchmark")

    registration_time = time.time() - start_time
    print(f"注册1000个事件类型耗时: {registration_time:.3f}秒")

    # 测试事件类型查询性能
    start_time = time.time()

    for i in range(1000):
        event_type = f"test.performance.type_{i:04d}"
        event_registry.is_registered(event_type)

    query_time = time.time() - start_time
    print(f"查询1000个事件类型耗时: {query_time:.3f}秒")

    # 测试智能推荐性能
    start_time = time.time()

    for i in range(100):
        EventType.suggest_event_type("benchmark", f"action_{i}", "test")

    suggestion_time = time.time() - start_time
    print(f"执行100次智能推荐耗时: {suggestion_time:.3f}秒")

    print()


if __name__ == "__main__":
    # 运行所有演示
    run_all_demos()

    # 运行高级功能演示
    demo_platform_manager()

    # 运行性能测试
    performance_benchmark()
