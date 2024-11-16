import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QAction, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Viewer")
        self.setFixedSize(800, 800)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)  # Center the label contents
        self.image_label.setStyleSheet("QLabel {border-radius: 10px; border: 2px solid gray;}")  # Rounded corners style
        self.setCentralWidget(self.image_label)

        self.create_actions()
        self.create_menus()

    def create_actions(self):
        self.open_action = QAction("Open Image", self)
        self.open_action.triggered.connect(self.open_image)

    def create_menus(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction(self.open_action)

    def open_image(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")

        if file_path:
            image = QImage(file_path)
            if not image.isNull():
                pixmap = QPixmap.fromImage(image)
                pixmap = self.scale_image(pixmap)
                self.image_label.setPixmap(pixmap)

    def scale_image(self, pixmap):
        window_size = self.centralWidget().size()
        width_ratio = window_size.width() / pixmap.width()
        height_ratio = window_size.height() / pixmap.height()

        if width_ratio > 1 and height_ratio > 1:
            return pixmap
        else:
            if width_ratio < height_ratio:
                scaled_width = window_size.width()
                scaled_height = int(pixmap.height() * width_ratio)
            else:
                scaled_width = int(pixmap.width() * height_ratio)
                scaled_height = window_size.height()

            return pixmap.scaled(scaled_width, scaled_height, Qt.KeepAspectRatio)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    sys.exit(app.exec_())
