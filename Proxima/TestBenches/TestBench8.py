import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import googletrans
import textblob

class Translate(QWidget):
    def __init__(self):
        super().__init__()

        self.languages = googletrans.LANGUAGES

        self.initWidgets()

    def initWidgets(self):
        # Create main layout
        mainLayout = QGridLayout()

        # Language selector layout
        languageSelectorLayout = QGridLayout()
        languageLabel = QLabel("Languages:")
        languageLabel.setFont(QFont("Comic Sans", 14))

        self.language1_ = QLineEdit()
        self.language1_.setFixedHeight(40)
        self.language1_.setText('English')
        self.language1_.setFont(QFont("Comic Sans", 12))

        self.language2_ = QLineEdit()
        self.language2_.setFixedHeight(40)
        self.language2_.setText('English')
        self.language2_.setFont(QFont("Comic Sans", 12))

        translateButton = QPushButton("Translate")
        translateButton.setFixedHeight(40)
        translateButton.setFont(QFont("Comic Sans", 14))
        translateButton.clicked.connect(self.translate)

        languageSelectorLayout.addWidget(languageLabel, 0, 0)
        languageSelectorLayout.addWidget(self.language1_, 0, 1)
        languageSelectorLayout.addWidget(self.language2_, 0, 2)
        languageSelectorLayout.addWidget(translateButton, 0, 3)

        # Translation window layout
        translateWindowLayout = QGridLayout()
        self.original = QTextEdit()
        self.original.setFixedHeight(560)
        self.translated = QTextEdit()
        self.translated.setFixedHeight(560)

        translateWindowLayout.addWidget(self.original, 0, 0)
        translateWindowLayout.addWidget(self.translated, 0, 1)

        # Add layouts to main layout
        mainLayout.addLayout(languageSelectorLayout, 0, 0)
        mainLayout.addLayout(translateWindowLayout, 1, 0)

        # Set main layout
        self.setLayout(mainLayout)

    def translate(self):
        self.translated.clear()

        try:
            language1 = self.language1_.text().lower()
            language2 = self.language2_.text().lower()
            words = textblob.TextBlob(self.original.toPlainText())

            if language1 != language2:
                language1key = next(key for key, value in self.languages.items() if value == language1)
                language2key = next(key for key, value in self.languages.items() if value == language2)
                words = words.translate(from_lang=language1key, to=language2key)

            self.translated.setPlainText(str(words))

        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator = Translate()
    translator.setWindowTitle('Translator')
    translator.resize(975, 600)
    translator.show()
    sys.exit(app.exec_())
