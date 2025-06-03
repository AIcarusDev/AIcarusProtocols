# AIcarus-Message-Protocol v1.4.0 模块化实现

## 概述

根据 AIcarus-Message-Protocol v1.4.0 协议规范，我们将原来的单一 `base.py` 文件重构为模块化的代码结构，提高了代码的可读性、可维护性和可扩展性。

## 模块结构

### 核心模块

1. **`event.py`** - Event 类
   - 所有交互的顶层载体
   - 包含事件ID、类型、时间戳、平台信息等
   - 提供事件类型判断和内容提取的便利方法

2. **`user_info.py`** - UserInfo 类  
   - 用户信息的完整描述
   - 支持平台特有的额外数据存储
   - 提供字典转换和序列化功能

3. **`conversation_info.py`** - ConversationInfo 类
   - 会话信息描述（群组、私聊、频道等）
   - 支持层级化的会话结构（如频道下的子频道）

4. **`seg.py`** - Seg 类和 SegBuilder 工具
   - 通用信息单元，构成所有事件内容的基本块
   - SegBuilder 提供快速创建常用 Seg 类型的方法

5. **`common.py`** - 通用工具和常量
   - 事件类型常量定义
   - EventBuilder 事件构建器
   - 工具函数（事件类型验证、内容提取等）

6. **`__init__.py`** - 模块入口
   - 统一导出所有公共接口
   - 版本信息管理

7. **`examples.py`** - 示例和测试
   - 展示各种事件类型的创建和使用
   - 提供完整的测试用例

## 主要改进

### 1. 协议升级（v1.2.0 → v1.4.0）

- **统一事件载体**: 所有交互都通过 `Event` 对象封装
- **层级化事件类型**: 采用点分层级结构（如 `message.group.normal`）
- **标准化内容结构**: `content` 字段统一为 `List[Seg]` 格式
- **丰富的事件类型**: 支持消息、通知、请求、动作、动作响应和元事件

### 2. 模块化重构

- **单一职责**: 每个模块负责特定的数据结构
- **减少文件长度**: 原 400+ 行代码分解为多个小文件
- **提高可读性**: 清晰的模块划分和文档注释
- **便于维护**: 修改某个数据结构不影响其他部分

### 3. 增强的功能

- **构建器模式**: `EventBuilder` 和 `SegBuilder` 简化对象创建
- **工具函数**: 提供事件分析和内容提取的便利方法
- **常量定义**: 规范化的事件类型和会话类型常量
- **完整测试**: 覆盖所有事件类型的示例代码

## 使用示例

### 基本导入

```python
from aicarus_protocols import (
    Event, UserInfo, ConversationInfo, Seg, 
    SegBuilder, EventBuilder, EventType
)
```

### 创建用户消息事件

```python
# 创建用户和会话信息
user_info = UserInfo(platform="qq", user_id="123", user_nickname="张三")
conversation_info = ConversationInfo(
    conversation_id="group456", 
    type="group", 
    name="测试群"
)

# 创建消息内容
content_segs = [
    SegBuilder.text("你好 "),
    SegBuilder.at("user789", "@李四"),
    SegBuilder.image(url="http://example.com/image.jpg")
]

# 创建消息事件
message_event = EventBuilder.create_message_event(
    event_type=EventType.MESSAGE_GROUP_NORMAL,
    platform="qq",
    bot_id="10001", 
    message_id="msg_123",
    content_segs=content_segs,
    user_info=user_info,
    conversation_info=conversation_info
)
```

### 创建通知事件

```python
notice_event = EventBuilder.create_notice_event(
    notice_type="conversation.member_increase",
    platform="qq",
    bot_id="10001",
    user_info=new_member_info,
    conversation_info=group_info,
    operator_user_info=operator_info.to_dict(),
    join_type="invite"
)
```

### 事件处理

```python
# 事件类型判断
if event.is_message_event():
    text_content = event.get_text_content()
    message_id = event.get_message_id()
    
# 内容提取
from aicarus_protocols.common import find_seg_by_type
at_seg = find_seg_by_type(event.content, "at")
if at_seg:
    target_user = at_seg.data.get("user_id")
```

## 向后兼容性

- **不保证向后兼容**: v1.4.0 是一个重大版本更新
- **备份保留**: 原 v1.2.0 代码已备份为 `base_v1.2.0_backup.py`
- **迁移指导**: 建议参考 `examples.py` 中的示例进行代码迁移

## 测试运行

```bash
cd src
python -m aicarus_protocols.examples
```

## 文件清单

```
src/aicarus_protocols/
├── __init__.py              # 模块入口
├── event.py                 # Event 类
├── user_info.py            # UserInfo 类  
├── conversation_info.py    # ConversationInfo 类
├── seg.py                  # Seg 类和构建器
├── common.py               # 工具函数和常量
├── examples.py             # 示例和测试
└── base_v1.2.0_backup.py   # v1.2.0 备份文件
```

## 下一步

1. 更新相关项目中的导入语句
2. 根据新的事件结构调整 Core 和 Adapter 代码
3. 完善错误处理和验证逻辑
4. 添加更多的工具函数和便利方法
