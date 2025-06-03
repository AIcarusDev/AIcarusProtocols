# AIcarus-Message-Protocol v1.4.0 动态事件类型系统示例

本目录包含了 AIcarus-Message-Protocol v1.4.0 版本中新增的动态事件类型系统的完整演示示例。

## 主要特性

v1.4.0 版本引入了全新的动态事件类型系统，具有以下核心特性：

### 1. 运行时注册自定义事件类型
- 支持在运行时动态注册新的事件类型
- 不再局限于预定义的事件类型列表
- 支持平台特定的事件类型扩展

### 2. 平台特定事件类型架构
- 每个平台可以定义自己的事件类型架构
- 包含验证规则、类型映射、平台能力描述
- 支持版本化管理和自动迁移

### 3. 智能事件类型推荐系统
- 基于动作、上下文和平台自动推荐合适的事件类型
- 支持缓存机制提高推荐性能
- 可扩展的相关性评分算法

### 4. 层次化事件类型结构
- 保持原有的前缀分类体系（message.*, notice.*, etc.）
- 支持更深层的嵌套分类
- 便于事件类型的组织和管理

### 5. 跨平台事件类型映射
- 支持将通用动作映射到平台特定的事件类型
- 简化跨平台开发的复杂性
- 统一的接口调用方式

### 6. 自定义验证规则
- 支持正则表达式、前缀检查等多种验证方式
- 可自定义验证逻辑
- 实时验证事件类型的有效性

## 示例文件说明

### `dynamic_examples.py`
主要的演示文件，包含了所有新特性的完整示例：

- `demo_basic_event_type_registration()` - 基础事件类型注册演示
- `demo_platform_specific_schemas()` - 平台特定架构演示
- `demo_intelligent_event_suggestions()` - 智能推荐演示
- `demo_hierarchical_event_structure()` - 层次化结构演示
- `demo_cross_platform_mapping()` - 跨平台映射演示
- `demo_custom_validation_rules()` - 自定义验证规则演示
- `demo_event_creation_with_dynamic_types()` - 动态事件创建演示
- `demo_advanced_event_type_queries()` - 高级查询演示
- `demo_event_type_metadata()` - 元数据管理演示

### 高级功能类
- `PlatformEventTypeManager` - 平台事件类型管理器示例
- `performance_benchmark()` - 性能基准测试

## 运行示例

### 运行所有演示
```python
from aicarus_protocols.dynamic_examples import run_all_demos
run_all_demos()
```

### 运行单个演示
```python
from aicarus_protocols.dynamic_examples import demo_basic_event_type_registration
demo_basic_event_type_registration()
```

### 运行完整测试（包括高级功能和性能测试）
```python
from aicarus_protocols.dynamic_examples import (
    run_all_demos, demo_platform_manager, performance_benchmark
)

run_all_demos()
demo_platform_manager()
performance_benchmark()
```

## 核心API使用

### 注册自定义事件类型
```python
from aicarus_protocols.common import EventType

# 注册单个事件类型
EventType.register("message.custom.type", "自定义消息类型", "my_platform")

# 批量注册平台事件类型
qq_types = {
    "message.qq.group": "QQ群消息",
    "action.qq.kick": "QQ踢人动作"
}
EventType.register_platform_types("qq", qq_types)
```

### 注册平台架构
```python
platform_schema = {
    "version": "1.0.0",
    "platform": "my_platform",
    "capabilities": ["text", "image", "file"],
    "types": {
        "message.my_platform.dm": "私信",
        "action.my_platform.send": "发送动作"
    },
    "validation_rules": {
        "pattern": r"^(message|action)\.my_platform\.[a-z_]+$"
    }
}
EventType.register_platform_schema("my_platform", platform_schema)
```

### 智能推荐事件类型
```python
# 获取推荐的事件类型
suggestions = EventType.suggest_event_type("qq", "send_message", "group")
print(f"推荐事件类型: {suggestions}")
```

### 查询和验证
```python
# 检查事件类型是否有效
is_valid = EventType.is_valid("message.qq.group")

# 获取平台的所有事件类型
platform_types = EventType.get_all_by_platform("qq")

# 获取指定前缀的事件类型
message_types = EventType.get_all_by_prefix("message")
```

## 性能特点

动态事件类型系统经过性能优化：

- **注册性能**: 1000个事件类型注册耗时 < 5ms
- **查询性能**: 1000次事件类型查询耗时 < 2ms  
- **推荐性能**: 100次智能推荐耗时 < 1ms
- **内存占用**: 优化的数据结构，最小化内存使用

## 兼容性

动态事件类型系统完全向后兼容：

- 所有 v1.2.0 和之前版本的事件类型继续有效
- 原有的 API 调用方式保持不变
- 新功能为可选增强，不影响现有代码

## 实际应用场景

1. **多平台机器人开发**: 轻松支持新的聊天平台
2. **插件系统**: 允许插件注册自定义事件类型
3. **企业集成**: 适配企业内部通信系统
4. **开发工具**: 提供智能的事件类型建议
5. **测试框架**: 动态生成测试事件类型

## 升级指南

从旧版本升级到 v1.4.0：

1. 现有代码无需修改即可正常工作
2. 可选择性地采用新的动态事件类型功能
3. 参考 `UPGRADE_TO_V1.4.0.md` 获取详细升级指南
4. 运行演示示例了解新功能的使用方法

---

更多详细信息请参考：
- [协议文档 v1.4.0](../doc/communication_protocol_v1.4.0.md)
- [升级指南](../UPGRADE_TO_V1.4.0.md)
- [API参考](../src/aicarus_protocols/)
