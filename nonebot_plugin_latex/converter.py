from .data import ConvertLatex

_converter = ConvertLatex()
"""
Latex 渲染器
"""


def get_converter() -> ConvertLatex:
    """
    获取渲染器
    """
    return _converter
