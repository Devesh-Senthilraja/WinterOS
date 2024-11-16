import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QMessageBox, QTextBrowser
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class News(QWidget):
    def __init__(self):
        super().__init__()

        self.popups = []

        self.initWidgets()

    def initWidgets(self):
        # Create main layout
        mainLayout = QGridLayout()

        # Category frame layout
        categoryLayout = QGridLayout()
        categoryLayout.setSpacing(10)

        buttons = [
            ("General", "general"),
            ("Entertainment", "entertainment"),
            ("Business", "business"),
            ("Sports", "sports"),
            ("Technology", "technology"),
            ("Health", "health")
        ]

        for i, (text, category) in enumerate(buttons):
            button = QPushButton(text)
            button.setFont(QFont("Comic Sans", 14))
            button.setFixedHeight(40)
            button.setFixedWidth(110)
            button.clicked.connect(lambda _, cat=category: self.getNews(cat))
            categoryLayout.addWidget(button, 0, i+1)

        categoryLayout.setColumnStretch(0, 1)
        categoryLayout.setColumnStretch(len(buttons)+1, 1)

        # News frame layout
        newsLayout = QGridLayout()
        self.newsOutput = QTextBrowser()
        self.newsOutput.setFont(QFont("Comic Sans", 12))
        self.newsOutput.setOpenExternalLinks(False)
        self.newsOutput.anchorClicked.connect(self.openPopup)
        newsLayout.addWidget(self.newsOutput, 0, 0)

        # Add layouts to main layout
        mainLayout.addLayout(categoryLayout, 0, 0)
        mainLayout.addLayout(newsLayout, 1, 0)

        # Set main layout
        self.setLayout(mainLayout)

    def getNews(self, type):
        newsURL = f"http://newsapi.org/v2/top-headlines?country=us&category={type}&apiKey=ff3ba8e42f024772a4424526fd246095"
        self.newsOutput.clear()
        try:
            newsInfo = (requests.get(newsURL).json())['articles']

            if newsInfo:
                for i, article in enumerate(newsInfo):
                    headline = f"\n • {article['title']}\n"
                    url = article['url']
                    self.newsOutput.append(f'<a href="{url}">{headline}</a>')

            else:
                self.newsOutput.setText("Sorry. No news available.")

        except Exception:
            QMessageBox.critical(self, 'No Internet', "Unable to connect to the internet at the moment.")

    def openPopup(self, url):
        webview = QWebEngineView()
        webview.setWindowTitle('News Article')
        webview.load(url)
        webview.show()
        self.popups.append(webview)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    newsApp = News()
    newsApp.setWindowTitle('News')
    newsApp.resize(850, 600)
    newsApp.show()
    sys.exit(app.exec_())
import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QMessageBox, QTextBrowser
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class News(QWidget):
    def __init__(self):
        super().__init__()

        self.popups = []

        self.initWidgets()

    def initWidgets(self):
        # Create main layout
        mainLayout = QGridLayout()

        # Category frame layout
        categoryLayout = QGridLayout()
        categoryLayout.setSpacing(10)

        buttons = [
            ("General", "general"),
            ("Entertainment", "entertainment"),
            ("Business", "business"),
            ("Sports", "sports"),
            ("Technology", "technology"),
            ("Health", "health")
        ]

        for i, (text, category) in enumerate(buttons):
            button = QPushButton(text)
            button.setFont(QFont("Comic Sans", 14))
            button.setFixedHeight(40)
            button.setFixedWidth(110)
            button.clicked.connect(lambda _, cat=category: self.getNews(cat))
            categoryLayout.addWidget(button, 0, i+1)

        categoryLayout.setColumnStretch(0, 1)
        categoryLayout.setColumnStretch(len(buttons)+1, 1)

        # News frame layout
        newsLayout = QGridLayout()
        self.newsOutput = QTextBrowser()
        self.newsOutput.setFont(QFont("Comic Sans", 12))
        self.newsOutput.setOpenExternalLinks(False)
        self.newsOutput.anchorClicked.connect(self.openPopup)
        newsLayout.addWidget(self.newsOutput, 0, 0)

        # Add layouts to main layout
        mainLayout.addLayout(categoryLayout, 0, 0)
        mainLayout.addLayout(newsLayout, 1, 0)

        # Set main layout
        self.setLayout(mainLayout)

    def getNews(self, type):
        newsURL = f"http://newsapi.org/v2/top-headlines?country=us&category={type}&apiKey=ff3ba8e42f024772a4424526fd246095"
        self.newsOutput.clear()
        try:
            newsInfo = (requests.get(newsURL).json())['articles']

            if newsInfo:
                for i, article in enumerate(newsInfo):
                    headline = f"\n • {article['title']}\n"
                    url = article['url']
                    self.newsOutput.append(f'<a href="{url}">{headline}</a>')

            else:
                self.newsOutput.setText("Sorry. No news available.")

        except Exception:
            QMessageBox.critical(self, 'No Internet', "Unable to connect to the internet at the moment.")

    def openPopup(self, url):
        webview = QWebEngineView()
        webview.setWindowTitle('News Article')
        webview.load(url)
        webview.show()
        self.popups.append(webview)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    newsApp = News()
    newsApp.setWindowTitle('News')
    newsApp.resize(850, 600)
    newsApp.show()
    sys.exit(app.exec_())
