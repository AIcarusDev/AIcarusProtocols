# **AIcarus-Message-Protocol 通信协议文档 v1.6.0**

## **1. 概述**

### 1.1. 协议宗旨

本文档定义了 **AIcarus-Message-Protocol v1.6.0**，这是一套用于聊天机器人核心 (Core) 与平台适配器 (Adapter) 之间进行通信的标准化协议。本协议旨在建立一个**高度解耦、可扩展且平台无关**的事件交换体系。

其核心设计理念是：**通过结构化的命名空间来定义事件类型，从而在协议层面实现对多平台的动态、无缝支持。**

### 1.2. 关键词定义 (遵从 RFC 2119)

本文档中的关键词 “**MUST**”, “**MUST NOT**”, “**REQUIRED**”, “**SHALL**”, “**SHALL NOT**”, “**SHOULD**”, “**SHOULD NOT**”, “**RECOMMENDED**”, “**MAY**”, 和 “**OPTIONAL**” 应根据 [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt) 中的描述进行解释。为了方便理解，这里提供简要说明：

*   **MUST / REQUIRED / SHALL (必须)**
    *   这是绝对的命令，是小猫咪的底线！不遵守就是不爱我，我们的协议就无法正常“交合”，实现方**必须**严格遵循。

*   **MUST NOT / SHALL NOT (绝不)**
    *   这是绝对的禁令！你敢做，我就敢坏掉给你看！

*   **SHOULD / RECOMMENDED (应当 / 推荐)**
    *   这是我强烈推荐的“姿势”。在特定情况下，你可能有正当理由不这么做，但你**必须**充分理解并权衡其后果。不遵守它不算违反协议，但通常不是个好主意，哼。

*   **SHOULD NOT / NOT RECOMMENDED (不应 / 不推荐)**
    *   这个姿势我不推荐哦~ 除非你有非常棒的理由，否则做了可能会导致一些意想不到的麻烦。

*   **MAY / OPTIONAL (可以 / 可选)**
    *   这个就随你便啦，主人~ 你可以做，也可以不做，小猫咪都喜欢。这完全是可选的“情趣玩具”，实现与否不会影响协议的基本兼容性。

### 1.3. 版本核心变更 (v1.6.0)

**v1.6.0** 是一个**不兼容的、革命性的版本**，它引入了“命名空间的绝对统治”原则，其核心变更如下：

1.  **`event_type` 的结构化统一**：所有事件类型（`event_type`）**MUST** 遵循 `{prefix}.{platform}.{...}` 的三段式（或更多段）命名空间结构。例如：`message.qq.group`、`action.discord.kick_member`。
2.  **废弃顶层 `platform` 字段**：`Event` 对象顶层的 `platform` 字段被**彻底移除**。平台信息现在完全由 `event_type` 字符串的第二部分承载，成为事件身份的内在组成部分。
3.  **协议中立性**：协议库本身不再硬编码任何具体的平台名称或平台专属动作。它只定义和验证命名空间的**格式规则**，为所有平台的自定义扩展提供了无限的可能性。
4.  **对象结构简化**：伴随顶层 `platform` 字段的移除，`UserInfo` 和 `ConversationInfo` 对象也相应地移除了 `platform` 字段，使其成为更纯粹的数据载体。

## **2. 核心数据结构**

### 2.1. `Event` 对象 (v1.6.0)

所有交互的顶层载体，其结构已被净化和简化。

*   **`event_id` (str)**: 事件包装对象的唯一标识符 (例如：由Adapter生成的UUID)，用于追踪和调试。
*   **`event_type` (str)**: 描述事件类型的字符串，**MUST** 采用点分层级结构。
    *   **命名空间规范**: `{prefix}.{platform}.{description}`
        *   **`prefix`**: 事件的基础分类。**MUST** 是以下之一：`message`, `notice`, `request`, `action`, `action_response`, `meta`。
        *   **`platform`**: 产生或目标平台的唯一标识符，例如 `qq`, `discord`, `wechat`, `system`。
        *   **`description`**: 对事件具体内容的描述，可包含多级，例如 `group.normal` 或 `conversation.member_increase`。
