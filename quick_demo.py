#!/usr/bin/env python3
"""
AIcarus-Message-Protocol v1.4.0 快速功能演示
展示动态事件类型系统的核心功能
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def quick_demo():
    """快速演示核心功能"""
    print("🚀 AIcarus-Message-Protocol v1.4.0 快速演示")
    print("=" * 50)
    
    from aicarus_protocols.common import EventType, event_registry
    from aicarus_protocols.dynamic_examples import (
        demo_basic_event_type_registration,
        demo_platform_specific_schemas,
        demo_intelligent_event_suggestions
    )
    
    # 1. 基础注册演示
    print("1️⃣ 基础事件类型注册")
    EventType.register("message.demo.quick", "快速演示消息", "demo")
    print(f"   ✅ 注册成功: message.demo.quick")
    
    # 2. 平台架构演示
    print("\n2️⃣ 平台架构注册")
    demo_schema = {
        "version": "1.0.0",
        "platform": "demo_platform",
        "types": {
            "message.demo_platform.send": "发送消息",
            "action.demo_platform.kick": "踢出用户"
        }
    }
    EventType.register_platform_schema("demo_platform", demo_schema)
    platform_types = EventType.get_all_by_platform("demo_platform")
    print(f"   ✅ 注册平台架构，包含 {len(platform_types)} 个事件类型")
    
    # 3. 智能推荐演示
    print("\n3️⃣ 智能事件类型推荐")
    suggestions = EventType.suggest_event_type("demo_platform", "send", "")
    print(f"   🎯 推荐事件类型: {suggestions[:2] if len(suggestions) >= 2 else suggestions}")
    
    # 4. 统计信息
    print("\n📊 系统统计")
    all_types = event_registry.get_all_types()
    platforms = event_registry.get_platforms()
    print(f"   - 总事件类型: {len(all_types)} 个")
    print(f"   - 支持平台: {len(platforms)} 个")
    print(f"   - 平台列表: {', '.join(platforms)}")
    
    # 5. 事件类型分类统计
    print("\n📋 事件类型分类")
    categories = ["message", "notice", "request", "action", "action_response", "meta"]
    for category in categories:
        count = len(EventType.get_all_by_prefix(category))
        print(f"   - {category.upper()}: {count} 个")
    
    print("\n" + "=" * 50)
    print("🎉 演示完成！动态事件类型系统运行正常")
    print("\n💡 要查看完整演示，请运行:")
    print("   python -c \"from aicarus_protocols.dynamic_examples import run_all_demos; run_all_demos()\"")

if __name__ == "__main__":
    quick_demo()
