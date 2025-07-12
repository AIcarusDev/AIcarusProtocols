# src/aicarus_protocols/utils.py
"""AIcarus-Message-Protocol v1.6.0 - 通用工具函数."""

from .seg import Seg


def extract_text_from_content(content: list[Seg]) -> str:
    """从 content 中提取所有文本内容.

    Args:
        content (list[Seg]): Seg 对象列表，可能包含多种类型的 Seg.

    Returns:
        str: 提取的所有文本内容，按顺序连接成一个字符串.
    """
    if not content:
        return ""
    text_parts = [seg.data["text"] for seg in content if seg.type == "text" and "text" in seg.data]
    return "".join(text_parts)


def find_seg_by_type(content: list[Seg], seg_type: str) -> Seg | None:
    """在 content 中查找指定类型的第一个 Seg.

    Args:
        content (list[Seg]): Seg 对象列表.
        seg_type (str): 要查找的 Seg 类型.

    Returns:
        Seg | None: 找到的第一个 Seg 对象或 None.
    """
    if not content:
        return None
    for seg in content:
        if seg.type == seg_type:
            return seg
    return None


def filter_segs_by_type(content: list[Seg], seg_type: str) -> list[Seg]:
    """在 content 中查找指定类型的所有 Seg.

    Args:
        content (list[Seg]): Seg 对象列表.
        seg_type (str): 要查找的 Seg 类型.

    Returns:
        list[Seg]: 所有匹配的 Seg 对象列表.
    """
    return [] if not content else [seg for seg in content if seg.type == seg_type]
