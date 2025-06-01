# -*- coding: utf-8 -*-

"""
AIcarus Protocols Package
本包定义了 AIcarus 项目中 Core 与 Adapter 之间通信的消息结构。
"""

# 从 base.py 中导入核心的数据结构类，方便用户直接从包顶层导入
from .base import (
    MessageBase,
    BaseMessageInfo,
    Seg,
    UserInfo,
    GroupInfo
)

# (可选) 定义包级别的 __version__，可以与 setup.py 中的版本同步
# 如果 setup.py 从这里读取版本，可以避免版本信息分散
# from .base import AICARUS_PROTOCOL_VERSION # 假设 base.py 也定义了这个
# __version__ = AICARUS_PROTOCOL_VERSION
# 或者直接硬编码：
__version__ = "1.2.0" # 确保与 setup.py 和文档一致

__all__ = [
    "MessageBase",
    "BaseMessageInfo",
    "Seg",
    "UserInfo",
    "GroupInfo",
    "__version__", # 如果定义了 __version__
]
