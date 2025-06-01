# AIcarus-Message-Protocol 通信协议文档 v1.2.0

## 1. 概述

本文档定义了聊天机器人核心 (Core) 与平台适配器 (Adapter) 之间，基于 AIcarus-Message-Protocol 的通信协议。该协议旨在提供一套标准化的消息结构和交互模式，以实现组件解耦、易于扩展和多平台支持。

所有通信均通过 AIcarus-Message-Protocol 定义的 `MessageBase` 对象进行封装和传输。`Seg` 对象作为通用信息单元，用于承载用户消息内容、平台通知详情、平台请求、元事件以及核心下发的动作指令。

**版本说明:** v1.2.0 - 本版本基于对 OneBot v11 等现有协议的分析，全面增强了 `UserInfo` 结构，细化并扩充了平台通知类型，并正式引入了 `platform_request` (平台请求) 和 `platform_meta` (平台元事件) 两种交互意图，以实现更全面的事件捕获和处理能力。

## 2. 核心数据结构

### 2.1. `MessageBase` 对象

所有交互的顶层载体。

* **`message_info` (`BaseMessageInfo`)**: 包含消息的元数据和上下文。详见 2.2节。
* **`message_segment` (`Seg`)**: 承载具体内容。通常是一个 `type="seglist"` 的 `Seg` 对象，其 `data` 字段是一个包含一个或多个具体 `Seg` 对象的列表。详见 2.3节。
* **`raw_message` (Optional[str])**: 原始消息字符串或事件的原始数据结构（例如JSON字符串），可选，主要用于调试或特殊处理。

### 2.2. `BaseMessageInfo` 对象 (用于 `MessageBase.message_info`)

此对象包含了所有交互类型共享的元数据。根据 `interaction_purpose` 的不同，可能还会包含一些特有的字段。

**通用字段:**

* `platform` (str): 来源或目标平台的标识符 (例如："qq", "napcat", "wechat", "onebot_v11")。
* `bot_id` (str): 机器人自身的ID (例如：QQ号, OneBot `self_id`)。
* `message_id` (Optional[str]): 平台提供的原始消息ID，或由生成方生成的唯一事件ID。对于某些通知或请求，此字段可能不存在或有特殊含义。
* `time` (float): 事件发生的Unix毫秒时间戳。
* `group_info` (Optional[`GroupInfo`]): 如果事件与特定群组相关，则包含此群组信息。详见 2.5节。
* `user_info` (Optional[`UserInfo`]): 与事件相关的用户信息（如发送者、操作者、事件主体）。详见 2.4节。
* **`interaction_purpose` (str)**: 明确此 `MessageBase` 对象的整体意图。关键字段，用于区分不同类型的交互。建议值：
    * `"user_message"`: 表示由用户产生的消息。
    * `"platform_notification"`: 表示由平台产生的、通常不需要机器人直接响应的状态变更或信息通知。
    * `"platform_request"`: 表示由平台产生的、需要机器人明确响应的请求（如好友请求、加群请求）。
    * `"platform_meta"`: 表示关于机器人自身或 Adapter 状态的元事件（如生命周期、心跳）。
    * `"core_action"`: 表示由 Core 发出的、指示 Adapter 执行的动作指令。
    * `"action_response"`: (可选) 表示 Adapter 对 `core_action` 的执行结果反馈。
* `additional_config` (Optional[dict]): 用于传递其他自定义元数据或特定于类型的配置。
    * **建议固定包含 `protocol_version`**: 例如 `{"protocol_version": "1.2.0"}`，以明确当前通信使用的协议版本。

**特定于 `interaction_purpose = "user_message"` 的额外字段:**

* `message_type` (str): 消息类型，如 `"private"` (私聊), `"group"` (群聊)。(可映射 OneBot `message_type`)
* `sub_type` (Optional[str]): 消息子类型。(可映射 OneBot `sub_type`)
    * 私聊时: `"friend"` (好友), `"group"` (群临时会话), `"group_self"` (自己在群里发消息给自己), `"other"`。
    * 群聊时: `"normal"` (普通消息), `"anonymous"` (匿名消息), `"notice"` (系统提示, 如xx撤回了一条消息)。
