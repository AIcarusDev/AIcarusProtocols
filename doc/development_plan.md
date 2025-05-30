# AIcarus-Message-Protocol 项目开发计划

## 1. 项目目标

构建一个基于 AIcarus-Message-Protocol 通信协议的 QQ 聊天机器人。该机器人采用核心 (Core) 与 Napcat 适配器 (Adapter) 分离的解耦架构，以实现易于维护、扩展和未来支持多平台的能力。

## 2. 技术栈

-   **核心与适配器开发语言**: Python 3.9+
-   **通信协议实现**: 自定义实现 (遵循 AIcarus-Message-Protocol，用于 Core-Adapter 间通信)
-   **QQ 平台接入**: Napcat (或其 Python SDK)
-   **文档**: Markdown
-   **(可选) 核心功能**: 自然语言处理库 (如 spaCy, NLTK, HanLP), 对话管理框架, 数据库 (如 SQLite, PostgreSQL)

## 3. 开发阶段与任务

### 阶段一：基础架构与协议实现 (预计时间: 2-3 周)

* **任务 1.1: 协议最终确认与文档化**
    * 负责人: Dax233
    * 描述: 根据 AIcarus-Message-Protocol 通信协议文档完成协议细节的最终审查和确认。
    * 产出: 最终版通信协议文档。
* **任务 1.2: 定义核心数据结构 (MessageBase, Seg 等) 的 Python 实现**
    * 负责人: Dax233
    * 描述: 根据协议文档，在 Python 中实现 `MessageBase`, `Seg`, `UserInfo`, `GroupInfo`, `BaseMessageInfo` 等核心数据类及其序列化/反序列化方法 (`to_dict`, `from_dict`)。
    * 产出: 包含核心数据结构的 Python 模块。
* **任务 1.3: 核心 (Core) 基础服务搭建**
    * 负责人: Dax233
    * 描述: 使用自定义实现的通信组件 (如基于 WebSocket 或 TCP 的服务器) 创建一个基础的核心服务，能够接收连接。实现对 `MessageBase` 对象的初步解析，特别是 `interaction_purpose` 字段。
    * 产出: 能够启动并接收 `MessageBase` 对象的核心服务骨架。
* **任务 1.4: Napcat 适配器 (Adapter) 基础客户端搭建**
    * 负责人: Dax233
    * 描述: 使用自定义实现的通信组件 (客户端部分) 创建一个能够连接到核心服务的基础适配器。
    * 产出: 能够连接到核心并发送简单 `MessageBase` 对象的适配器骨架。
* **任务 1.5: 初步连接测试**
    * 负责人: Dax233
    * 描述: 测试 Adapter 与 Core 之间的基本连接和 `MessageBase` 对象收发。
    * 产出: 验证连接成功的日志或测试报告。

### 阶段二：适配器 (Adapter) - QQ 消息与通知处理 (预计时间: 2-4 周)

* **任务 2.1: Napcat SDK 集成与事件监听**
    * 负责人: Dax233
    * 描述: 在 Adapter 中集成 Napcat SDK，配置并监听 QQ 私聊消息、群聊消息以及关键的平台通知 (如加群、退群等)。
    * 产出: Adapter 能够接收并打印原始 Napcat 事件数据。
* **任务 2.2: 用户消息转换与上报**
    * 负责人: Dax233
    * 描述: 将接收到的 Napcat 用户消息 (私聊/群聊) 转换为协议定义的 `MessageBase` 对象 (`interaction_purpose="user_message"`)，填充 `message_info` 和 `message_segment` (包含各种 `Seg` 类型如 text, image, at)。通过通信客户端发送给 Core。
    * 产出: Core 能够接收到格式正确的用户消息 `MessageBase` 对象。
* **任务 2.3: 平台通知转换与上报**
    * 负责人: Dax233
    * 描述: 将接收到的 Napcat 平台通知 (如加群、退群、好友请求等) 转换为协议定义的 `MessageBase` 对象 (`interaction_purpose="platform_notification"`)，填充 `message_info` 和相应的 `notification:[event_name]` 类型的 `Seg`。发送给 Core。
    * 产出: Core 能够接收到格式正确的平台通知 `MessageBase` 对象。
* **任务 2.4: Adapter 日志与错误处理**
    * 负责人: Dax233
    * 描述: 在 Adapter 中实现健壮的日志记录和基本的错误处理机制。
    * 产出: 清晰的 Adapter 运行日志。

### 阶段三：核心 (Core) - 消息处理与动作下发 (预计时间: 3-5 周)

