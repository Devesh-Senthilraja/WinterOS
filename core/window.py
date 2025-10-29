from __future__ import annotations

from contextlib import suppress
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Callable, Dict, Iterable, Optional, Set, Tuple

from PyQt5.QtCore import QDateTime, QPoint, Qt, QTimer
from PyQt5.QtGui import QColor, QIcon, QPalette
from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QWidget,
)

from apps.audio_player import AudioPlayer
from apps.browser import Browser
from apps.calculator import Calculator
from apps.calendar import Calendar
from apps.camera import Camera
from apps.clock import Clock
from apps.dictionary import Dictionary
from apps.image_viewer import ImageViewer
from apps.map import Map
from apps.news import News
from apps.notepad import Notepad
from apps.paint import Paint
from apps.terminal import Terminal
from apps.translate import Translate
from apps.video_player import VideoPlayer
from apps.weather import Weather


ICON_DIR = Path(__file__).resolve().parent.parent / "icons"


@dataclass(frozen=True)
class ButtonConfig:
    icon: Path
    aliases: Set[str]
    action: Callable[[], None]


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.active_window: Optional[Window] = None
        self.buttonElements: Dict[str, ButtonConfig] = {}
        self.line_edit: Optional[QLineEdit] = None
        self.time_label: Optional[QLabel] = None
        self.date_label: Optional[QLabel] = None

        self._configure_window()
        launcher_layout = self._build_layout()
        self._init_button_elements()
        self._add_buttons(launcher_layout)

    def _configure_window(self) -> None:
        self.setWindowTitle("OS")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("lightgrey"))
        self.setPalette(palette)

    def _build_layout(self) -> QGridLayout:
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout(central_widget)
        grid_layout.setContentsMargins(10, 0, 0, 10)
        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(1, 0)

        launcher_widget, launcher_layout = self._create_launcher_panel()
        grid_layout.addWidget(launcher_widget, 0, 0, Qt.AlignLeft | Qt.AlignVCenter)

        bottom_widget = self._create_bottom_panel()
        grid_layout.addWidget(bottom_widget, 1, 0, Qt.AlignBottom | Qt.AlignHCenter)

        return launcher_layout

    def _create_launcher_panel(self) -> Tuple[QWidget, QGridLayout]:
        launcher_widget = QWidget()
        launcher_widget.setFixedSize(300, 900)
        launcher_widget.setStyleSheet("background-color: lightgrey; border-radius: 25px;")

        launcher_layout = QGridLayout(launcher_widget)
        launcher_layout.setContentsMargins(15, 15, 15, 15)
        launcher_layout.setHorizontalSpacing(15)
        launcher_layout.setVerticalSpacing(15)

        return launcher_widget, launcher_layout

    def _create_bottom_panel(self) -> QWidget:
        bottom_widget = QWidget()
        bottom_widget.setFixedSize(625, 100)
        bottom_widget.setStyleSheet("background-color: lightgrey; border-radius: 25px;")

        bottom_layout = QGridLayout(bottom_widget)
        bottom_layout.setContentsMargins(10, 0, 10, 0)

        for index in range(3):
            container = QWidget()
            container.setStyleSheet("background-color: black; border-radius: 25px;")
            bottom_layout.addWidget(container, 0, index, Qt.AlignCenter)

            if index == 1:
                self._build_search_widget(container)
            elif index == 0:
                self._build_clock_widget(container)
            else:
                self._build_power_widget(container)

        return bottom_widget

    def _build_search_widget(self, parent: QWidget) -> None:
        parent.setFixedSize(325, 75)

        layout = QGridLayout(parent)
        layout.setContentsMargins(15, 0, 15, 0)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Enter app name")
        self.line_edit.setFixedSize(240, 50)
        self.line_edit.setStyleSheet("background-color: white; border-radius: 12px; padding: 5px;")
        layout.addWidget(self.line_edit, 0, 0, Qt.AlignLeft)

        search_button = QPushButton()
        search_button.setIcon(self._icon("searchButton.png"))
        search_button.setFixedSize(50, 50)
        search_button.setIconSize(search_button.size())
        search_button.setStyleSheet("background-color: black; border: none;")
        search_button.clicked.connect(self.searchAndRunApp)
        layout.addWidget(search_button, 0, 1, Qt.AlignRight)

    def _build_clock_widget(self, parent: QWidget) -> None:
        parent.setFixedSize(125, 75)

        layout = QGridLayout(parent)
        layout.setContentsMargins(0, 10, 0, 10)

        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: white;")
        self.time_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.time_label, 0, 0, Qt.AlignCenter)

        self.date_label = QLabel()
        self.date_label.setStyleSheet("color: white;")
        self.date_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.date_label, 1, 0, Qt.AlignCenter)

        timer = QTimer(self)
        timer.timeout.connect(self.updateDateTime)
        timer.start(1000)
        self.updateDateTime()

    def _build_power_widget(self, parent: QWidget) -> None:
        parent.setFixedSize(125, 75)

        layout = QGridLayout(parent)
        layout.setContentsMargins(0, 0, 0, 0)

        shutdown_button = QPushButton()
        shutdown_button.setIcon(self._icon("powerButton.png"))
        shutdown_button.setFixedSize(50, 50)
        shutdown_button.setIconSize(shutdown_button.size())
        shutdown_button.setStyleSheet("background-color: black; border: none;")
        shutdown_button.clicked.connect(self.close)
        layout.addWidget(shutdown_button, 0, 0, Qt.AlignCenter)

    def _icon(self, filename: str) -> QIcon:
        icon_path = ICON_DIR / filename
        if not icon_path.is_file():
            print(f"Icon file not found: {icon_path}")
        return QIcon(str(icon_path))

    def updateDateTime(self) -> None:
        if not self.time_label or not self.date_label:
            return
        current_time = QDateTime.currentDateTime()
        self.time_label.setText(current_time.toString("hh:mm:ss"))
        self.date_label.setText(current_time.toString("yyyy-MM-dd"))

    def searchAndRunApp(self) -> None:
        if not self.line_edit:
            return

        search_text = self.line_edit.text().strip().lower()
        if not search_text:
            return

        for config in self.buttonElements.values():
            if search_text in config.aliases:
                config.action()
                break

    def _register_app(
        self,
        key: str,
        icon_filename: str,
        widget_cls: type,
        *,
        title: str,
        width: int,
        height: int,
        aliases: Optional[Iterable[str]] = None,
    ) -> None:
        alias_set = {key.lower()}
        if aliases:
            alias_set.update(alias.lower() for alias in aliases)

        self.buttonElements[key] = ButtonConfig(
            icon=ICON_DIR / icon_filename,
            aliases=alias_set,
            action=partial(self.runApp, width, height, title, widget_cls),
        )

    def _init_button_elements(self) -> None:
        self._register_app("calculator", "calculator.png", Calculator, title="Calculator", width=470, height=740)
        self._register_app("calendar", "calendar.png", Calendar, title="Calendar", width=1130, height=780)
        self._register_app("clock", "clock.png", Clock, title="Clock", width=650, height=700)
        self._register_app("notepad", "notepad.png", Notepad, title="Notepad", width=735, height=990)
        self._register_app("paint", "paint.png", Paint, title="Paint", width=735, height=990)
        self._register_app(
            "photos",
            "photoViewer.png",
            ImageViewer,
            title="Image Viewer",
            width=1130,
            height=780,
        )
        self._register_app(
            "music",
            "musicPlayer.png",
            AudioPlayer,
            title="Audio Player",
            width=650,
            height=700,
            aliases=["audio"],
        )
        self._register_app(
            "videos",
            "videoPlayer.png",
            VideoPlayer,
            title="Video Player",
            width=1130,
            height=780,
        )
        self._register_app("camera", "camera.png", Camera, title="Camera", width=1130, height=780)
        self._register_app("terminal", "terminal.png", Terminal, title="Terminal", width=1130, height=780)
        self._register_app("weather", "weather.png", Weather, title="Weather", width=1130, height=780)
        self._register_app("news", "news.png", News, title="News", width=1130, height=780)
        self._register_app("map", "map.png", Map, title="Map", width=1130, height=780)
        self._register_app(
            "translate",
            "translate.png",
            Translate,
            title="Translate",
            width=1130,
            height=780,
            aliases=["translator"],
        )
        self._register_app("dictionary", "dictionary.png", Dictionary, title="Dictionary", width=1130, height=780)
        self._register_app(
            "chat",
            "chat.png",
            Browser,
            title="Browser",
            width=1130,
            height=780,
            aliases=["browser"],
        )

    def _add_buttons(self, layout: QGridLayout) -> None:
        for index, config in enumerate(self.buttonElements.values()):
            if not config.icon.is_file():
                print(f"Icon file not found: {config.icon}")
                continue

            button = QPushButton()
            button.setIcon(QIcon(str(config.icon)))
            button.setFixedSize(75, 75)
            button.setIconSize(button.size())
            button.setStyleSheet("background-color: lightgrey; border: none;")
            button.clicked.connect(config.action)

            row = index % 8
            col = index // 8
            layout.addWidget(button, row, col)

    def runApp(self, width: int, height: int, appName: str, app: type) -> None:
        if self.active_window is not None:
            with suppress(Exception):
                self.active_window.close()

        self.active_window = Window(width, height, appName, app)
        self.active_window.show()


