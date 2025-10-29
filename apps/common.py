from __future__ import annotations

from typing import Callable, Iterable, Optional, Tuple

from PyQt5.QtWidgets import QPushButton, QWidget

_DEFAULT_FONT_FAMILY = "'Arial'"
_BORDER_STYLE = "border: 1px solid lightgrey; border-radius: 10px;"


def widget_style(*, font_size: int = 20, background: str = "#f0f0f0", bold: bool = True, border: bool = True) -> str:
    weight = "bold " if bold else ""
    parts: Iterable[str] = (
        f"background-color: {background};",
        f"font: {weight}{font_size}px {_DEFAULT_FONT_FAMILY};",
        _BORDER_STYLE if border else "",
    )
    return " ".join(part for part in parts if part)


def apply_style(widget: QWidget, /, *, font_size: int = 20, background: str = "#f0f0f0", bold: bool = True, border: bool = True) -> QWidget:
    widget.setStyleSheet(widget_style(font_size=font_size, background=background, bold=bold, border=border))
    return widget


def button_style(*, font_size: int = 20, background: str = "#d9d9d9", bold: bool = True, border: bool = True) -> str:
    return widget_style(font_size=font_size, background=background, bold=bold, border=border)


def create_button(
    text: str,
    *,
    slot: Optional[Callable] = None,
    size: Optional[Tuple[int, int]] = (100, 50),
    font_size: int = 20,
    background: str = "#d9d9d9",
    bold: bool = True,
    parent: Optional[QWidget] = None,
    checkable: bool = False,
) -> QPushButton:
    button = QPushButton(text, parent)
    button.setStyleSheet(button_style(font_size=font_size, background=background, bold=bold, border=True))
    if size:
        if len(size) != 2:
            raise ValueError("size must be a (width, height) tuple when provided")
        button.setFixedSize(*size)
    if slot:
        button.clicked.connect(slot)
    if checkable:
        button.setCheckable(True)
    return button