* `font` (Optional[str]): (可选) 字体名称或ID。(可映射 OneBot `font`)
* `anonymity_info` (Optional[dict]): (可选) 如果是匿名消息 (`sub_type="anonymous"`)，包含匿名信息。
    * 例如: `{"id": "Optional[int]", "name": "str", "flag": "str"}` (可映射 OneBot `anonymous` 对象)

### 2.3. `Seg` 对象 (通用信息单元)

AIcarus-Message-Protocol 定义的 `Seg` 对象是构成消息内容、通知详情、请求参数和动作指令的基本单元。

* **`type` (str)**: 字符串，用于区分 `Seg` 的类型和用途。
    * 用户消息内容: 如 `"text"`, `"image"`, `"face"`, `"at"`, `"reply"` 等。
    * 平台通知/请求/元事件: 使用特定格式，如 `"notification:[event_name]"`, `"request:[request_name]"`, `"meta:[meta_name]"`。
    * 核心动作: 使用特定格式，如 `"action:[action_name]"`。
    * 动作响应: 使用特定格式，如 `"action_result:[status]"`。
* **`data` (Union[str, List[Seg], Dict[str, Any]])**: 承载具体数据。
    * 对于简单的文本类 `Seg` (如 `"text"`)，`data` 是字符串。
    * 对于 `"seglist"` 类型的 `Seg` (通常作为 `MessageBase.message_segment` 的直接子对象)，`data` 是一个 `List[Seg]`。
    * 对于表示平台通知详情、请求参数、元事件参数、核心动作参数或动作响应详情的 `Seg`，其 `data` 字段通常为一个字典 `Dict[str, Any]`，包含该事件/动作所需的结构化参数。

### 2.4. `UserInfo` 对象

用于描述用户信息。

