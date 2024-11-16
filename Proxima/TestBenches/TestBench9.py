import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from difflib import get_close_matches

class Dictionary(QWidget):
    def __init__(self):
        super().__init__()

        self.wordsData = json.load(open("words.json"))

        self.initWidgets()

    def initWidgets(self):
        # Create main layout
        mainLayout = QGridLayout()

        # Search frame layout
        searchLayout = QGridLayout()
        searchLabel = QLabel("Word:")
        searchLabel.setFont(QFont("Comic Sans", 14))

        self.word_ = QLineEdit()
        self.word_.setFixedHeight(40)
        self.word_.setFont(QFont("Comic Sans", 12))

        findButton = QPushButton("Search")
        findButton.setFixedHeight(40)
        findButton.setFont(QFont("Comic Sans", 14))
        findButton.clicked.connect(lambda: self.wordMeaning(self.word_.text()))

        searchLayout.addWidget(searchLabel, 0, 0)
        searchLayout.addWidget(self.word_, 0, 1)
        searchLayout.addWidget(findButton, 0, 2)

        # Viewer layout
        viewerLayout = QGridLayout()
        self.info = QTextEdit()
        self.info.setFont(QFont("Comic Sans", 12))
        self.info.setReadOnly(True)

        viewerLayout.addWidget(self.info, 0, 0)

        # Add layouts to main layout
        mainLayout.addLayout(searchLayout, 0, 0)
        mainLayout.addLayout(viewerLayout, 1, 0)

        # Set main layout
        self.setLayout(mainLayout)

    def printWord(self, def__):

        def_ = def__.replace("', '", "\n •  ")
        def_ = def_.replace("['", " •  ")
        def_ = def_.strip("']")

        self.info.append(def_)

    def wordMeaning(self, word):
        word = word.lower()

        self.info.clear()

        if word in self.wordsData:
            self.printWord(str(self.wordsData[word]))

        elif word.title() in self.wordsData:
            self.printWord(str(self.wordsData[word.title()]))

        elif word.upper() in self.wordsData:
            self.printWord(str(self.wordsData[word.upper()]))

        elif len(get_close_matches(word, self.wordsData.keys())) > 0:
            similarWords = get_close_matches(word, self.wordsData.keys())[0]

            ans = QMessageBox.question(self, 'Confirmation', f"Did you mean {similarWords} instead?",
                                       QMessageBox.Yes | QMessageBox.No)

            if ans == QMessageBox.Yes:
                self.wordMeaning(similarWords)

        else:
            QMessageBox.critical(self, 'Error', "This word does not exist")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dictionary = Dictionary()
    dictionary.setWindowTitle('Dictionary')
    dictionary.resize(620, 700)
    dictionary.show()
    sys.exit(app.exec_())
