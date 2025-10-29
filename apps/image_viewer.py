from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

from .common import apply_style, create_button

class ImageViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.originalHeight, self.originalWidth = None, None
        self.initUI()

    def initUI(self):
        main_layout = QGridLayout(self)
        main_layout.setSpacing(15)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(1105, 635)
        apply_style(self.image_label)
        main_layout.addWidget(self.image_label, 0, 0, 1, 3)

        buttons_layout = QGridLayout()

        zoom_in_button = create_button("Zoom In", slot=self.zoom_in)
        buttons_layout.addWidget(zoom_in_button, 1, 0)

        browse_button = create_button("Browse", slot=self.open_image)
        buttons_layout.addWidget(browse_button, 1, 1)

        zoom_out_button = create_button("Zoom Out", slot=self.zoom_out)
        buttons_layout.addWidget(zoom_out_button, 1, 2)

        main_layout.addLayout(buttons_layout, 1, 0, 1, 3)
        self.setLayout(main_layout)

    def open_image(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            image = QImage(file_path)
            if not image.isNull():
                pixmap = QPixmap.fromImage(image)
                pixmap = self.scale_image(pixmap)
                self.image_label.setPixmap(pixmap)
                self.originalHeight, self.originalWidth = pixmap.height(), pixmap.width()

    def scale_image(self, pixmap):
        window_size = self.size()
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

    def zoom_in(self):
        pixmap = self.image_label.pixmap()
        if pixmap:
            new_width = int(pixmap.width() * 1.5)
            new_height = int(pixmap.height() * 1.5)
            pixmap = pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)

    def zoom_out(self):
        pixmap = self.image_label.pixmap()
        if pixmap:
            new_width = int(pixmap.width() * 0.5)
            new_height = int(pixmap.height() * 0.5)
            if new_width <= self.originalWidth or new_height <= self.originalHeight:
                new_width, new_height = self.originalWidth, self.originalHeight
            pixmap = pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)