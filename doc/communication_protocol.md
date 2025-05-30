# AIcarus-Message-Protocol 通信协议文档

## 1. 概述

本文档定义了聊天机器人核心 (Core) 与平台适配器 (Adapter) 之间，基于 AIcarus-Message-Protocol 的通信协议。该协议旨在提供一套标准化的消息结构和交互模式，以实现组件解耦、易于扩展和多平台支持。其设计参考了 `maim_message` Python 库中的优秀概念。

所有通信均通过 AIcarus-Message-Protocol 定义的 `MessageBase` 对象进行封装和传输。`Seg` 对象作为通用信息单元，用于承载用户消息内容、平台通知详情以及核心下发的动作指令。

## 2.核心数据结构

### 2.1. `MessageBase` 对象

所有交互的顶层载体。其结构和概念参考了 `maim_message` 库中的 `MessageBase` 对象，但为 AIcarus-Message-Protocol 独立定义。

-   **`message_info` (`BaseMessageInfo`)**: 包含消息的元数据和上下文。
    -   `platform` (str): 来源或目标平台的标识符 (例如："qq", "napcat", "wechat")。
    -   `bot_id` (Optional[str]): 机器人自身的ID (例如：QQ号)。
    -   `message_id` (Optional[str]): 平台提供的原始消息ID，或由生成方生成的唯一事件ID。
    -   `time` (Optional[float]): 消息的Unix毫秒时间戳。
    -   `group_info` (Optional[`GroupInfo`]): 相关的群组信息。如果存在，通常表示事件发生在群聊中。
    -   `user_info` (Optional[`UserInfo`]): 相关的用户信息（如发送者、操作者、事件主体）。
    -   `format_info` (Optional[`FormatInfo`]): 格式信息，可选。 (结构待定义)
    -   `template_info` (Optional[`TemplateInfo`]): 模板信息，可选。 (结构待定义)
    -   **`interaction_purpose` (Optional[str])**: **[新增约定字段]** 用于明确此 `MessageBase` 对象的整体意图。建议值：
        -   `"user_message"`: 表示由用户产生的消息，由 Adapter 发往 Core。
        -   `"platform_notification"`: 表示由平台产生的事件通知，由 Adapter 发往 Core。
        -   `"core_action"`: 表示由 Core 发出的动作指令，由 Core 发往 Adapter。
        -   `"action_response"`: (可选) 表示 Adapter 对 `core_action` 的执行结果反馈，由 Adapter 发往 Core。
    -   `additional_config` (Optional[dict]): 用于传递其他自定义元数据或特定于类型的配置。

-   **`message_segment` (`Seg`)**: 承载具体内容。通常是一个 `type="seglist"` 的 `Seg` 对象，其 `data` 字段是一个包含一个或多个具体 `Seg` 对象的列表。

-   **`raw_message` (Optional[str])**: 原始消息字符串，可选，主要用于调试或特殊处理。

### 2.2. `Seg` 对象 (通用信息单元)

AIcarus-Message-Protocol 定义的 `Seg` 对象是构成消息内容、通知详情和动作指令的基本单元。其结构和概念参考了 `maim_message` 库中的 `Seg` 对象。

-   **`type` (str)**: 字符串，用于区分 `Seg` 的类型和用途。
    -   对于用户消息内容：如 `"text"`, `"image"`, `"face"`, `"at"`, `"reply"` 等。
    -   对于平台通知：建议使用 `"notification:[event_name]"` 格式，如 `"notification:group_member_increase"`。
    -   对于核心动作：建议使用 `"action:[action_name]"` 格式，如 `"action:send_message"`。
-   **`data` (Union[str, List[Seg], Dict[str, Any]])**: 承载具体数据。
    -   对于简单的文本类 `Seg` (如 `"text"`)，`data` 是字符串。
    -   对于 `"seglist"` 类型的 `Seg`，`data` 是一个 `List[Seg]`。
    -   **[约定]** 对于表示**平台通知详情**和**核心动作参数**的 `Seg`，其 `data` 字段应为一个**字典 `Dict[str, Any]`**，包含该通知或动作所需的结构化参数。

