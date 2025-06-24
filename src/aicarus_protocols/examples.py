"""
AIcarus-Message-Protocol v1.5.0 示例和测试
展示如何使用新的协议结构创建和处理各种事件。
"""

import json
from aicarus_protocols import (
    Event,
    UserInfo,
    ConversationInfo,
    SegBuilder,
    EventBuilder,
    ConversationType,
    PROTOCOL_VERSION,
)


def test_message_event():
    """测试创建用户消息事件。"""
    print("=== 测试用户消息事件 ===")

    # 创建用户信息
    user_info = UserInfo(
        platform="qq",
        user_id="user_sender_456",
        user_nickname="李四",
        user_cardname="群里的李四",
        permission_level="member",
        additional_data={"constellation": "aries", "custom_badge": "vip"},
    )

    # 创建会话信息
    conversation_info = ConversationInfo(
        conversation_id="group123",
        type=ConversationType.GROUP,
        platform="qq",
        name="测试群",
    )

    # 创建消息内容
    content_segs = [
        SegBuilder.text("你好 "),
        SegBuilder.at("user_zhangsan_001", "@张三"),
        SegBuilder.text(" "),
        SegBuilder.image(url="http://example.com/image.jpg", file_id="qq_image_abc"),
    ]
    # 创建消息事件
    message_event = EventBuilder.create_message_event(
        event_type="message.receive",  # 使用核心事件类型
        platform="qq",
        bot_id="10001",
        message_id="platform_msg_789",
        content_segs=content_segs,
        user_info=user_info,
        conversation_info=conversation_info,
        font="宋体",
    )

    # 转换为字典并打印
    event_dict = message_event.to_dict()
    print("用户消息事件 (JSON格式):")
    print(json.dumps(event_dict, indent=2, ensure_ascii=False))

    # 测试从字典重构
    reconstructed_event = Event.from_dict(event_dict)
    print(f"\n重构的事件类型: {reconstructed_event.event_type}")
    print(f"消息文本内容: '{reconstructed_event.get_text_content()}'")
    print(f"消息ID: {reconstructed_event.get_message_id()}")

    return message_event


def test_notice_event():
    """测试创建通知事件。"""
    print("\n=== 测试通知事件 ===")

    # 新成员信息
    new_member = UserInfo(
        platform="qq", user_id="new_member_789", user_nickname="萌新小王"
    )

    # 操作者信息
    operator_info = UserInfo(
        platform="qq", user_id="admin_user_007", user_nickname="管理员张三"
    )

    # 群组信息
    group_info = ConversationInfo(
        conversation_id="group123",
        type=ConversationType.GROUP,
        platform="qq",
        name="测试群",
    )

    # 创建群成员增加通知
    notice_event = EventBuilder.create_notice_event(
        notice_type="conversation.member_increase",
        platform="qq",
        bot_id="10001",
        user_info=new_member,
        conversation_info=group_info,
        operator_user_info=operator_info.to_dict(),
        join_type="invite",
    )

    event_dict = notice_event.to_dict()
    print("群成员增加通知 (JSON格式):")
    print(json.dumps(event_dict, indent=2, ensure_ascii=False))

    return notice_event


def test_request_event():
    """测试创建请求事件。"""
    print("\n=== 测试请求事件 ===")

    # 请求者信息
    requester = UserInfo(
        platform="qq", user_id="potential_friend_007", user_nickname="想加好友的小明"
    )

    # 创建好友请求事件
    request_event = EventBuilder.create_request_event(
        request_type="friend.add",
        platform="qq",
        bot_id="10001",
        user_info=requester,
        comment="你好，我是小明，想加你好友！",
        request_flag="flag_for_responding_to_friend_request_abc",
    )

    event_dict = request_event.to_dict()
    print("好友请求事件 (JSON格式):")
    print(json.dumps(event_dict, indent=2, ensure_ascii=False))

    return request_event


