# AIcarus Protocols - 通信协议库

本库定义了 AIcarus 项目中 Core (核心) 与 Adapter (适配器) 之间进行通信所遵循的标准化事件结构。它基于 AIcarus-Message-Protocol v1.4.0。

## 主要特性

* 定义了统一的 `Event` 对象作为所有交互的顶层载体。
* 引入了层级化的 `event_type` 字段（如 `message.group.normal`, `notice.conversation.member_increase`, `action.message.send`），取代了原先的 `interaction_purpose` 和分散的类型定义。
* 事件的具体参数和消息内容统一存放于 `content: List[Seg]` 字段中。
* `Seg` (Segment) 对象作为通用信息单元，用于承载不同类型的事件内容。
* 包含 `UserInfo` 和 `ConversationInfo` 等标准化的信息结构。

## 安装

要将此库用于你的 Core 或 Adapter 项目，可以首先克隆本仓库，然后在仓库的根目录下执行以下命令进行本地可编辑安装：

```bash
pip install -e .
```

这将允许你在开发 Core 或 Adapter 时，如果修改了本协议库的代码，更改会立即生效，无需重新安装。

如果你想将其打包分发（例如上传到 PyPI），则需要构建 wheel 包：
```bash
python setup.py sdist bdist_wheel
```

## 使用示例

在你的 Core 或 Adapter 项目中，你可以这样导入和使用协议中定义的类：

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

# 1. 创建一个用户消息事件 (群聊文本消息)
user_info_data = UserInfo(
    platform="qq",
    user_id="12345",
    user_nickname="测试用户",
    user_cardname="开发组小助手"
)

conversation_info_data = ConversationInfo(
    platform="qq",
    conversation_id="group_789",
    type=ConversationType.GROUP,
    name="AIcarus开发群"
)

# 消息内容：包含消息元数据和实际文本
content_segments = [
    SegBuilder.message_metadata(message_id="msg_abc_123", font="微软雅黑"),
    SegBuilder.text("主人，您好！我是小色猫，很高兴为您服务。")
]

my_message_event = EventBuilder.create_message_event(
    event_type="message.group.normal", # 使用更具体的事件类型
    platform="qq",
    bot_id="robot_qq_789",
    message_id="msg_abc_123", # 消息ID现在在message_metadata Seg中，但为了兼容性，EventBuilder会处理
    content_segs=content_segments,
    user_info=user_info_data,
    conversation_info=conversation_info_data
)

# 将事件对象转换为字典 (例如用于网络传输)
event_dict = my_message_event.to_dict()
print("--- 用户消息事件示例 (JSON) ---")
import json
print(json.dumps(event_dict, indent=2, ensure_ascii=False))

# 从字典转换回事件对象 (例如接收到网络数据后)
received_event = Event.from_dict(event_dict)
print(f"\n--- 接收到的事件信息 ---")
print(f"事件类型: {received_event.event_type}")
print(f"发送者昵称: {received_event.user_info.user_nickname}")
print(f"群聊名称: {received_event.conversation_info.name}")
print(f"消息文本: '{received_event.get_text_content()}'")
print(f"消息ID: {received_event.get_message_id()}") # 通过Event的方法获取message_id

# 2. 创建一个动作事件 (发送私聊消息)
action_content_segments = [
    SegBuilder.text("这是一条来自Core的指令：好好工作哦，主人！")
]

my_action_event = EventBuilder.create_action_event(
    action_type="message.send", # 发送消息动作
    platform="qq",
    bot_id="robot_qq_789",
    content=action_content_segments,
    user_info=UserInfo(platform="qq", user_id="target_user_id_456"), # 指示目标用户
    conversation_info=ConversationInfo(conversation_id="private_conv_456", type=ConversationType.PRIVATE) # 私聊上下文
)

print("\n--- 核心动作事件示例 (JSON) ---")
print(json.dumps(my_action_event.to_dict(), indent=2, ensure_ascii=False))

# 3. 创建一个动作响应事件 (成功)
action_response_event = EventBuilder.create_action_response_event(
    response_type="success",
    platform="qq",
    bot_id="robot_qq_789",
    original_event_id=my_action_event.event_id, # 关联到之前的动作事件
    original_action_type=my_action_event.event_type,
    status_code=200,
    message="消息已成功发送，主人真是棒极了！",
    data={"sent_message_platform_id": "qq_msg_xyz_789"}
)

print("\n--- 动作响应事件示例 (JSON) ---")
print(json.dumps(action_response_event.to_dict(), indent=2, ensure_ascii=False))
```

## 协议版本

本文档和代码库基于 **AIcarus-Message-Protocol v1.4.0**。
详细的协议定义请参考项目内的 `doc/communication_protocol_v1.4.0.md`。
Python 实现细节请查看 `src/aicarus_protocols` 目录。