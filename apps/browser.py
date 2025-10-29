from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pathlib import Path

from .common import apply_style, create_button

class Browser(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        mainLayout = QGridLayout(self)
        topLayout = QGridLayout()
        bottomLayout = QGridLayout()

        self.webView = QWebEngineView()
        self.webView.setFixedSize(1105, 645)
        apply_style(self.webView, font_size=15)
        self.webView.setUrl(QUrl("https://www.google.com"))

        backButton = QPushButton()
        backButton.setIcon(QIcon(str(Path(__file__).resolve().parents[1] / "icons" / "arrow1.png")))
        backButton.setFixedHeight(50)
        backButton.clicked.connect(self.webView.back)

        forwardButton = QPushButton()
        forwardButton.setIcon(QIcon(str(Path(__file__).resolve().parents[1] / "icons" / "arrow2.png")))
        forwardButton.setFixedHeight(50)
        forwardButton.clicked.connect(self.webView.forward)

        homeButton = QPushButton()
        homeButton.setIcon(QIcon(str(Path(__file__).resolve().parents[1] / "icons" / "home.png")))
        homeButton.setFixedHeight(50)
        homeButton.clicked.connect(lambda: self.webView.setUrl(QUrl("https://www.google.com")))

        self.urlLineEdit = QLineEdit()
        self.urlLineEdit.setFixedSize(850, 50)
        apply_style(self.urlLineEdit, font_size=15)

        goButton = create_button("Go", slot=self.navigate, size=(100, 50), font_size=15)

        topLayout.addWidget(backButton, 0, 0)
        topLayout.addWidget(forwardButton, 0, 1)
        topLayout.addWidget(homeButton, 0, 2)
        topLayout.addWidget(self.urlLineEdit, 0, 3)
        topLayout.addWidget(goButton, 0, 4)

        bottomLayout.addWidget(self.webView, 0, 0)

        mainLayout.addLayout(topLayout, 0, 0)
        mainLayout.addLayout(bottomLayout, 1, 0)

    def navigate(self):
        url = self.urlLineEdit.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://www.google.com/search?q=" + url
        self.webView.setUrl(QUrl(url))