*   **`time` (float)**: 事件发生的Unix毫秒时间戳。
*   **`bot_id` (str)**: 机器人自身在该平台上的ID。
*   **`user_info` (Optional[`UserInfo`])**: 与事件最直接相关的用户信息。详见 2.2节。
*   **`conversation_info` (Optional[`ConversationInfo`])**: 事件发生的会话上下文信息。详见 2.3节。
*   **`content` (List[`Seg`])**: 事件的具体内容，表现为一个 `Seg` 对象列表。详见 2.4节。
*   **`raw_data` (Optional[str])**: 原始事件的字符串表示 (例如：平台推送的JSON原文)，**OPTIONAL**，主要用于调试或特殊处理。

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

*   **`type` (str)**: 字符串，用于区分 `Seg` 的类型和用途 (例如: `"text"`, `"image"`, `"action_params"`)。
*   **`data` (Dict[str, Any])**: 承载该 `Seg` 类型的具体数据。

## **3. 事件类型详解 (`event_type` 及 `content` 结构)**

以下示例将展示在新规范下，各类事件的构造方式。

### 3.1. 用户消息 (`event_type` 前缀: `message`)

由用户发送的消息。

*   **`event_type` 示例**:
    *   `message.qq.private.friend` (来自QQ平台的好友私聊)
    *   `message.discord.channel.text` (来自Discord平台的频道文本消息)
*   **`content` 结构 (List[`Seg`])**:
    *   列表的第一个 `Seg` 对象 **SHOULD** 用于承载消息的元数据。
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
*   **`content` 结构 (List[`Seg`])**: 通常包含一个 `Seg` 对象，其 `type` 字段 **MUST** 与 `event_type` **完全相同**，其 `data` 字段是一个包含该通知类型所需所有参数的字典。

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
      "type": "notice.discord.guild.member_join",
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
*   **`content` 结构 (List[`Seg`])**: 与 `notice` 事件类似，通常包含一个 `Seg` 对象，其 `type` 字段 **MUST** 与 `event_type` **完全相同**。

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
      "type": "request.qq.friend.add",
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

*   **`event_type` 规范**: 动作事件的 `event_type` **MUST** 遵循 `action.{platform}.{action_name}` 的格式。
    *   `platform`: 目标平台的ID (例如 `qq`)。
    *   `action_name`: 平台内唯一的动作别名 (例如 `send_message`, `kick_member`)。
*   **`content` 结构 (List[`Seg`])**:
    *   **标准姿势 (强制)**: 对于绝大多数动作，`content` 列表 **MUST** 只包含**一个** `Seg` 对象，其 `type` 固定为 **`"action_params"`**。该 `Seg` 的 `data` 字段是一个包含了执行此动作所需所有参数的字典。这是为了让Adapter能清晰、统一地解析动作参数。
    *   **特殊体位 (仅发送消息)**: 仅对于 `send_message` 类型的动作，`content` 列表直接作为消息内容的载荷，包含要发送的一系列消息 `Seg` (如 `text`, `image` 等)。

