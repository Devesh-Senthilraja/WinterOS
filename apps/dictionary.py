from pathlib import Path
from difflib import get_close_matches
import json

from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QMessageBox,
)

from .common import apply_style, create_button


class Dictionary(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        words_path = Path(__file__).resolve().parents[1] / "resources" / "words.json"
        if words_path.exists():
            with words_path.open(encoding="utf-8") as fh:
                self.wordsData = json.load(fh)
        else:
            self.wordsData = {}
        self.initUI()

    def initUI(self):
        mainLayout = QGridLayout()

        searchLayout = QGridLayout()
        searchLabel = QLabel("Word:")
        searchLabel.setStyleSheet("font: bold 15px 'Arial';")

        self.word_ = QLineEdit()
        self.word_.setFixedSize(900, 50)
        apply_style(self.word_, font_size=15)

        findButton = create_button(
            "Search",
            slot=lambda: self.wordMeaning(self.word_.text()),
            size=(100, 50),
            font_size=15,
        )

        searchLayout.addWidget(searchLabel, 0, 0)
        searchLayout.addWidget(self.word_, 0, 1)
        searchLayout.addWidget(findButton, 0, 2)

        viewerLayout = QGridLayout()
        self.info = QTextEdit()
        self.info.setFixedSize(1105, 645)
        apply_style(self.info, font_size=15)
        self.info.setReadOnly(True)
        viewerLayout.addWidget(self.info, 0, 0)

        mainLayout.addLayout(searchLayout, 0, 0)
        mainLayout.addLayout(viewerLayout, 1, 0)
        self.setLayout(mainLayout)

    def display_definition(self, meaning):
        if isinstance(meaning, list):
            lines = [str(item) for item in meaning]
        else:
            lines = [str(meaning)]
        bullets = "\n".join(f" •  {line}" for line in lines if line)
        self.info.setPlainText(bullets)

    def wordMeaning(self, word):
        word = word.strip()
        self.info.clear()

        if not word:
            return

        for candidate in (word.lower(), word.title(), word.upper()):
            meaning = self.wordsData.get(candidate)
            if meaning:
                self.display_definition(meaning)
                return

        matches = get_close_matches(word.lower(), self.wordsData.keys(), n=1)
        if matches:
            similarWord = matches[0]
            ans = QMessageBox.question(
                self,
                'Confirmation',
                f"Did you mean {similarWord} instead?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if ans == QMessageBox.Yes:
                self.wordMeaning(similarWord)
        else:
            QMessageBox.critical(self, 'Error', "This word does not exist")