### 2.3. 辅助数据结构 (AIcarus-Message-Protocol 定义)

-   **`UserInfo`**:
    -   `platform` (Optional[str])
    -   `user_id` (Optional[str])
    -   `user_nickname` (Optional[str])
    -   `user_cardname` (Optional[str]) (群名片)
    -   `user_titlename` (Optional[str]) (群头衔)
-   **`GroupInfo`**:
    -   `platform` (Optional[str])
    -   `group_id` (Optional[str])
    -   `group_name` (Optional[str])
-   **`BaseMessageInfo`**: (对应 `MessageBase.message_info` 的结构)
    -   (包含2.1中列出的所有 `message_info` 的子字段)

## 3. 交互类型详解

### 3.1. 用户消息 (Adapter -> Core)

-   `MessageBase.message_info.interaction_purpose = "user_message"`
-   `MessageBase.message_segment` 包含描述用户发送内容的一个或多个 `Seg` 对象。

**常见 `Seg` 类型 (用于消息内容):**

* **`Seg(type="text", data="文本内容")`**
* **`Seg(type="image", data={"url": "图片URL", "file_id": "可选文件ID", "base64": "可选Base64数据"})`**
* **`Seg(type="face", data="表情ID或代码")`** (QQ原生表情)
* **`Seg(type="at", data={"user_id": "被@用户ID", "display_name": "可选，被@时显示的名称"})`**
* **`Seg(type="reply", data={"message_id": "被回复的平台消息ID"})`**
* **`Seg(type="voice", data={"url": "语音URL", "file_id": "...", "duration_ms": 10000})`**
* **`Seg(type="file", data={"url": "文件URL", "name": "文件名", "size": 1024})`**
* **`Seg(type="location", data={"latitude": 30.0, "longitude": 120.0, "address": "详细地址", "title": "位置标题"})`**
* **`Seg(type="share", data={"url": "分享链接", "title": "分享标题", "content": "分享描述", "image_url": "可选分享图"})`**
* ... 其他平台支持的消息段类型。

**示例 (Adapter -> Core): 用户在群聊发送 "你好 @张三 [图片]"**

```json
{
  "message_info": {
    "platform": "qq",
    "bot_id": "10001",
    "message_id": "qq_msg_789",
    "time": 1678886400123,
    "interaction_purpose": "user_message",
    "group_info": {
      "platform": "qq",
      "group_id": "group123",
      "group_name": "测试群"
    },
    "user_info": {
      "platform": "qq",
      "user_id": "user_sender_456",
      "user_nickname": "李四",
      "user_cardname": "群里的李四"
    }
  },
  "message_segment": {
    "type": "seglist",
    "data": [
      { "type": "text", "data": "你好 " },
      { "type": "at", "data": { "user_id": "user_zhangsan_001", "display_name": "@张三" } },
      { "type": "text", "data": " " },
      { "type": "image", "data": { "url": "[http://example.com/image.jpg](http://example.com/image.jpg)" } }
    ]
  },
  "raw_message": "你好 @张三 [CQ:image,file=[http://example.com/image.jpg](http://example.com/image.jpg)]"
}
```

### 3.2. 平台通知 (Adapter -> Core)

-   `MessageBase.message_info.interaction_purpose = "platform_notification"`
-   `MessageBase.message_segment` 包含描述平台事件详情的一个 `Seg` 对象。
-   `Seg.type` 格式: `"notification:[event_name]"`
-   `Seg.data` (dict): 包含通知相关的结构化参数。

**常见通知 `Seg` 类型:**

* **`Seg(type="notification:group_member_increase", data={...})`**
    * `target_user_info` (Dict): 加入群的成员信息 (UserInfo 结构)。
    * `operator_user_info` (Optional[Dict]): 操作者信息 (如邀请人) (UserInfo 结构)。
    * `join_type` (Optional[str]): 加入方式 (e.g., "invited", "approved", "direct_join")。
