# quick_demo.py
"""
AIcarus-Message-Protocol v1.6.0 快速功能演示
展示基于命名空间的动态事件类型系统。
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def quick_demo():
    """快速演示核心功能"""
    print("🚀 AIcarus-Message-Protocol v1.6.0 快速演示")
    print("=" * 50)

    # 从新模块导入
    from aicarus_protocols.event_type import (
        EventType,
        validate_event_type,
    )
    from aicarus_protocols.event import Event

    # 1. 动态、自由的事件类型注册
    print("1️⃣ 动态事件类型注册 (遵循命名空间规则)")
    EventType.register("message.my_platform.custom_sticker", "我的平台的自定义贴纸")
    EventType.register("action.another_app.execute_script", "另一个应用执行脚本")
    print("   ✅ 注册成功: message.my_platform.custom_sticker")
    print("   ✅ 注册成功: action.another_app.execute_script")

    # 2. 统一的验证规则
    print("\n2️⃣ 统一的事件类型验证")
    valid_type = "notice.qq.friend_add"
    invalid_type = "message.private"  # 旧格式，现在不合法了
    print(
        f"   - 验证 '{valid_type}': {'合法' if validate_event_type(valid_type) else '非法'}"
    )
    print(
        f"   - 验证 '{invalid_type}': {'合法' if validate_event_type(invalid_type) else '非法'}"
    )

    # 3. 从事件中轻松获取平台信息
    print("\n3️⃣ 从事件中解析平台信息")
    test_event = Event(
        event_id="demo-event-1",
        event_type="action.telegram.send_poll",
        time=0,
        bot_id="tg_bot",
        content=[],
    )
    platform = test_event.get_platform()
    print(f"   - 事件类型: '{test_event.event_type}'")
    print(f"   - 解析出的平台: '{platform}'")

    # 4. 移除了顶层的 platform 字段
    print("\n4️⃣ Event 对象结构简化")
    event_dict = test_event.to_dict()
    has_platform_field = "platform" in event_dict
    print(
        f"   - Event 字典中是否还存在顶层 'platform' 字段: {'是' if has_platform_field else '否，已被移除！'}"
    )

    print("\n" + "=" * 50)
    print("🎉 演示完成！基于命名空间的动态事件系统运行正常！")
    print("\n💡 要查看更详细的示例，请运行:")
    print(
        '   python -m src.aicarus_protocols.examples' # 推荐运行这个，更详细
    )


if __name__ == "__main__":
    quick_demo()
