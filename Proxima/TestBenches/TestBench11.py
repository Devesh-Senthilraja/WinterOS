import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create main layout
        mainLayout = QVBoxLayout(self)

        # Top layout for controls
        topLayout = QGridLayout()
        
        # Bottom layout for the web view
        bottomLayout = QGridLayout()

        # WebEngineView
        self.webView = QWebEngineView()
        self.webView.setUrl(QUrl("https://www.google.com"))

        # Buttons and LineEdit
        backButton = QPushButton()
        backButton.setIcon(QIcon("Icons/arrow1.png"))  # Use appropriate path or resource
        backButton.clicked.connect(self.webView.back)

        forwardButton = QPushButton()
        forwardButton.setIcon(QIcon("Icons/arrow2.png"))  # Use appropriate path or resource
        forwardButton.clicked.connect(self.webView.forward)

        homeButton = QPushButton()
        homeButton.setIcon(QIcon("Icons/home.png"))  # Use appropriate path or resource
        homeButton.clicked.connect(lambda: self.webView.setUrl(QUrl("https://www.google.com")))

        self.urlLineEdit = QLineEdit()
        self.urlLineEdit.setFont(QFont("Arial", 14))
        
        goButton = QPushButton("Go")
        goButton.setFont(QFont("Arial", 14))
        goButton.clicked.connect(self.navigate)

        # Add widgets to top layout
        topLayout.addWidget(backButton, 0, 0)
        topLayout.addWidget(forwardButton, 0, 1)
        topLayout.addWidget(homeButton, 0, 2)
        topLayout.addWidget(self.urlLineEdit, 0, 3)
        topLayout.addWidget(goButton, 0, 4)

        # Add web view to bottom layout
        bottomLayout.addWidget(self.webView, 0, 0)

        # Add layouts to main layout
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(bottomLayout)

        # Set main layout
        self.setLayout(mainLayout)
        self.setWindowTitle('Web Browser')
        self.resize(1024, 768)

    def navigate(self):
        url = self.urlLineEdit.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://www.google.com/search?q=" + url
        self.webView.setUrl(QUrl(url))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())