* **`Seg(type="notification:group_member_decrease", data={...})`**
    * `target_user_info` (Dict): 离开/被踢成员信息 (UserInfo 结构)。
    * `operator_user_info` (Optional[Dict]): 操作者信息 (如踢人管理员) (UserInfo 结构)。
    * `reason` (Optional[str]): 原因 (e.g., "kicked", "left_voluntarily")。
* **`Seg(type="notification:group_message_recalled", data={...})`**
    * `recalled_message_id` (str): 被撤回的平台消息ID。
    * `operator_user_info` (Dict): 操作者信息 (UserInfo 结构)。
* **`Seg(type="notification:friend_request", data={...})`**
    * `source_user_info` (Dict): 发起好友请求的用户信息 (UserInfo 结构)。
    * `request_message` (Optional[str]): 好友请求附带的消息。
    * `request_id` (str): 平台提供的请求标识，用于后续处理。
* **`Seg(type="notification:group_admin_changed", data={...})`**
    * `target_user_info` (Dict): 被设置/取消管理员的用户信息 (UserInfo 结构)。
    * `action_type` (str): "set_admin" | "unset_admin"。
    * `operator_user_info` (Optional[Dict]): 操作者信息 (群主) (UserInfo 结构)。

**示例 (Adapter -> Core): 用户 "王五" 被管理员 "赵六" 移出群聊 "group123"**

```json
{
  "message_info": {
    "platform": "qq",
    "bot_id": "10001",
    "message_id": "event_id_abc", // 事件唯一ID
    "time": 1678886400234,
    "interaction_purpose": "platform_notification",
    "group_info": {
      "platform": "qq",
      "group_id": "group123",
      "group_name": "测试群"
    }
  },
  "message_segment": {
    "type": "seglist",
    "data": [
      {
        "type": "notification:group_member_decrease",
        "data": {
          "target_user_info": { "platform": "qq", "user_id": "user_wangwu_789", "user_nickname": "王五" },
          "operator_user_info": { "platform": "qq", "user_id": "user_zhaoliu_101", "user_nickname": "赵六" },
          "reason": "kicked"
        }
      }
    ]
  }
}
```

### 3.3. 核心动作 (Core -> Adapter)

-   `MessageBase.message_info.interaction_purpose = "core_action"`
-   `MessageBase.message_segment` 包含一个或多个描述核心希望执行的动作的 `Seg` 对象。
-   `Seg.type` 格式: `"action:[action_name]"`
-   `Seg.data` (dict): 包含执行该动作所需的结构化参数。
-   Adapter 执行动作后，**可选地**可以通过 `interaction_purpose = "action_response"` 将执行结果反馈给 Core。

**常见动作 `Seg` 类型:**

* **`Seg(type="action:send_message", data={...})`**
    * `segments` (List[Dict]): 要发送的消息段列表 (每个元素是 `Seg.to_dict()` 的结果)。
    * `target_user_id` (Optional[str]): 如果是私聊，指定接收用户ID。
    * `target_group_id` (Optional[str]): 如果是群聊，指定接收群组ID。 (通常此信息已在 `MessageBase.message_info.group_info` 或 `user_info` 中提供，这里可作为补充或覆盖)
    * `reply_to_message_id` (Optional[str]): 可选，回复某条平台消息的ID。
* **`Seg(type="action:delete_message", data={...})`** (撤回消息)
    * `target_message_id` (str): 要撤回的平台消息ID。
* **`Seg(type="action:kick_user", data={...})`**
    * `target_user_id` (str): 要踢出的用户ID。
    * `target_group_id` (str): 从哪个群踢出 (通常此信息已在 `MessageBase.message_info.group_info` 中)。
    * `reason` (Optional[str]): 踢人理由。
    * `block_user` (Optional[bool]): 是否同时拉黑 (默认为 `False`)。
