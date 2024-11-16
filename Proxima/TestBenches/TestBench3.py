import sys
import vlc
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPainter, QBrush, QColor

class VLCVideoPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("VLC Video Player")
        self.setFixedSize(640, 360)  # Set the fixed size of the video player window

        # Set the window to be frameless and transparent
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Initialize the VLC player
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # Set up the video frame
        self.video_frame = QFrame()
        self.video_frame.setFixedSize(640, 360)
        self.video_frame.setStyleSheet("background-color: transparent; border-radius: 20px;")

        # Use a QVBoxLayout to lay out the widgets (just the video frame for now)
        layout = QVBoxLayout()
        layout.addWidget(self.video_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Set the VLC player to use the frame as its drawable (video output)
        if sys.platform.startswith('linux'):  # for Linux using the X Server
            self.player.set_xwindow(self.video_frame.winId())
        elif sys.platform == "win32":  # for Windows
            self.player.set_hwnd(self.video_frame.winId())
        elif sys.platform == "darwin":  # for MacOS
            self.player.set_nsobject(int(self.video_frame.winId()))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        brush = QBrush(QColor(255, 255, 255, 0))  # Transparent
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)  # Rounded corners with a radius of 20

    def loadMedia(self, url):
        media = self.instance.media_new(url)
        self.player.set_media(media)
        self.player.play()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VLCVideoPlayer()
    player.loadMedia("path_to_video.mp4")  # Make sure to provide the correct path to the video
    player.show()
    sys.exit(app.exec_())
