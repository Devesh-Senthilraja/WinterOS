from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QDir
from pathlib import Path
import vlc

from .common import apply_style, create_button

class AudioPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        grid_layout = QGridLayout(self)
        grid_layout.setSpacing(15)

        thumbnail = QLabel(self)
        thumbnail.setFixedSize(625, 560)
        apply_style(thumbnail)
        pixmap = QPixmap(str(Path(__file__).resolve().parents[1] / "icons" / "audio.png"))
        scaled_pixmap = pixmap.scaled(thumbnail.size(), aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        thumbnail.setPixmap(scaled_pixmap)
        grid_layout.addWidget(thumbnail, 0, 0, 1, 4)

        self.vlcInstance = vlc.Instance()
        self.mediaPlayer = self.vlcInstance.media_player_new()

        button_layout = QGridLayout()

        browse_button = create_button("Browse", slot=self.open_audio)
        button_layout.addWidget(browse_button, 0, 0)

        self.play_pause_button = create_button("Play", slot=self.toggle_play_pause)
        button_layout.addWidget(self.play_pause_button, 0, 1)

        volume_up_button = create_button("Volume Up", slot=self.volume_up, size=(160, 50))
        button_layout.addWidget(volume_up_button, 0, 2)

        volume_down_button = create_button("Volume Down", slot=self.volume_down, size=(160, 50))
        button_layout.addWidget(volume_down_button, 0, 3)

        grid_layout.addLayout(button_layout, 1, 0, 1, 4)

    def open_audio(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Audio", QDir.homePath(), "Audio Files (*.mp3 *.wav *.flac)")
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