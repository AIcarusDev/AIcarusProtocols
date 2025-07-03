# **AIcarus-Message-Protocol 通信协议文档 v1.6.0**

## **1. 概述**

### 1.1. 协议宗旨

本文档定义了 **AIcarus-Message-Protocol v1.6.0**，这是一套用于聊天机器人核心 (Core) 与平台适配器 (Adapter) 之间进行通信的标准化协议。本协议旨在建立一个**高度解耦、可扩展且平台无关**的事件交换体系。

其核心设计理念是：**通过结构化的命名空间来定义事件类型，从而在协议层面实现对多平台的动态、无缝支持。**

### 1.2. 版本核心变更 (v1.6.0)

**v1.6.0** 是一个**不兼容的、革命性的版本**，它引入了“命名空间的绝对统治”原则，其核心变更如下：

1.  **`event_type` 的结构化统一**：所有事件类型（`event_type`）**必须**遵循 `{prefix}.{platform}.{...}` 的三段式（或更多段）命名空间结构。例如：`message.qq.group`、`action.discord.kick_member`。
2.  **废弃顶层 `platform` 字段**：`Event` 对象顶层的 `platform` 字段被**彻底移除**。平台信息现在完全由 `event_type` 字符串的第二部分承载，成为事件身份的内在组成部分。
3.  **协议中立性**：协议库本身不再硬编码任何具体的平台名称或平台专属动作。它只定义和验证命名空间的**格式规则**，为所有平台的自定义扩展提供了无限的可能性。
4.  **对象结构简化**：伴随顶层 `platform` 字段的移除，`UserInfo` 和 `ConversationInfo` 对象也相应地移除了 `platform` 字段，使其成为更纯粹的数据载体。

## **2. 核心数据结构**

### 2.1. `Event` 对象 (v1.6.0)

所有交互的顶层载体，其结构已被净化和简化。

*   **`event_id` (str)**: 事件包装对象的唯一标识符 (例如：由Adapter生成的UUID)，用于追踪和调试。
*   **`event_type` (str)**: 描述事件类型的字符串，**必须**采用点分层级结构。
    *   **命名空间规范**: `{prefix}.{platform}.{description}`
        *   **`prefix`**: 事件的基础分类。必须是以下之一：`message`, `notice`, `request`, `action`, `action_response`, `meta`。
        *   **`platform`**: 产生或目标平台的唯一标识符，例如 `qq`, `discord`, `wechat`, `system`。
        *   **`description`**: 对事件具体内容的描述，可包含多级，例如 `group.normal` 或 `conversation.member_increase`。
*   **`time` (float)**: 事件发生的Unix毫秒时间戳。
*   **`bot_id` (str)**: 机器人自身在该平台上的ID。
*   **`user_info` (Optional[`UserInfo`])**: 与事件最直接相关的用户信息。详见 2.2节。
*   **`conversation_info` (Optional[`ConversationInfo`])**: 事件发生的会话上下文信息。详见 2.3节。
*   **`content` (List[`Seg`])**: 事件的具体内容，表现为一个 `Seg` 对象列表。详见 2.4节。
*   **`raw_data` (Optional[str])**: 原始事件的字符串表示 (例如：平台推送的JSON原文)，可选，主要用于调试或特殊处理。

### 2.2. `UserInfo` 对象 (v1.6.0)

用于描述用户信息。`platform` 字段已被移除。

```json
{
  "user_id": "Optional[str]",
  "user_nickname": "Optional[str]",
  "user_cardname": "Optional[str]",
  "user_titlename": "Optional[str]",
  "permission_level": "Optional[str]",
  "role": "Optional[str]",
  "level": "Optional[str]",
  "sex": "Optional[str]",
  "age": "Optional[int]",
  "area": "Optional[str]",
  "additional_data": "Optional[Dict[str, Any]]"
}
```

### 2.3. `ConversationInfo` 对象 (v1.6.0)

用于描述会话信息。`platform` 字段已被移除。

```json
{
  "conversation_id": "str",
  "type": "str",
  "name": "Optional[str]",
  "parent_id": "Optional[str]",
  "extra": "Optional[Dict[str, Any]]"
}
```

### 2.4. `Seg` 对象 (通用信息单元)

`Seg` 对象的结构和定义保持不变，它依然是构成所有事件具体内容的原子构建块。

*   **`type` (str)**: 字符串，用于区分 `Seg` 的类型和用途 (例如: `"text"`, `"image"`, `"at"`)。
*   **`data` (Dict[str, Any])**: 承载该 `Seg` 类型的具体数据。

## **3. 事件类型详解 (`event_type` 及 `content` 结构)**

以下示例将展示在新规范下，各类事件的构造方式。

### 3.1. 用户消息 (`event_type` 前缀: `message`)

由用户发送的消息。

*   **`event_type` 示例**:
    *   `message.qq.private.friend` (来自QQ平台的好友私聊)
    *   `message.discord.channel.text` (来自Discord平台的频道文本消息)
*   **`content` 结构 (List[`Seg`])**:
    *   列表的第一个 `Seg` 对象**应当 (SHOULD)** 用于承载消息的元数据。
        *   `Seg(type="message_metadata", data={"message_id": "str", ...})`
    *   后续的 `Seg` 对象列表则代表消息的实际内容片段。

