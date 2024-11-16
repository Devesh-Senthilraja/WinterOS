import sys
import os
import cv2
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer

class Camera(QWidget):
    def __init__(self, parent=None):
        super(Camera, self).__init__(parent)

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1080)  # Set the width
        self.cap.set(4, 720)   # Set the height
        self.existingIDs = []

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)  # Main layout

        # Frame for showing video feed
        self.photoViewer = QLabel(self)
        self.layout.addWidget(self.photoViewer)

        # Controls frame
        controls = QHBoxLayout()
        self.layout.addLayout(controls)

        # Capture button
        captureButton = QPushButton("Capture", self)
        captureButton.clicked.connect(self.capture)
        controls.addWidget(captureButton)

        # Set up a timer to pull data from the video capture
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showFrames)
        self.timer.start(20)  # Update interval

    def checkID(self):
        if not os.path.exists("Photos"):
            os.mkdir("Photos")
        for x in os.listdir("Photos"):
            if x.endswith(".jpg"):
                id = x.replace("picture", "")
                id = id.replace(".png", "")
                self.existingIDs.append(id)

    def capture(self):
        self.checkID()
        ret, frame = self.cap.read()
        id = str(random.randint(1, 1000))
        while id in self.existingIDs:
            id = str(random.randint(1, 1000))
        if ret:
            outpath = os.path.join("Photos", f"picture{id}.png")
            cv2.imwrite(outpath, frame)
            cv2.waitKey(0)

    def showFrames(self):
        ret, frame = self.cap.read()
        if ret:
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(self.photoViewer.width(), self.photoViewer.height(), Qt.KeepAspectRatio)
            self.photoViewer.setPixmap(QPixmap.fromImage(p))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Camera()
    win.show()
    sys.exit(app.exec_())
