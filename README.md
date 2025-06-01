# AIcarus Protocols - 通信协议库

本库定义了 AIcarus 项目中 Core (核心) 与 Adapter (适配器) 之间进行通信所遵循的标准化消息结构。它基于 AIcarus-Message-Protocol v{AICARUS_PROTOCOL_VERSION}。

## 主要特性

* 定义了统一的 `MessageBase` 作为所有交互的顶层载体。
* 使用 `Seg` (Segment) 对象来表示不同类型的消息内容、通知、请求和动作。
* 包含 `UserInfo` 和 `GroupInfo` 等标准化的信息结构。
* 明确了 `interaction_purpose` (交互意图) 以区分不同类型的通信。

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
from aicarus_protocols import MessageBase, Seg, UserInfo, GroupInfo, BaseMessageInfo

# 创建一个用户消息对象
user_info_data = UserInfo(
    platform="qq",
    user_id="12345",
    user_nickname="测试用户"
)

message_info_data = BaseMessageInfo(
    platform="qq_adapter_1", # 适配器标识
    bot_id="robot_qq_789",    # 机器人ID
    interaction_purpose="user_message",
    time=1678886400123.0,
    user_info=user_info_data,
    message_type="private",
    additional_config={{"protocol_version": "{AICARUS_PROTOCOL_VERSION}"}} # 使用f-string插入版本
)

text_segment = Seg(type="text", data="你好，世界！")
message_content_segment = Seg(type="seglist", data=[text_segment])

my_message = MessageBase(
    message_info=message_info_data,
    message_segment=message_content_segment,
    raw_message="原始文本：你好，世界！"
)

# 将消息对象转换为字典 (例如用于网络传输)
message_dict = my_message.to_dict()
print(message_dict)

# 从字典转换回消息对象 (例如接收到网络数据后)
received_message = MessageBase.from_dict(message_dict)
print(received_message.message_info.user_info.user_nickname)
```

## 协议版本

本文档和代码库基于 **AIcarus-Message-Protocol v1.2.0**。
详细的协议定义请参考项目内的 `communication_protocol.md` (如果包含在该仓库或主文档仓库中)。
Python 实现细节请查看 `src/aicarus_protocols/base.py`。