**示例: 来自QQ平台的群消息**
```json
{
  "event_id": "uuid_adapter_1",
  "event_type": "message.qq.group.normal",
  "time": 1678886400123.0,
  "bot_id": "10001",
  "user_info": {
    "user_id": "user_sender_456",
    "user_nickname": "李四"
  },
  "conversation_info": {
    "conversation_id": "group123",
    "type": "group",
    "name": "AIcarus淫乱派对"
  },
  "content": [
    { "type": "message_metadata", "data": { "message_id": "platform_msg_789" } },
    { "type": "text", "data": { "text": "你好！" } }
  ]
}
```

### 3.2. 平台通知 (`event_type` 前缀: `notice`)

由平台产生的状态变更或信息通知。

*   **`event_type` 示例**:
    *   `notice.qq.group.member_increase` (QQ群成员增加)
    *   `notice.discord.channel.reaction_add` (Discord频道消息表情回应增加)
*   **`content` 结构 (List[`Seg`])**: 通常包含一个 `Seg` 对象，其 `type` 字段**可以 (MAY)** 与 `event_type` 的描述部分相同，其 `data` 字段是一个包含该通知类型所需所有参数的字典。

**示例: Discord服务器成员加入通知**
```json
{
  "event_id": "uuid_notice_1",
  "event_type": "notice.discord.guild.member_join",
  "time": 1678886400300.0,
  "bot_id": "discord_bot_id_123",
  "conversation_info": {
    "conversation_id": "guild_456",
    "type": "channel",
    "name": "欢迎频道"
  },
  "user_info": {
    "user_id": "new_discord_user_789",
    "user_nickname": "Newbie"
  },
  "content": [
    {
      "type": "notice.guild.member_join",
      "data": {
        "join_timestamp": "2023-03-15T12:05:00Z"
      }
    }
  ]
}
```

### 3.3. 平台请求 (`event_type` 前缀: `request`)

由平台产生的、需要机器人明确响应的请求。

*   **`event_type` 示例**:
    *   `request.qq.friend.add` (收到QQ好友添加请求)
    *   `request.wechat.group.join_invite` (收到微信群聊邀请)

**示例: 收到QQ加好友请求**
```json
{
  "event_id": "uuid_request_1",
  "event_type": "request.qq.friend.add",
  "time": 1678886400400.0,
  "bot_id": "10001",
  "user_info": {
    "user_id": "potential_friend_007",
    "user_nickname": "小明"
  },
  "content": [
    {
      "type": "request.friend.add",
      "data": {
        "comment": "你好，我是小明！",
        "request_flag": "flag_for_qq_friend_request_abc"
      }
    }
  ]
}
```

### 3.4. 核心动作 (`event_type` 前缀: `action`)

由Core发起，指示Adapter执行的动作。

*   **`event_type` 示例**:
    *   `action.qq.message.send` (指示QQ适配器发送消息)
    *   `action.wechat.user.call` (指示微信适配器打电话)

**示例: Core指示Adapter在微信上打电话**
```json
{
  "event_id": "core_action_uuid_1",
  "event_type": "action.wechat.user.call",
  "time": 1678886400500.0,
  "bot_id": "wechat_bot_xyz",
  "user_info": { "user_id": "target_wechat_user_123" },
  "content": [
    {
      "type": "call",
      "data": {
        "video": false,
        "timeout_seconds": 60
      }
    }
  ]
}
```

### 3.5. 动作响应 (`event_type` 前缀: `action_response`)

Adapter对Core发起的`action.*`的执行结果进行反馈。

*   **`event_type` 示例**:
    *   `action_response.qq.success`
    *   `action_response.wechat.failure`

**示例: 微信打电话动作执行失败的响应**
```json
{
  "event_id": "adapter_response_uuid_1",
  "event_type": "action_response.wechat.failure",
  "time": 1678886400700.0,
  "bot_id": "wechat_bot_xyz",
  "content": [
    {
      "type": "action_response.failure",
      "data": {
        "original_event_id": "core_action_uuid_1",
        "original_action_type": "action.wechat.user.call",
        "message": "对方已拒接或无应答。"
      }
    }
  ]
}
```

### 3.6. 元事件 (`event_type` 前缀: `meta`)

关于机器人自身或 Adapter 状态的元事件。

*   **`event_type` 示例**:
    *   `meta.qq.lifecycle.connect` (QQ适配器连接成功)
    *   `meta.system.heartbeat` (系统级心跳)

**示例: QQ适配器连接成功元事件**
```json
{
  "event_id": "adapter_meta_uuid_1",
  "event_type": "meta.qq.lifecycle.connect",
  "time": 1678886400800.0,
  "bot_id": "10001",
  "content": [
    {
      "type": "meta.lifecycle.connect",
      "data": {
        "adapter_version": "2.0.0",
        "protocol_version": "1.6.0"
      }
    }
  ]
}
```

## **4. 传输**

所有 `Event` 对象在序列化为 JSON 字符串后，通过自定义实现的通信组件 (如基于 WebSocket、TCP、HTTP 或消息队列) 进行传输。

## **5. 版本控制**

本协议当前版本为 **v1.6.0**。所有通信参与方都应能处理符合本文档规范的事件结构。