```json
{
  "platform": "Optional[str]",
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
**说明:**
* `additional_data`: 用于存储平台特有的、协议未明确定义的其他用户相关信息。

### 2.5. `GroupInfo` 对象

用于描述群组信息。

```json
{
  "platform": "Optional[str]",
  "group_id": "Optional[str]",
  "group_name": "Optional[str]"
}
```

## 3. 交互类型详解

### 3.1. 用户消息 (`interaction_purpose = "user_message"`)

由用户发送的消息，Adapter 捕获后转换为此结构发往 Core。

**`MessageBase.message_info` 结构:** 包含通用字段以及本节 2.2 中列出的 `user_message` 特定字段 (`message_type`, `sub_type`, `font`, `anonymity_info`)。

**`MessageBase.message_segment` (`Seg`) 常见类型 (用于消息内容):**

* **`Seg(type="text", data="文本内容")`**
* **`Seg(type="image", data={"url": "Optional[str]", "file_id": "Optional[str]", "base64": "Optional[str]", "is_flash": "Optional[bool]"})`**
    * `url`: 图片链接。
    * `file_id`: 平台提供的文件ID或路径。
    * `base64`: 图片的Base64编码。
    * `is_flash`: 是否为闪照 (部分平台支持)。
* **`Seg(type="face", data={"face_id": "str", "name": "Optional[str]"})`**
    * `face_id`: 平台原生表情的ID。
    * `name`: 表情的可读名称 (如 "[呲牙]")。
* **`Seg(type="at", data={"user_id": "str", "display_name": "Optional[str]"})`**
    * `user_id`: 被@用户的ID。`"all"` 表示@全体成员。
    * `display_name`: @时显示的名称 (如 "@张三")。
* **`Seg(type="reply", data={"message_id": "str"})`**
    * `message_id`: 被回复的平台消息ID。
* **`Seg(type="voice", data={"url": "Optional[str]", "file_id": "Optional[str]", "base64": "Optional[str]", "duration_ms": "Optional[int]"})`**
* **`Seg(type="file", data={"url": "Optional[str]", "file_id": "Optional[str]", "name": "str", "size": "Optional[int]"})`**
* **`Seg(type="location", data={"latitude": "float", "longitude": "float", "address": "Optional[str]", "title": "Optional[str]"})`**
* **`Seg(type="share", data={"url": "str", "title": "str", "content": "Optional[str]", "image_url": "Optional[str]"})`** (分享链接)
* **`Seg(type="json_card", data={"content": "str"})`** (JSON 卡片消息，`content` 为 JSON 字符串)
* **`Seg(type="xml_card", data={"content": "str"})`** (XML 卡片消息，`content` 为 XML 字符串)
* ... 其他平台特有的消息段类型，适配器应尽可能转换为通用类型或提供平台特定类型。

**示例 (Adapter -> Core): 用户在群聊发送 "你好 @张三 [图片]"**

```json
{
  "message_info": {
    "platform": "qq",
    "bot_id": "10001",
    "message_id": "platform_msg_789",
    "time": 1678886400123.0,
    "group_info": {
      "platform": "qq",
      "group_id": "group123",
      "group_name": "测试群"
    },
    "user_info": {
      "platform": "qq",
      "user_id": "user_sender_456",
      "user_nickname": "李四",
      "user_cardname": "群里的李四",
      "permission_level": "member",
      "role": "member",
      "additional_data": {"constellation": "aries"}
    },
    "interaction_purpose": "user_message",
    "message_type": "group",
    "sub_type": "normal",
    "additional_config": {"protocol_version": "1.2.0"}
  },
  "message_segment": {
    "type": "seglist",
    "data": [
      { "type": "text", "data": "你好 " },
      { "type": "at", "data": { "user_id": "user_zhangsan_001", "display_name": "@张三" } },
      { "type": "text", "data": " " },
      { "type": "image", "data": { "url": "[http://example.com/image.jpg](http://example.com/image.jpg)", "file_id": "qq_image_abc" } }
    ]
  },
  "raw_message": "你好 @张三 [CQ:image,file=qq_image_abc,url=[http://example.com/image.jpg](http://example.com/image.jpg)]"
}
```

### 3.2. 平台通知 (`interaction_purpose = "platform_notification"`)

由平台产生的、通常不需要机器人直接响应的状态变更或信息通知。

**`MessageBase.message_info.user_info`**: 通常代表与通知直接相关的用户（如操作者、被操作者或事件主体）。

**`Seg.type` 命名约定**: `notification:[onebot_notice_type]_[optional_onebot_sub_type]` 或更具体的描述性名称。
**`MessageBase.message_segment`**: 通常只包含一个描述通知详情的 `Seg` 对象。

**常见通知 `Seg` 类型及其 `data` 结构:**

* **`Seg(type="notification:group_member_increase", data={...})`** (群成员增加)
    * `target_user_info` (UserInfo): 加入群的成员信息。
    * `operator_user_info` (Optional[UserInfo]): 操作者信息 (如邀请人、批准管理员)。
    * `join_type` (str): 加入方式 (例如: `"approve"` (管理员同意), `"invite"` (被邀请))。
* **`Seg(type="notification:group_member_decrease", data={...})`** (群成员减少)
    * `target_user_info` (UserInfo): 离开/被踢成员信息。
    * `operator_user_info` (Optional[UserInfo]): 操作者信息 (如踢人管理员)。
    * `reason` (str): 原因 (例如: `"leave"` (主动退群), `"kick"` (被踢), `"kick_me"` (机器人被踢))。
* **`Seg(type="notification:group_message_recalled", data={...})`** (群消息撤回)
    * `recalled_message_id` (str): 被撤回的平台消息ID。
    * `recalled_message_sender_info` (Optional[UserInfo]): 被撤回消息的发送者信息。
    * `operator_user_info` (UserInfo): 执行撤回操作的用户信息。
* **`Seg(type="notification:friend_message_recalled", data={...})`** (好友消息撤回)
    * `recalled_message_id` (str): 被撤回的平台消息ID。
    * `friend_user_info` (UserInfo): 好友的用户信息 (即消息对话的另一方)。
    * `operator_user_info` (UserInfo): 执行撤回操作的用户信息 (可能是机器人自己或好友)。
* **`Seg(type="notification:group_admin_changed", data={...})`** (群管理员变更)
    * `target_user_info` (UserInfo): 被设置/取消管理员的用户信息。
    * `action_type` (str): `"set"` (设为管理员) | `"unset"` (取消管理员)。
    * `operator_user_info` (Optional[UserInfo]): 操作者信息 (通常是群主)。
* **`Seg(type="notification:group_file_uploaded", data={...})`** (群文件上传)
    * `file_info` (dict): 文件信息。
        * `id` (str): 文件ID。
        * `name` (str): 文件名。
        * `size` (int): 文件大小 (字节)。
        * `busid` (Optional[Any]): 平台特定的业务ID (如QQ群文件的 `busid`)。
    * `uploader_user_info` (UserInfo): 上传文件的用户信息。
* **`Seg(type="notification:group_member_banned", data={...})`** (群成员禁言/解禁)
    * `target_user_info` (UserInfo): 被禁言/解禁的成员信息。
    * `operator_user_info` (Optional[UserInfo]): 操作者信息 (管理员)。
    * `duration_seconds` (int): 禁言时长 (秒)。0 表示解除禁言。
    * `ban_type` (str): `"ban"` (禁言) | `"lift_ban"` (解除禁言)。
* **`Seg(type="notification:friend_added_successfully", data={...})`** (好友添加成功)
    * `friend_user_info` (UserInfo): 新添加的好友的用户信息。
* **`Seg(type="notification:group_card_changed", data={...})`** (群名片变更)
    * `target_user_info` (UserInfo): 名片被更改的用户信息。
    * `new_card_name` (str): 新的群名片。
    * `old_card_name` (str): 旧的群名片。
    * `operator_user_info` (Optional[UserInfo]): 操作者信息 (可能是用户自己或管理员)。
* **`Seg(type="notification:poke_received", data={...})`** (戳一戳)
    * `sender_user_info` (UserInfo): 发起戳一戳的用户信息。
    * `target_user_info` (UserInfo): 被戳的用户信息 (通常是机器人自己)。
    * `context_type` (Optional[str]): 戳一戳发生的上下文，如 `"group"` 或 `"private"`。
* **`Seg(type="notification:lucky_king_awarded", data={...})`** (群红包运气王)
    * `lucky_user_info` (UserInfo): 运气王的用户信息。
    * `red_envelope_sender_user_info` (Optional[UserInfo]): 红包发送者的用户信息。
    * `context_id` (Optional[str]): 相关上下文ID (例如红包ID)。
* **`Seg(type="notification:group_honor_changed", data={...})`** (群成员荣誉变更，如龙王、群聊之火)
    * `target_user_info` (UserInfo): 获得/失去荣誉的用户信息。
    * `honor_type_name` (str): 荣誉类型名称 (例如: `"talkative"`, `"performer"`, `"emotion"`)。
    * `action` (str): `"add"` (获得) | `"remove"` (失去)。
    * `description` (Optional[str]): 荣誉的描述文本。
* **`Seg(type="notification:message_reactions_updated", data={...})`** (消息表情回应更新)
    * `target_message_id` (str): 被回应的消息ID。
    * `acting_user_info` (Optional[UserInfo]): 最近一个做出回应/改变回应的用户信息。
    * `reactions` (List[dict]): 当前消息的所有回应列表。
        * `emoji_id` (str): 表情代码或ID。
        * `emoji_name` (Optional[str]): 表情名称。
        * `count` (int): 该表情的回应数量。
* **`Seg(type="notification:message_marked_as_essence", data={...})`** (消息被标记/取消标记为精华)
    * `target_message_id` (str): 被操作的消息ID。
    * `target_message_sender_info` (Optional[UserInfo]): 被操作消息的发送者信息。
    * `operator_user_info` (UserInfo): 执行标记/取消标记操作的管理员信息。
    * `action` (str): `"add"` (添加为精华) | `"remove"` (取消精华)。

**示例 (Adapter -> Core): 群文件上传通知**

```json
{
  "message_info": {
    "platform": "qq",
    "bot_id": "10001",
    "message_id": "event_id_upload_xyz",
    "time": 1678886400234.0,
    "group_info": {
      "platform": "qq",
      "group_id": "group123",
      "group_name": "测试群"
    },
    "user_info": {
      "platform": "qq",
      "user_id": "uploader_789",
      "user_nickname": "文件上传君",
      "permission_level": "member"
    },
    "interaction_purpose": "platform_notification",
    "additional_config": {"protocol_version": "1.2.0"}
  },
  "message_segment": {
    "type": "seglist",
    "data": [
      {
        "type": "notification:group_file_uploaded",
        "data": {
          "file_info": {
            "id": "file_abc_123",
            "name": "重要文档.docx",
            "size": 102400,
            "busid": 102
          },
          "uploader_user_info": {
            "platform": "qq",
            "user_id": "uploader_789",
            "user_nickname": "文件上传君"
          }
        }
      }
    ]
  }
}
```

### 3.3. 平台请求 (`interaction_purpose = "platform_request"`)

由平台产生的、需要机器人明确响应的请求。

**`MessageBase.message_info.user_info`**: 通常代表请求的发起者。
**`MessageBase.message_segment`**: 通常只包含一个描述请求详情的 `Seg` 对象。

**`Seg.type` 命名约定**: `request:[request_type]_[optional_sub_type]`

**常见请求 `Seg` 类型及其 `data` 结构:**

* **`Seg(type="request:friend_add", data={...})`** (好友添加请求)
    * `source_user_info` (UserInfo): 发起好友请求的用户信息。
    * `comment` (Optional[str]): 验证消息。
    * `request_flag` (str): 用于响应此请求的唯一标识 (对应 OneBot `flag`)。**此字段必须包含。**
* **`Seg(type="request:group_join_application", data={...})`** (用户申请加入群聊)
    * `source_user_info` (UserInfo): 申请加群的用户信息。
    * `comment` (Optional[str]): 加群验证消息。
    * `request_flag` (str): 用于响应此请求的唯一标识。**此字段必须包含。**
    * `inviter_user_info` (Optional[UserInfo]): 如果是通过邀请链接等方式，邀请人的信息。
* **`Seg(type="request:group_invite_received", data={...})`** (机器人被邀请加入群聊)
    * `inviter_user_info` (UserInfo): 发起邀请的用户信息。
    * `request_flag` (str): 用于响应此请求的唯一标识。**此字段必须包含。**

**示例 (Adapter -> Core): 收到好友添加请求**

```json
{
  "message_info": {
    "platform": "qq",
    "bot_id": "10001",
    "message_id": "request_event_friend_add_1",
    "time": 1678886400300.0,
    "user_info": {
      "platform": "qq",
      "user_id": "potential_friend_007",
      "user_nickname": "想加好友的小明"
    },
    "interaction_purpose": "platform_request",
    "additional_config": {"protocol_version": "1.2.0"}
  },
  "message_segment": {
    "type": "seglist",
    "data": [
      {
        "type": "request:friend_add",
        "data": {
          "source_user_info": {
            "platform": "qq",
            "user_id": "potential_friend_007",
            "user_nickname": "想加好友的小明"
          },
          "comment": "你好，我是小明，想加你好友一起玩！",
          "request_flag": "flag_unique_friend_request_abc"
        }
      }
    ]
  }
}
```

### 3.4. 平台元事件 (`interaction_purpose = "platform_meta"`)

关于机器人自身或 Adapter 状态的元事件。

**`MessageBase.message_info.user_info`**: 通常不适用或为机器人自身。
**`MessageBase.message_segment`**: 通常只包含一个描述元事件详情的 `Seg` 对象。

**`Seg.type` 命名约定**: `meta:[meta_event_type]_[optional_sub_type]`

**常见元事件 `Seg` 类型及其 `data` 结构:**

* **`Seg(type="meta:lifecycle", data={...})`** (生命周期事件)
    * `lifecycle_type` (str): 生命周期类型，例如:
        * `"enable"` (适配器启用)
        * `"disable"` (适配器禁用)
        * `"connect"` (适配器连接到平台成功)
        * `"disconnect"` (适配器与平台断开连接)
    * `details` (Optional[dict]): 额外详情。
* **`Seg(type="meta:heartbeat", data={...})`** (心跳事件)
    * `status_object` (dict): 平台或Adapter的当前状态对象 (可映射 OneBot `status`)。
    * `interval_ms` (Optional[int]): 心跳间隔 (毫秒)。
    * `is_online` (Optional[bool]): 机器人是否在线。

**示例 (Adapter -> Core): 适配器连接成功**

```json
{
  "message_info": {
    "platform": "qq_adapter_manager",
    "bot_id": "10001",
    "message_id": "meta_event_connect_1",
    "time": 1678886000000.0,
    "interaction_purpose": "platform_meta",
    "additional_config": {"protocol_version": "1.2.0"}
  },
  "message_segment": {
    "type": "seglist",
    "data": [
      {
        "type": "meta:lifecycle",
        "data": {
          "lifecycle_type": "connect",
          "details": {"adapter_version": "1.0.0", "platform_api_version": "v11"}
        }
      }
    ]
  }
}
```

### 3.5. 核心动作 (`interaction_purpose = "core_action"`)

由 Core 发出的、指示 Adapter 执行的动作指令。

**`MessageBase.message_info.group_info` / `user_info`**: 通常用于指定动作的目标上下文。
**`MessageBase.message_segment`**: 包含一个或多个描述核心希望执行的动作的 `Seg` 对象。

**`Seg.type` 命名约定**: `action:[action_name]`

**常见动作 `Seg` 类型及其 `data` 结构:**

* **`Seg(type="action:send_message", data={...})`**
    * `segments` (List[Dict]): 要发送的消息段列表 (每个元素是符合本协议 `Seg` 结构的字典)。
    * `target_user_id` (Optional[str]): 如果是私聊，指定接收用户ID。
    * `target_group_id` (Optional[str]): 如果是群聊，指定接收群组ID。
    * `reply_to_message_id` (Optional[str]): (可选) 回复某条平台消息的ID。
* **`Seg(type="action:delete_message", data={"target_message_id": "str"})`** (撤回消息)
* **`Seg(type="action:kick_user", data={...})`**
    * `target_user_id` (str): 要踢出的用户ID。
    * `target_group_id` (str): 从哪个群踢出。
    * `reason` (Optional[str]): 踢人理由。
    * `reject_future_requests` (Optional[bool]): 是否拒绝此人后续的加群请求 (部分平台支持)。
* **`Seg(type="action:mute_user", data={...})`** (禁言/解禁群成员)
    * `target_user_id` (str): 要操作的用户ID。
    * `target_group_id` (str): 在哪个群操作。
    * `duration_seconds` (int): 禁言时长 (秒)。0 表示解除禁言。
* **`Seg(type="action:set_group_card", data={...})`** (修改群名片)
    * `target_user_id` (str): 要修改名片的用户ID。
    * `target_group_id` (str): 在哪个群修改。
    * `card` (str): 新的群名片内容。空字符串通常表示删除群名片。
* **`Seg(type="action:handle_friend_request", data={...})`**
    * `request_flag` (str): 从对应的 `request:friend_add` 事件中获取的 `request_flag`。**此字段必须提供。**
    * `approve` (bool): `True` 表示同意，`False` 表示拒绝。
    * `remark` (Optional[str]): 同意后的备注名。
* **`Seg(type="action:handle_group_request", data={...})`** (处理加群请求/邀请)
    * `request_flag` (str): 从对应的 `request:group_join_application` 或 `request:group_invite_received` 事件中获取的 `request_flag`。**此字段必须提供。**
    * `request_type` (str): 原始请求类型，如 `"join_application"` 或 `"invite_received"`，用于适配器区分处理逻辑。
    * `approve` (bool): `True` 表示同意，`False` 表示拒绝/忽略。
    * `reason` (Optional[str]): 拒绝理由。
* **`Seg(type="action:get_user_info", data={"target_user_id": "str", "no_cache": "Optional[bool]"})`**
* **`Seg(type="action:get_group_info", data={"target_group_id": "str", "no_cache": "Optional[bool]"})`**
* **`Seg(type="action:get_group_member_list", data={"target_group_id": "str"})`**
* **`Seg(type="action:set_group_whole_ban", data={"target_group_id": "str", "enable": "bool"})`** (开启/关闭全群禁言)
* **`Seg(type="action:set_group_admin", data={"target_group_id": "str", "target_user_id": "str", "enable": "bool"})`** (设置/取消群管理员)
* **`Seg(type="action:set_group_anonymous_ban", data={"target_group_id": "str", "anonymous_flag": "str", "duration_seconds": "int"})`** (禁言群匿名用户)
* **`Seg(type="action:leave_group", data={"target_group_id": "str"})`** (机器人退出群聊)
* **`Seg(type="action:mark_message_as_read", data={"target_message_id": "str"})`** (标记消息已读)
* **`Seg(type="action:upload_group_file", data={...})`**
    * `target_group_id` (str): 上传到哪个群。
    * `file_path_or_url_or_base64` (str): 文件本地路径、URL或Base64编码。
    * `file_name` (str): 在群里显示的文件名。
    * `folder_id` (Optional[str]): (可选) 上传到群文件的哪个文件夹。
* ... 其他更多动作。

**示例 (Core -> Adapter): 同意好友请求并发送欢迎消息**

```json
{
  "message_info": {
    "platform": "qq",
    "bot_id": "10001",
    "message_id": "core_action_handle_friend_welcome_1",
    "time": 1678886400345.0,
    "user_info": {
      "platform": "qq",
      "user_id": "potential_friend_007"
    },
    "interaction_purpose": "core_action",
    "additional_config": {"protocol_version": "1.2.0"}
  },
  "message_segment": {
    "type": "seglist",
    "data": [
      {
        "type": "action:handle_friend_request",
        "data": {
          "request_flag": "flag_unique_friend_request_abc",
          "approve": true,
          "remark": "AI助手小爱"
        }
      },
      {
        "type": "action:send_message",
        "data": {
          "segments": [
            { "type": "text", "data": "你好！很高兴成为你的好友！我是AI助手小爱，有什么可以帮助你的吗？" }
          ]
        }
      }
    ]
  }
}
```

### 3.6. 动作响应 (`interaction_purpose = "action_response"`) (可选)

Adapter 对 Core 发起的 `core_action` 的执行结果进行反馈。

**`MessageBase.message_info.message_id`**: 应与对应的 `core_action` 的 `message_id` 相关联，方便追踪。
**`MessageBase.message_segment`**: 包含一个或多个 `Seg` 对象，描述动作执行结果。

**`Seg` 类型:**

* **`Seg(type="action_result:success", data={...})`**
    * `original_action_type` (str): 原始动作类型 (例如: `"action:send_message"`)。
    * `details` (Optional[Dict]): 成功时的附加信息 (例如: `{"sent_message_id": "platform_msg_new_123"}` 对于 `send_message`)。
* **`Seg(type="action_result:failure", data={...})`**
    * `original_action_type` (str): 原始动作类型。
    * `error_code` (Optional[int]): 平台或Adapter定义的错误码。
    * `error_message` (str): 错误描述。
    * `details` (Optional[Dict]): 失败时的附加信息。

**示例 (Adapter -> Core): 发送消息成功响应**
```json
{
  "message_info": {
    "platform": "qq",
    "bot_id": "10001",
    "message_id": "core_action_handle_friend_welcome_1",
    "time": 1678886400350.0,
    "interaction_purpose": "action_response",
    "additional_config": {"protocol_version": "1.2.0"}
  },
  "message_segment": {
    "type": "seglist",
    "data": [
      {
        "type": "action_result:success",
        "data": {
          "original_action_type": "action:send_message",
          "details": {
            "sent_message_id": "platform_msg_sent_xyz"
          }
        }
      }
    ]
  }
}
```

## 4. 传输

所有 AIcarus-Message-Protocol 定义的 `MessageBase` 对象在序列化为 JSON 字符串后，通过自定义实现的通信组件 (如基于 WebSocket、TCP、HTTP 或消息队列) 进行传输。

## 5. 版本控制

本协议当前版本为 **v1.2.0**。后续如有不兼容的重大变更，将递增主版本号或次版本号。小的兼容性修正或补充可递增修订版本号。
强烈建议在 `MessageBase.message_info.additional_config` 中始终包含 `protocol_version` 字段，以确保通信双方能够正确解析协议内容。