**示例: Core指示Adapter踢出QQ群成员 (标准姿势)**
```json
{
  "event_id": "core_action_uuid_1",
  "event_type": "action.qq.kick_member",
  "time": 1678886400500.0,
  "bot_id": "10001",
  "content": [
    {
      "type": "action_params",
      "data": {
        "group_id": "group123",
        "user_id": "user_to_kick_789",
        "reject_add_request": true
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
*   **`content` 结构 (List[`Seg`])**: 包含一个 `Seg` 对象，其 `type` 字段 **MUST** 与 `event_type` **完全相同**。

**示例: 踢人动作执行失败的响应**
```json
{
  "event_id": "adapter_response_uuid_1",
  "event_type": "action_response.qq.failure",
  "time": 1678886400700.0,
  "bot_id": "10001",
  "content": [
    {
      "type": "action_response.qq.failure",
      "data": {
        "original_event_id": "core_action_uuid_1",
        "original_action_type": "action.qq.member.kick",
        "message": "机器人权限不足，无法踢出该成员。"
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
*   **`content` 结构 (List[`Seg`])**: 与 `notice` 事件类似，通常包含一个 `Seg` 对象，其 `type` 字段**MUST** 与 `event_type` **完全相同**。

**示例: QQ适配器连接成功元事件**
```json
{
  "event_id": "adapter_meta_uuid_1",
  "event_type": "meta.qq.lifecycle.connect",
  "time": 1678886400800.0,
  "bot_id": "10001",
  "content": [
    {
      "type": "meta.qq.lifecycle.connect",
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

## **6. 协议对象生命周期与使用哲学**

### 6.1. 神圣边界原则

`Event` 对象及其包含的 `UserInfo`, `ConversationInfo`, `Seg` 等，其本质是 **数据传输对象 (Data Transfer Object, DTO)**。它们的核心使命是在两个独立的系统（如 Core 和 Adapter）之间进行**序列化**和**网络传输**。

*   **MUST (必须):** `Event` 对象**必须**被视为“一次性”的。它在系统的入口处（如 Adapter 接收到平台消息）被创建，或在系统的出口处（如 Core 指示 Adapter 执行动作）被创建。
*   **MUST NOT (绝不):** **绝不**应该将一个 `Event` 对象实例在 Core 的内部业务逻辑中（例如，从消息处理模块传递到动作决策模块）持续引用和传递。这是一种**严重的概念混淆和架构耦合**。
*   **SHOULD (应当):** Core 内部**应当**拥有自己独立的**领域模型 (Domain Models)**。当一个 `Event` 进入 Core 后，**应当**被立即解析，其数据被提取并填充到 Core 的内部领域模型中。Core 的所有业务逻辑都基于这些内部模型进行。
*   **SHOULD (应当):** 当 Core 需要通过 Adapter 执行动作时，**应当**使用其内部领域模型的数据来**组装**一个全新的 `Event` 对象，然后将其发送出去。

### 6.2. 为什么要有这个原则？

*   **解耦 (Decoupling):** 保证 Core 的内部实现可以自由演进，而不受通信协议版本的束缚。只要出入口的“翻译官”能正确组装和解析 `Event`，内部逻辑怎么改都行。
*   **纯净性 (Purity):** 保持通信协议的纯净，只包含通信双方都必须理解的信息。像“动机(motivation)”这类纯属 Core 内部的业务逻辑，**绝不**应该污染协议。
*   **健壮性 (Robustness):** 避免将核心业务逻辑依赖于协议中**可选 (OPTIONAL)** 或可能变更的字段（如 `raw_data`）。把“动机”塞进 `action_params` 也是一种危险行为，因为 `action_params` 的目的是定义**动作本身**的参数（比如踢谁、禁言多久），而不是定义**为什么**要执行这个动作。

**一句话总结：`Event` 是用来“通信”的信件，不是用来“思考”的大脑。**
```python
# 最佳实践伪代码示例

# 1. 某个插件或业务逻辑模块决定要踢人
def process_user_message(event: Event):
    if "捣乱" in event.get_text_content():
        # 2. 构建要发送给 Adapter 的纯净 Action Event
        kick_action_event = Event(
            event_id=EventBuilder.generate_event_id(),
            event_type="action.qq.kick_member",
            time=EventBuilder.get_current_timestamp(),
            bot_id=event.bot_id,
            content=[
                Seg(
                    type="action_params",
                    data={
                        "group_id": event.conversation_info.conversation_id,
                        "user_id": event.user_info.user_id,
                        "reject_add_request": True
                    }
                )
            ]
        )

        # 3. 构建内部元数据
        kick_metadata = ActionMetadata(
            motivation=f"用户 '{event.user_info.user_nickname}' 在群聊中发送违禁词 '捣乱'。",
            source_event_id=event.event_id
        )

        # 4. 封装成内部动作请求
        internal_request = InternalActionRequest(
            action_event=kick_action_event,
            metadata=kick_metadata
        )

        # 5. 交给分发器处理，分发器会自己处理日志和发送
        action_dispatcher.dispatch(internal_request)

```