from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from pathlib import Path
import cv2
import time

from .common import apply_style, create_button

class Camera(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.project_root = Path(__file__).resolve().parents[1]   # .../WinterOS
        self.photos_dir = self.project_root / "Photos"
        self.photos_dir.mkdir(exist_ok=True)

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self._last_frame_bgr = None  # keep latest frame to save on capture
        self.initUI()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showFrames)
        self.timer.start(30)  # ~33 fps

    def initUI(self):
        grid = QGridLayout(self)

        self.photoViewer = QLabel(self)
        self.photoViewer.setFixedSize(1105, 635)
        self.photoViewer.setAlignment(Qt.AlignCenter)
        apply_style(self.photoViewer)
        grid.addWidget(self.photoViewer, 0, 0, 1, 3)

        captureButton = create_button("Capture", slot=self.capture, size=(120, 50), parent=self)
        grid.addWidget(captureButton, 1, 1)

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(2, 1)

    def _unique_photo_path(self) -> Path:
        ts = time.strftime("%Y%m%d-%H%M%S")
        return self.photos_dir / f"picture-{ts}.png"

    def capture(self):
        if self._last_frame_bgr is None:
            return  # nothing to save yet
        outpath = self._unique_photo_path()
        ok = cv2.imwrite(str(outpath), self._last_frame_bgr)
        if not ok:
            print(f"Failed to save image to {outpath}")

    def showFrames(self):
        ok, frame_bgr = self.cap.read()
        if not ok:
            return
        self._last_frame_bgr = frame_bgr

        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w

        qimg = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        scaled = qimg.scaled(self.photoViewer.width(), self.photoViewer.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.photoViewer.setPixmap(QPixmap.fromImage(scaled))

    def closeEvent(self, event):
        try:
            if self.timer.isActive():
                self.timer.stop()
        except Exception:
            pass
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        super().closeEvent(event)