* **任务 3.1: Core 接收与解析 `MessageBase`**
    * 负责人: Dax233
    * 描述: 完善 Core 对从 Adapter 收到的 `MessageBase` 对象的解析逻辑，能够根据 `interaction_purpose` 和 `Seg.type` 进行分发。
    * 产出: Core 内部清晰的消息/通知处理流程。
* **任务 3.2: 用户消息处理逻辑 (初期简单回复)**
    * 负责人: Dax233
    * 描述: 实现对 `user_message` 的初步处理逻辑，例如简单的关键词回复、echo 服务等。
    * 产出: Core 能够对特定用户消息做出反应。
* **任务 3.3: 核心动作构建与发送**
    * 负责人: Dax233
    * 描述: Core 根据处理逻辑，构建符合协议的 `MessageBase` 对象 (`interaction_purpose="core_action"`)，其中 `message_segment` 包含如 `action:send_message` 等动作 `Seg`。通过通信服务器发送给对应的 Adapter。
    * 产出: Adapter 能够接收到 Core 下发的动作指令。
* **任务 3.4: 平台通知处理逻辑 (初期)**
    * 负责人: Dax233
    * 描述: 实现对部分 `platform_notification` 的处理，如记录日志、更新内部状态等。
    * 产出: Core 能够响应部分平台通知。
* **任务 3.5: Core 日志与错误处理**
    * 负责人: Dax233
    * 描述: 在 Core 中实现健壮的日志记录和错误处理。
    * 产出: 清晰的 Core 运行日志。

### 阶段四：适配器 (Adapter) - 执行核心动作 (预计时间: 2-4 周)

* **任务 4.1: Adapter 接收与解析核心动作**
    * 负责人: Dax233
    * 描述: Adapter 能够正确接收并解析 Core 发来的 `core_action` 类型的 `MessageBase`，并根据 `action:[action_name]` 类型的 `Seg` 进行分发。
    * 产出: Adapter 内部清晰的动作处理流程。
* **任务 4.2: 实现 `action:send_message`**
    * 负责人: Dax233
    * 描述: Adapter 将 `action:send_message` 指令中的 `segments` 转换为 Napcat 支持的消息格式，并调用 Napcat API 发送消息。处理私聊和群聊目标。
    * 产出: 机器人能够通过 Napcat 发送消息。
* **任务 4.3: 实现其他关键动作**
    * 负责人: Dax233
    * 描述: 根据需求优先级，逐步实现其他核心动作，如 `action:kick_user`, `action:mute_user`, `action:delete_message`, `action:handle_friend_request` 等。
    * 产出: 机器人具备更多通过 Napcat 执行操作的能力。
* **任务 4.4: (可选) 动作结果反馈**
    * 负责人: Dax233
    * 描述: 实现 Adapter 将动作执行结果 (成功/失败) 通过 `interaction_purpose="action_response"` 的 `MessageBase` 反馈给 Core。
    * 产出: Core 能够获知动作执行状态。

### 阶段五：核心 (Core) - 高级功能与智能化 (持续迭代)

* **任务 5.1: 自然语言理解 (NLU) 集成**
    * 负责人: Dax233
* **任务 5.2: 对话管理**
    * 负责人: Dax233
* **任务 5.3: 业务逻辑与插件系统**
    * 负责人: Dax233
* **任务 5.4: 数据持久化**
    * 负责人: Dax233

### 阶段六：测试、部署与维护 (贯穿始终，集中在后期)

* **任务 6.1: 单元测试**
    * 负责人: Dax233
* **任务 6.2: 集成测试**
    * 负责人: Dax233
* **任务 6.3: 用户验收测试 (UAT)**
    * 负责人: Dax233
* **任务 6.4: 性能优化与稳定性提升**
    * 负责人: Dax233
* **任务 6.5: 部署方案设计与实施**
    * 负责人: Dax233
* **任务 6.6: 运维文档与用户手册编写**
    * 负责人: Dax233

## 4. 时间规划 (占位)

| 阶段                                       | 预计开始日期 | 预计结束日期 | 状态   |
| :----------------------------------------- | :----------- | :----------- | :----- |
| 阶段一：基础架构与协议实现                 |              |              | 未开始 |
| 阶段二：适配器 - QQ 消息与通知处理         |              |              | 未开始 |
| 阶段三：核心 - 消息处理与动作下发         |              |              | 未开始 |
| 阶段四：适配器 - 执行核心动作             |              |              | 未开始 |
| 阶段五：核心 - 高级功能与智能化           |              | 持续迭代     | 未开始 |
| 阶段六：测试、部署与维护                   |              | 持续进行     | 未开始 |

## 5. 团队角色与职责

-   **项目开发者**: Dax233 - 负责项目整体规划、设计、开发、测试与维护。

---
*本文档为初步计划，具体任务、时间安排可能根据项目进展进行调整。*