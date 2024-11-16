import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QVBoxLayout, QScrollArea, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class News(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QGridLayout(self)

        # Category frame
        category = QWidget(self)
        category.setStyleSheet("background-color: #ebebeb;")
        layout.addWidget(category, 0, 0, 1, 2)

        categoryLayout = QGridLayout(category)
        categoryLayout.setColumnStretch(0, 1)
        categoryLayout.setColumnStretch(7, 1)

        generalButton = QPushButton("General", self)
        generalButton.setStyleSheet("font: bold 14px; background-color: #F7F6F5; color: #373433; border-radius: 10px;")
        generalButton.clicked.connect(lambda: self.getNews("general"))
        categoryLayout.addWidget(generalButton, 0, 1, 1, 1)

        entertainmentButton = QPushButton("Entertainment", self)
        entertainmentButton.setStyleSheet("font: bold 14px; background-color: #F7F6F5; color: #373433; border-radius: 10px;")
        entertainmentButton.clicked.connect(lambda: self.getNews("entertainment"))
        categoryLayout.addWidget(entertainmentButton, 0, 2, 1, 1)

        businessButton = QPushButton("Business", self)
        businessButton.setStyleSheet("font: bold 14px; background-color: #F7F6F5; color: #373433; border-radius: 10px;")
        businessButton.clicked.connect(lambda: self.getNews("business"))
        categoryLayout.addWidget(businessButton, 0, 3, 1, 1)

        sportsButton = QPushButton("Sports", self)
        sportsButton.setStyleSheet("font: bold 14px; background-color: #F7F6F5; color: #373433; border-radius: 10px;")
        sportsButton.clicked.connect(lambda: self.getNews("sports"))
        categoryLayout.addWidget(sportsButton, 0, 4, 1, 1)

        technologyButton = QPushButton("Technology", self)
        technologyButton.setStyleSheet("font: bold 14px; background-color: #F7F6F5; color: #373433; border-radius: 10px;")
        technologyButton.clicked.connect(lambda: self.getNews("technology"))
        categoryLayout.addWidget(technologyButton, 0, 5, 1, 1)

        healthButton = QPushButton("Health", self)
        healthButton.setStyleSheet("font: bold 14px; background-color: #F7F6F5; color: #373433; border-radius: 10px;")
        healthButton.clicked.connect(lambda: self.getNews("health"))
        categoryLayout.addWidget(healthButton, 0, 6, 1, 1)

        # News frame
        news = QWidget(self)
        news.setStyleSheet("background-color: #ebebeb;")
        layout.addWidget(news, 1, 0)

        newsLayout = QVBoxLayout(news)
        newsLayout.setAlignment(Qt.AlignTop)

        self.scrollArea = QScrollArea()
        newsLayout.addWidget(self.scrollArea)

        self.newsOutputWidget = QWidget()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.newsOutputWidget)

        self.newsOutputLayout = QVBoxLayout(self.newsOutputWidget)
        self.newsOutputLayout.setAlignment(Qt.AlignTop)

    def getNews(self, category):
        newsURL = f"http://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey=ff3ba8e42f024772a4424526fd246095"
        try:
            newsInfo = requests.get(newsURL).json()['articles']

            if newsInfo:
                self.clearLayout(self.newsOutputLayout)
                for i, article in enumerate(newsInfo):
                    headline = f"{article['title']}"
                    label = QLabel(headline, self)
                    label.setStyleSheet("font: bold 12px; border: 5px bold blue")
                    self.newsOutputLayout.addWidget(label)
                    label.linkActivated.connect(lambda url=article['url']: self.openPopup(url))

            else:
                self.clearLayout(self.newsOutputLayout)
                label = QLabel("Sorry. No news available.")
                label.setStyleSheet("font: bold 12px;")
                self.newsOutputLayout.addWidget(label)

        except Exception:
            QMessageBox.critical(self, 'No Internet', "Unable to connect to the internet at the moment.")

    def openPopup(self, url):
        QMessageBox.information(self, "URL", url)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = News()
    win.show()
    sys.exit(app.exec_())
