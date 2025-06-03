#!/usr/bin/env python3
"""
AIcarus-Message-Protocol v1.4.0 动态事件类型系统验证脚本
快速验证所有功能是否正常工作
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_basic_functionality():
    """测试基础功能"""
    print("🔍 测试基础功能...")
    
    from aicarus_protocols.common import EventType, event_registry
      # 测试注册功能
    success = EventType.register("message.test.validation", "基础验证测试", "test")
    assert success, "基础事件类型注册失败"
    
    # 测试查询功能
    assert event_registry.is_registered("message.test.validation"), "注册的事件类型无法查询"
    
    print("✅ 基础功能测试通过")

def test_platform_schema():
    """测试平台架构功能"""
    print("🔍 测试平台架构功能...")
    
    from aicarus_protocols.common import EventType
    
    test_schema = {
        "version": "1.0.0",
        "platform": "test_platform",
        "types": {
            "message.test_platform.msg": "测试消息"
        },
        "validation_rules": {
            "pattern": r"^message\.test_platform\.[a-z_]+$"
        }
    }
    
    success = EventType.register_platform_schema("test_platform", test_schema)
    assert success, "平台架构注册失败"
    
    platform_types = EventType.get_all_by_platform("test_platform")
    assert len(platform_types) > 0, "平台事件类型查询失败"
    
    print("✅ 平台架构功能测试通过")

def test_intelligent_suggestions():
    """测试智能推荐功能"""
    print("🔍 测试智能推荐功能...")
    
    from aicarus_protocols.common import EventType, event_registry
    
    # 先注册一些测试平台的事件类型
    test_types = {
        "message.suggestion_test.send": "发送消息",
        "action.suggestion_test.kick": "踢出用户"
    }
    # 使用 event_registry 的方法
    registered = event_registry.register_platform_types("suggestion_test", test_types)
    assert len(registered) > 0, "平台事件类型注册失败"
    
    # 测试推荐功能
    suggestions = EventType.suggest_event_type("suggestion_test", "send", "")
    assert len(suggestions) > 0, "智能推荐功能无结果"
    
    print("✅ 智能推荐功能测试通过")

def test_event_creation():
    """测试事件创建功能"""
    print("🔍 测试事件创建功能...")
    
    from aicarus_protocols.common import EventBuilder
    from aicarus_protocols.seg import SegBuilder
    from aicarus_protocols.user_info import UserInfo
    from aicarus_protocols.conversation_info import ConversationInfo
    
    # 创建测试用户和会话信息
    user = UserInfo(user_id="test_user", user_nickname="测试用户", platform="test")
    conversation = ConversationInfo(conversation_id="test_conv", type="private", platform="test")
    
    # 创建测试事件
    event = EventBuilder.create_message_event(
        event_type="message.test.validation",
        platform="test",
        bot_id="test_bot",
        message_id="test_msg",
        content_segs=[SegBuilder.text("测试消息")],
        user_info=user,
        conversation_info=conversation
    )
    
    assert event.event_type == "message.test.validation", "事件类型设置错误"
    assert event.platform == "test", "平台设置错误"
    assert len(event.content) >= 1, "事件内容为空"
    
    print("✅ 事件创建功能测试通过")

def test_performance():
    """测试性能"""
    print("🔍 测试性能...")
    
    import time
    from aicarus_protocols.common import EventType, event_registry
    
    # 测试大量注册的性能
    start_time = time.time()
    for i in range(100):  # 减少数量以加快测试
        EventType.register(f"meta.performance.type_{i:03d}", f"性能测试 {i}", "perf_test")
    registration_time = time.time() - start_time
    
    # 测试查询性能
    start_time = time.time()
    for i in range(100):
        event_registry.is_registered(f"meta.performance.type_{i:03d}")
    query_time = time.time() - start_time
    
    assert registration_time < 1.0, f"注册性能过慢: {registration_time:.3f}s"
    assert query_time < 0.1, f"查询性能过慢: {query_time:.3f}s"
    
    print(f"✅ 性能测试通过 (注册: {registration_time:.3f}s, 查询: {query_time:.3f}s)")

def run_all_tests():
    """运行所有测试"""
    print("🚀 开始 AIcarus-Message-Protocol v1.4.0 功能验证")
    print("=" * 60)
    
    try:
        # 导入必要模块以确保代码正确
        from aicarus_protocols.common import event_registry
        
        test_basic_functionality()
        test_platform_schema()
        test_intelligent_suggestions()
        test_event_creation()
        test_performance()
        
        print("=" * 60)
        print("🎉 所有功能验证通过！AIcarus-Message-Protocol v1.4.0 工作正常")
        
        # 显示一些统计信息
        all_types = event_registry.get_all_types()
        platforms = event_registry.get_platforms()
        
        print(f"📊 统计信息:")
        print(f"   - 总事件类型数量: {len(all_types)}")
        print(f"   - 支持平台数量: {len(platforms)}")
        print(f"   - 支持的平台: {', '.join(platforms)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
