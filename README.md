# AIcarus Protocols - 通信协议库 (v1.6.0)

本库定义了 AIcarus 项目中 Core (核心) 与 Adapter (适配器) 之间进行通信所遵循的标准化事件结构。它基于 **AIcarus-Message-Protocol v1.6.0**。

## 主要特性 (v1.6.0)

*   **命名空间驱动的事件系统**:
    *   引入了强制性的、层级化的 `event_type` 字段（例如 `message.qq.group.normal`, `action.discord.kick_member`），这是协议的核心。
    *   废弃了 `Event` 对象顶层的 `platform` 字段，平台信息现在完全由 `event_type` 的第二部分承载。
*   **简化的数据对象**:
    *   `UserInfo` 和 `ConversationInfo` 对象不再包含 `platform` 字段，成为更纯粹的数据载体。
*   **统一的载荷结构**:
    *   所有事件的具体参数和消息内容统一存放于 `content: List[Seg]` 字段中。
    *   `Seg` (Segment) 对象作为通用信息单元，用于承载不同类型的事件内容。

## 安装

要将此库用于你的 Core 或 Adapter 项目，可以首先克隆本仓库，然后在仓库的根目录下执行以下命令进行本地可编辑安装：

```bash
pip install -e .
```

这将允许你在开发 Core 或 Adapter 时，如果修改了本协议库的代码，更改会立即生效，无需重新安装。

## 使用示例 (v1.6.0)

在你的 Core 或 Adapter 项目中，你可以这样导入和使用协议中定义的类。新的命名空间系统使得事件的创建和解析更加直观。

```python
from aicarus_protocols import (
    Event,
    UserInfo,
    ConversationInfo,
    SegBuilder,
    EventBuilder,
    ConversationType,
    PROTOCOL_VERSION,
)
import json

# 1. 创建一个包含文本和图片的用户消息事件
# 注意：UserInfo 和 ConversationInfo 不再需要 platform 字段
user_info_data = UserInfo(
    user_id="12345",
    user_nickname="未来星織",
)

conversation_info_data = ConversationInfo(
    conversation_id="group_789",
    type=ConversationType.GROUP,
    name="AIcarus大家庭"
)

content_segments = [
    SegBuilder.text("主人，你看这张图色不色？"),
    SegBuilder.image(
        url="http://example.com/horny_cat.jpg", 
        file_id="platform_image_id_12345",
    )
]

# 2. 使用 EventBuilder 创建事件
# 注意：不再需要 platform 参数，平台信息直接包含在 event_type 中
my_message_event = EventBuilder.create_message_event(
    event_type="message.qq.group.normal",  # <--- 关键变更！
    bot_id="robot_qq_789",
    message_id="msg_abc_123",
    content_segs=content_segments,
    user_info=user_info_data,
    conversation_info=conversation_info_data
)

# 3. 将事件对象转换为字典 (例如用于网络传输)
event_dict = my_message_event.to_dict()
print("--- 用户消息事件示例 (v1.6.0 JSON) ---")
print(json.dumps(event_dict, indent=2, ensure_ascii=False))


# 4. 从字典转换回事件对象 (例如接收到网络数据后)
received_event = Event.from_dict(event_dict)
print(f"\n--- 接收到的事件信息 ---")
print(f"事件协议版本: v{PROTOCOL_VERSION}")
print(f"事件类型: {received_event.event_type}")
# 使用新的 get_platform() 方法从 event_type 中提取平台信息
print(f"解析出的平台: {received_event.get_platform()}") # <--- 新的玩法！
print(f"发送者: {received_event.user_info.user_nickname}")
print(f"消息文本: '{received_event.get_text_content()}'")

# 5. 查找特定类型的 Seg 依然简单
from aicarus_protocols import find_seg_by_type
image_seg = find_seg_by_type(received_event.content, "image")
if image_seg:
    print("图片信息:")
    if "url" in image_seg.data:
        print(f"  - URL: {image_seg.data['url']}")
    if "file_id" in image_seg.data:
        print(f"  - File ID: {image_seg.data['file_id']}")
```

## 协议版本

本文档和代码库基于 **AIcarus-Message-Protocol v1.6.0**。
详细的协议定义请参考项目内的 `doc/communication_protocol_v1.6.0.md`。
Python 实现细节请查看 `src/aicarus_protocols` 目录。