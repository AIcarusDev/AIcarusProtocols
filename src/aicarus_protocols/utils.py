# src/aicarus_protocols/utils.py
"""
AIcarus-Message-Protocol v1.6.0 - 通用工具函数
"""

from typing import List, Optional
from .seg import Seg


def extract_text_from_content(content: List[Seg]) -> str:
    """从 content 中提取所有文本内容。"""
    if not content:
        return ""
    text_parts = [
        seg.data["text"] for seg in content if seg.type == "text" and "text" in seg.data
    ]
    return "".join(text_parts)


def find_seg_by_type(content: List[Seg], seg_type: str) -> Optional[Seg]:
    """在 content 中查找指定类型的第一个 Seg。"""
    if not content:
        return None
    for seg in content:
        if seg.type == seg_type:
            return seg
    return None


def filter_segs_by_type(content: List[Seg], seg_type: str) -> List[Seg]:
    """在 content 中查找指定类型的所有 Seg。"""
    return [] if not content else [seg for seg in content if seg.type == seg_type]
