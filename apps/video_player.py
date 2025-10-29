from PyQt5.QtWidgets import QWidget, QGridLayout, QSizePolicy, QFileDialog
from PyQt5.QtCore import QDir, Qt
import vlc
import sys

from .common import apply_style, create_button

class VideoPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vlcInstance = vlc.Instance()  
        self.mediaPlayer = self.vlcInstance.media_player_new()
        self.initUI()

    def initUI(self):
        main_layout = QGridLayout(self)
        main_layout.setSpacing(15)

        self.videoFrame = QWidget(self)
        self.videoFrame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.videoFrame.setFixedSize(1105, 635)
        self.videoFrame.setAttribute(Qt.WA_NativeWindow, True)
        apply_style(self.videoFrame)
        main_layout.addWidget(self.videoFrame, 0, 0, 1, 4)

        wid = int(self.videoFrame.winId())
        if sys.platform.startswith("linux"):
            self.mediaPlayer.set_xwindow(wid)
        elif sys.platform == "win32":
            self.mediaPlayer.set_hwnd(wid)
        elif sys.platform == "darwin":
            self.mediaPlayer.set_nsobject(wid)

        buttons_layout = QGridLayout()

        browse_button = create_button("Browse", slot=self.open_video)
        buttons_layout.addWidget(browse_button, 0, 0)

        self.play_pause_button = create_button("Play", slot=self.toggle_play_pause)
        buttons_layout.addWidget(self.play_pause_button, 0, 1)

        volume_up_button = create_button("Volume Up", slot=self.volume_up, size=(160, 50))
        buttons_layout.addWidget(volume_up_button, 0, 2)

        volume_down_button = create_button("Volume Down", slot=self.volume_down, size=(160, 50))
        buttons_layout.addWidget(volume_down_button, 0, 3)

        main_layout.addLayout(buttons_layout, 1, 0, 1, 4)

    def open_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Movie", QDir.homePath())
        if file_path:
            media = self.vlcInstance.media_new(file_path)
            self.mediaPlayer.set_media(media)
            self.mediaPlayer.play()
            self.play_pause_button.setText("Pause")

    def toggle_play_pause(self):
        if self.mediaPlayer.is_playing():
            self.mediaPlayer.pause()
            self.play_pause_button.setText("Play")
        else:
            self.mediaPlayer.play()
            self.play_pause_button.setText("Pause")

    def volume_up(self):
        volume = self.mediaPlayer.audio_get_volume()
        self.mediaPlayer.audio_set_volume(min(volume + 10, 100))

    def volume_down(self):
        volume = self.mediaPlayer.audio_get_volume()
        self.mediaPlayer.audio_set_volume(max(volume - 10, 0))