* **`Seg(type="action:mute_user", data={...})`** (禁言)
    * `target_user_id` (str): 要禁言的用户ID。
    * `target_group_id` (str): 在哪个群禁言。
    * `duration_seconds` (int): 禁言时长 (秒)。0 表示解除禁言。
* **`Seg(type="action:set_group_card", data={...})`** (修改群名片)
    * `target_user_id` (str): 要修改名片的用户ID (通常是机器人自己或被授权修改他人)。
    * `target_group_id` (str): 在哪个群修改。
    * `card` (str): 新的群名片内容。空字符串通常表示删除群名片。
* **`Seg(type="action:handle_friend_request", data={...})`**
    * `request_id` (str): 平台提供的原始好友请求ID。
    * `approve` (bool): `True` 表示同意，`False` 表示拒绝。
    * `remark` (Optional[str]): 同意后的备注名。
* **`Seg(type="action:handle_group_invite_or_join_request", data={...})`**
    * `request_id` (str): 平台提供的原始请求ID。
    * `approve` (bool): `True` 表示同意，`False` 表示拒绝/忽略。
    * `reason` (Optional[str]): 拒绝理由。
* **`Seg(type="action:get_user_info", data={"target_user_id": "str"})`**
    * Adapter 收到后，应获取用户信息，并通过 `interaction_purpose="platform_notification"`，类型为 `notification:user_info_response` (自定义) 将结果返回给 Core。
* **`Seg(type="action:get_group_info", data={"target_group_id": "str"})`**
    * Adapter 收到后，应获取群信息，并通过 `notification:group_info_response` 返回。
* **`Seg(type="action:get_group_member_list", data={"target_group_id": "str"})`**
    * Adapter 收到后，应获取群成员列表，并通过 `notification:group_member_list_response` 返回。

**示例 (Core -> Adapter): 机器人回复用户消息，并在群 "group123" 中踢出用户 "bad_user_007"**

```json
{
  "message_info": {
    "platform": "qq",
    "bot_id": "10001",
    "message_id": "core_action_xyz", // 核心生成的动作ID
    "time": 1678886400345,
    "interaction_purpose": "core_action",
    "group_info": { // 默认的动作执行上下文
      "platform": "qq",
      "group_id": "group123"
    }
  },
  "message_segment": {
    "type": "seglist",
    "data": [
      {
        "type": "action:send_message",
        "data": {
          "segments": [
            { "type": "reply", "data": { "message_id": "qq_msg_789" } }, // 回复原始消息
            { "type": "text", "data": "已收到您的反馈。" }
          ]
        }
      },
      {
        "type": "action:kick_user",
        "data": {
          "target_user_id": "bad_user_007",
          "reason": "发布不当内容"
        }
      }
    ]
  }
}
```

### 3.4. 动作响应 (Adapter -> Core) (可选)

-   `MessageBase.message_info.interaction_purpose = "action_response"`
-   `MessageBase.message_info.message_id` 应与对应的 `core_action` 的 `message_id` 相关联，方便追踪。
-   `MessageBase.message_segment` 包含一个或多个 `Seg` 对象，描述动作执行结果。

**`Seg` 类型:**

* **`Seg(type="action_result:success", data={...})`**
    * `original_action_type` (str): 原始动作类型 (如 "action:kick_user")。
    * `details` (Optional[Dict]): 成功时的附加信息 (如 "成功发送消息的消息ID")。
* **`Seg(type="action_result:failure", data={...})`**
    * `original_action_type` (str): 原始动作类型。
    * `error_code` (Optional[int]): 平台或Adapter定义的错误码。
    * `error_message` (str): 错误描述。

## 4. 传输

所有 AIcarus-Message-Protocol 定义的 `MessageBase` 对象在序列化为字典后，通过自定义实现的通信组件 (如基于 WebSocket 或 TCP) 进行传输。

## 5. 版本控制

本协议初始版本为 v1.0.0。后续如有变更，将更新版本号。
建议在 `MessageBase.message_info.additional_config` 中加入一个 `protocol_version` 字段。