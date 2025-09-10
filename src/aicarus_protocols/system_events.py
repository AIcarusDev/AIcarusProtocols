# src/aicarus_protocols/system_events.py
"""AIcarus-Message-Protocol v1.6.0 - 系统状态事件.

定义与系统核心状态相关的事件.
"""
import json
import time
from uuid import uuid4

from .event import Event
from .seg import Seg, SegBuilder


def build_system_status_event(status: str, message: str = "") -> Event:
    """构建一个系统状态事件.

    Args:
        status (str): 当前的系统状态.
            (e.g., "initializing", "services_built", "ready")
        message (str, optional): 附加的描述信息. Defaults to "".

    Returns:
        Event: 构建好的事件对象.
    """
    # [修复] 将状态码直接整合进 event_type，使其更具描述性
    event_type = f"system.status.{status}"
    
    # [修复] 创建符合协议规范的 content 字段
    content = [SegBuilder.text(f"[{status}] {message}")] if message else [SegBuilder.text(status)]

    # [修复] 调用 Event 构造函数时，提供所有必需的参数
    return Event(
        event_id=str(uuid4()),
        time=int(time.time()),
        event_type=event_type,
        bot_id="aicarus_core_system",  # 为系统事件使用一个固定的 ID
        content=content,
        # 对于系统事件，以下上下文信息可以为空
        user_info=None,
        conversation_info=None,
        raw_data=json.dumps({"status": status, "message": message}),  # 将原始信息放入附加数据中
    )
