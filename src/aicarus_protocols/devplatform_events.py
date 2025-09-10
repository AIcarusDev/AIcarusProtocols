# src/aicarus_protocols/devplatform_events.py
"""AIcarus-Message-Protocol - 开发者平台专属事件.

定义专用于开发者平台与 AIcarusCore 之间通信的事件.
这些事件以 `devplatform.` 为前缀，以区别于标准的用户或系统事件.
"""

# --- UI -> Core (Commands) ---

# UI连接成功后发送，用于身份认证
CMD_CONNECT = "devplatform.command.connect"

# 请求加载指定的YAML测试场景
CMD_LOAD_SCENE = "devplatform.command.load_scene"

# 请求获取Core当前的内部状态快照
CMD_GET_STATE_SNAPSHOT = "devplatform.command.get_state_snapshot"

# (高级) 请求使用临时的Prompt片段重新运行一次认知循环
CMD_WHAT_IF_RERUN = "devplatform.command.what_if_rerun"


# --- Core -> UI (Events) ---

# 对 connect 命令的确认响应
EVT_CONNECTION_ACK = "devplatform.event.connection_ack"

# Core主动推送的内部状态更新
EVT_STATE_UPDATE = "devplatform.event.state_update"

# 确认场景已成功加载
EVT_SCENE_LOADED = "devplatform.event.scene_loaded"

# 当处理开发者命令失败时，向UI发送错误信息
EVT_ERROR = "devplatform.event.error"
