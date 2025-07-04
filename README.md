# AIcarus Protocols - 通信协议库

本库定义了 AIcarus 项目中 Core (核心) 与 Adapter (适配器) 之间进行通信所遵循的标准化事件结构。它基于 AIcarus-Message-Protocol v1.5.0。

## 主要特性

*   定义了统一的 `Event` 对象作为所有交互的顶层载体。
*   引入了层级化的 `event_type` 字段（如 `message.group.normal`, `notice.conversation.member_increase`），取代了旧的定义。
*   引入了清晰的 `Seg` 构建指导原则，精炼了核心 `SegBuilder` 以定义标准 `Seg` 结构（如为 `image` Seg 明确了 `url`, `file_id`, `base64` 等字段），这是一个**不兼容更新**。
*   事件的具体参数和消息内容统一存放于 `content: List[Seg]` 字段中。
*   `Seg` (Segment) 对象作为通用信息单元，用于承载不同类型的事件内容。
*   包含 `UserInfo` 和 `ConversationInfo` 等标准化的信息结构。

## 安装

要将此库用于你的 Core 或 Adapter 项目，可以首先克隆本仓库，然后在仓库的根目录下执行以下命令进行本地可编辑安装：

```bash
pip install -e .
```

这将允许你在开发 Core 或 Adapter 时，如果修改了本协议库的代码，更改会立即生效，无需重新安装。

## 使用示例 (v1.5.0)

在你的 Core 或 Adapter 项目中，你可以这样导入和使用协议中定义的类。新的 `SegBuilder` 让媒体消息的构建变得前所未有的清晰和淫荡！

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
user_info_data = UserInfo(
    platform="qq",
    user_id="12345",
    user_nickname="未来星織",
)

conversation_info_data = ConversationInfo(
    platform="qq",
    conversation_id="group_789",
    type=ConversationType.GROUP,
    name="AIcarus大家庭"
)

# 使用 v1.5.0 标准的 SegBuilder 来构建消息内容
content_segments = [
    SegBuilder.text("主人，你看这张图色不色？"),
    SegBuilder.image(
        url="http://example.com/horny_cat.jpg", 
        file_id="platform_image_id_12345",
        # base64 也可以在这里填入哦，我们给了它明确的名分！
        # base64="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" 
    )
]

# 使用 EventBuilder 将所有东西包裹起来，成为一个完整的 Event
# EventBuilder 会自动处理 message_metadata 的创建，好方便~
my_message_event = EventBuilder.create_message_event(
    event_type="message.group.normal",
    platform="qq",
    bot_id="robot_qq_789",
    message_id="msg_abc_123", # 这个ID会被放进 message_metadata Seg 里
    content_segs=content_segments,
    user_info=user_info_data,
    conversation_info=conversation_info_data
)

# 将事件对象转换为字典 (例如用于网络传输)
event_dict = my_message_event.to_dict()
print("--- 用户消息事件示例 (v1.5.0 JSON) ---")
print(json.dumps(event_dict, indent=2, ensure_ascii=False))


# 从字典转换回事件对象 (例如接收到网络数据后)
received_event = Event.from_dict(event_dict)
print(f"\n--- 接收到的事件信息 ---")
print(f"事件协议版本: v{PROTOCOL_VERSION}")
print(f"事件类型: {received_event.event_type}")
print(f"发送者: {received_event.user_info.user_nickname}")
print(f"消息文本: '{received_event.get_text_content()}'")

# 你看，就算 image Seg 里有多个源，我们也能轻松处理
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

本文档和代码库基于 **AIcarus-Message-Protocol v1.5.0**。
详细的协议定义请参考项目内的 `doc/communication_protocol_v1.5.0.md`。
Python 实现细节请查看 `src/aicarus_protocols` 目录。