def test_action_event():
    """测试创建动作事件。"""
    print("\n=== 测试动作事件 ===")

    # 目标会话
    target_conversation = ConversationInfo(
        conversation_id="target_group_456", type=ConversationType.GROUP, platform="qq"
    )

    # 要发送的消息内容
    message_content = [
        SegBuilder.reply("target_replied_message_id"),
        SegBuilder.text("收到主人的命令！"),
    ]

    # 创建发送消息动作
    action_event = EventBuilder.create_action_event(
        action_type="message.send",
        platform="qq",
        bot_id="10001",
        content=message_content,
        conversation_info=target_conversation,
    )

    event_dict = action_event.to_dict()
    print("发送消息动作 (JSON格式):")
    print(json.dumps(event_dict, indent=2, ensure_ascii=False))

    return action_event


def test_action_response_event():
    """测试创建动作响应事件。"""
    print("\n=== 测试动作响应事件 ===")

    # 创建成功响应
    success_response = EventBuilder.create_action_response_event(
        response_type="success",
        platform="qq",
        bot_id="10001",
        original_event_id="core_action_uuid_1",
        original_action_type="action.message.send",
        status_code=200,
        message="消息已成功发送。",
        data={"sent_message_id": "platform_new_msg_id_abc123"},
    )

    event_dict = success_response.to_dict()
    print("动作成功响应 (JSON格式):")
    print(json.dumps(event_dict, indent=2, ensure_ascii=False))

    # 创建失败响应
    failure_response = EventBuilder.create_action_response_event(
        response_type="failure",
        platform="qq",
        bot_id="10001",
        original_event_id="core_action_uuid_2",
        original_action_type="action.message.send",
        status_code=403,
        message="网络连接错误，无法发送消息。",
    )

    print("\n动作失败响应 (JSON格式):")
    print(json.dumps(failure_response.to_dict(), indent=2, ensure_ascii=False))

    return success_response, failure_response


def test_meta_event():
    """测试创建元事件。"""
    print("\n=== 测试元事件 ===")

    # 创建连接成功元事件
    meta_event = EventBuilder.create_meta_event(
        meta_type="lifecycle.connect",
        platform="qq",
        bot_id="10001",
        adapter_version="1.0.0",
        platform_api_version="v11_custom",
    )

    event_dict = meta_event.to_dict()
    print("Adapter连接成功元事件 (JSON格式):")
    print(json.dumps(event_dict, indent=2, ensure_ascii=False))

    return meta_event


def test_event_utilities():
    """测试事件工具函数。"""
    print("\n=== 测试事件工具函数 ===")
    # 创建一个测试事件
    test_event = Event(
        event_id="test_event_123",
        event_type="message.receive",  # 使用核心事件类型
        time=1678886400123.0,
        platform="qq",
        bot_id="10001",
        content=[
            SegBuilder.message_metadata("msg_123", font="宋体"),
            SegBuilder.text("Hello "),
            SegBuilder.at("user123", "@Someone"),
            SegBuilder.text(" World!"),
        ],
    )

    # 测试事件类型判断
    print(f"是消息事件: {test_event.is_message_event()}")
    print(f"是通知事件: {test_event.is_notice_event()}")
    print(f"是请求事件: {test_event.is_request_event()}")

    # 测试内容提取
    print(f"文本内容: '{test_event.get_text_content()}'")
    print(f"消息ID: {test_event.get_message_id()}")

    # 测试Seg查找
    from aicarus_protocols.common import find_seg_by_type, filter_segs_by_type

    at_seg = find_seg_by_type(test_event.content, "at")
    print(f"找到的@片段: {at_seg}")

    text_segs = filter_segs_by_type(test_event.content, "text")
    print(f"所有文本片段: {text_segs}")


def main():
    """主测试函数。"""
    print(f"AIcarus-Message-Protocol v{PROTOCOL_VERSION} 示例和测试")
    print("=" * 60)

    try:
        # 测试各种事件类型
        test_message_event()
        test_notice_event()
        test_request_event()
        test_action_event()
        test_action_response_event()
        test_meta_event()
        test_event_utilities()

        print("\n" + "=" * 60)
        print("所有测试完成！")

    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