class Window(QWidget):
    def __init__(self, width: int, height: int, title: str, app_widget_class: type) -> None:
        super().__init__()
        self._size = (width, height)
        self._title = title
        self._app_widget_class = app_widget_class
        self.app_space: Optional[QWidget] = None
        self.app_widget: Optional[QWidget] = None
        self._drag_active = False
        self._drag_position = QPoint()

        self._build_ui()

    def _build_ui(self) -> None:
        width, height = self._size
        self.setFixedSize(width, height)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        title_bar = QWidget(self)
        title_bar.setStyleSheet(
            "background-color: gray; border-top-left-radius: 10px; border-top-right-radius: 10px;"
        )
        title_bar.setFixedHeight(50)

        self.app_space = QWidget(self)
        self.app_space.setStyleSheet(
            "background-color: white; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;"
        )

        layout.addWidget(title_bar, 0, 0)
        layout.addWidget(self.app_space, 1, 0)

        title_layout = QGridLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 15, 0)

        title_label = QLabel(self._title)
        title_label.setStyleSheet("color: white; font: 20px 'Bernoru'")
        title_layout.addWidget(title_label, 0, 0)

        close_button = QPushButton("X")
        close_button.setStyleSheet("background-color: red; color: white; border-radius: 10px;")
        close_button.setFixedSize(30, 30)
        close_button.clicked.connect(self.on_close_clicked)
        title_layout.addWidget(close_button, 0, 1, Qt.AlignRight)

        self.app_widget = self._app_widget_class(self.app_space)

    def _teardown_app(self) -> None:
        if self.app_space is not None:
            for timer in self.app_space.findChildren(QTimer):
                if timer.isActive():
                    timer.stop()

        widget = self.app_widget
        if widget is None:
            return

        media_player = getattr(widget, "mediaPlayer", None)
        if media_player is not None:
            with suppress(Exception):
                media_player.stop()
            with suppress(Exception):
                media_player.release()

        vlc_instance = getattr(widget, "vlcInstance", None)
        if vlc_instance is not None:
            with suppress(Exception):
                vlc_instance.release()

        capture = getattr(widget, "cap", None)
        if capture is not None:
            with suppress(Exception):
                capture.release()

        with suppress(Exception):
            import cv2 as _cv2

            _cv2.destroyAllWindows()

    def on_close_clicked(self) -> None:
        self._teardown_app()
        self.close()

    def closeEvent(self, event) -> None:  # type: ignore[override]
        self._teardown_app()
        super().closeEvent(event)

    def mousePressEvent(self, event) -> None:  # type: ignore[override]
        if event.button() == Qt.LeftButton:
            self._drag_active = True
            self._drag_position = event.globalPos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:  # type: ignore[override]
        if self._drag_active and event.buttons() & Qt.LeftButton:
            delta = event.globalPos() - self._drag_position
            self.move(self.pos() + delta)
            self._drag_position = event.globalPos()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # type: ignore[override]
        if event.button() == Qt.LeftButton:
            self._drag_active = False
        super().mouseReleaseEvent(event)
