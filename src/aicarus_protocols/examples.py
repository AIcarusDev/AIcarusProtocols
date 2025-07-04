# src/aicarus_protocols/examples.py
"""
AIcarus-Message-Protocol v1.6.0 - 示例和测试
展示如何使用新的、基于命名空间的协议结构创建和处理各种事件。
"""

import json
from . import (
    Seg,
    Event,
    UserInfo,
    ConversationInfo,
    SegBuilder,
    EventBuilder,
    ConversationType,
    PROTOCOL_VERSION,
    EventType,
    validate_event_type,
)


# 在演示开始前，动态注册一些平台相关的事件类型，模拟真实使用场景
def register_demo_types():
    print("--- 动态注册演示用事件类型 ---")
    EventType.register("message.qq.group", "QQ群消息")
    EventType.register("notice.discord.member_join", "Discord成员加入")
    EventType.register("action.wechat.send_text", "微信发送文本")
    EventType.register("meta.system.startup", "核心系统启动")
    print("------------------------------\n")


def test_message_event():
    """测试创建用户消息事件。"""
    print("=== 测试用户消息事件 ===")

    # 创建用户信息 (不再需要 platform 字段)
    user_info = UserInfo(
        user_id="user_sender_456",
        user_nickname="李四",
        user_cardname="群里的李四",
        permission_level="member",
    )

    # 创建会话信息 (不再需要 platform 字段)
    conversation_info = ConversationInfo(
        conversation_id="group123",
        type=ConversationType.GROUP,
        name="AIcarus淫乱派对",
    )

    content_segs = [
        SegBuilder.text("你好，这是符合新规范的消息！"),
        SegBuilder.face("66"),  # QQ经典滑稽
    ]

    # 关键：event_type 必须包含平台信息！
    # EventBuilder 不再需要 platform 参数！
    message_event = EventBuilder.create_message_event(
        event_type="message.qq.group",  # <--- 看这里！
        bot_id="10001",
        message_id="platform_msg_789",
        content_segs=content_segs,
        user_info=user_info,
        conversation_info=conversation_info,
    )

    event_dict = message_event.to_dict()
    print("用户消息事件 (JSON格式):")
    print(json.dumps(event_dict, indent=2, ensure_ascii=False))

    # 测试从字典重构
    reconstructed_event = Event.from_dict(event_dict)
    print(f"\n重构的事件类型: {reconstructed_event.event_type}")
    print(
        f"从事件中解析出的平台: {reconstructed_event.get_platform()}"
    )  # <--- 测试新方法！
    print(f"消息文本内容: '{reconstructed_event.get_text_content()}'")

    return message_event


def test_action_event():
    """测试创建动作事件 (V6.0 规范)。"""
    print("\n=== 测试动作事件 ===")

    target_conversation = ConversationInfo(
        conversation_id="user_wechat_123", type=ConversationType.PRIVATE
    )

    # 假设我们要调用微信的打电话功能
    # Seg 的 type 最好与动作的最后一部分对应，便于适配器解析
    action_content = [Seg(type="call", data={"remark": "来自AIcarus核心的爱心呼叫"})]

    # 创建动作事件，event_type 包含平台
    action_event = Event(
        event_id=EventBuilder.generate_event_id(),
        event_type="action.wechat.call",  # <--- 新的命名方式！
        time=EventBuilder.get_current_timestamp(),
        bot_id="wx_bot_abc",
        content=action_content,
        conversation_info=target_conversation,
    )

    event_dict = action_event.to_dict()
    print("微信打电话动作 (JSON格式):")
    print(json.dumps(event_dict, indent=2, ensure_ascii=False))

    print(f"\n从动作事件中解析出的平台: {action_event.get_platform()}")

    return action_event


def test_action_response_event():
    """测试创建动作响应事件 (V6.0 规范)。"""
    print("\n=== 测试动作响应事件 ===")

    # 先有一个原始的动作事件
    original_action = test_action_event()

    # 创建成功响应，现在 builder 会自动从原始事件中推断平台和类型
    success_response = EventBuilder.create_action_response_event(
        response_type="success",
        original_event=original_action,
        status_code=200,
        message="呼叫已成功接通。",
        data={"call_duration": 30},
    )

    event_dict = success_response.to_dict()
    print("动作成功响应 (JSON格式):")
    print(json.dumps(event_dict, indent=2, ensure_ascii=False))
    print(f"响应事件的类型是: {success_response.event_type}")
    print(f"从响应事件中解析出的平台: {success_response.get_platform()}")

    return success_response


def test_validation():
    """测试新的事件类型验证逻辑。"""
    print("\n=== 测试事件类型验证 ===")

    valid_types = [
        "message.qq.group",
        "action.discord.kick_member",
        "meta.system.heartbeat",
    ]
    invalid_types = [
        "message.group",  # 缺少平台
        "qq.message.group",  # 前缀错误
        "message.qq",  # 缺少动作
        "message..group",  # 平台名为空
        "unknownprefix.platform.action",  # 未知前缀
    ]

    print("合法类型测试:")
    for t in valid_types:
        is_valid = validate_event_type(t)
        print(f"  - '{t}': {'✅ 合法' if is_valid else '❌ 非法'}")

    print("\n非法类型测试:")
    for t in invalid_types:
        is_valid = validate_event_type(t)
        print(f"  - '{t}': {'✅ 合法' if is_valid else '❌ 非法'}")


def main():
    """主测试函数。"""
    print(f"AIcarus-Message-Protocol v{PROTOCOL_VERSION} 示例和测试 (V6.0 规范)")
    print("=" * 60)

    try:
        register_demo_types()
        test_message_event()
        test_action_event()
        test_action_response_event()
        test_validation()

        print("\n" + "=" * 60)
        print("所有测试完成！")

    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
