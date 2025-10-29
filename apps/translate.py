from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
from googletrans import Translator, LANGUAGES

from .common import apply_style, create_button

class Translate(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.languages = LANGUAGES                 
        self.translator = Translator()
        self.initUI()

    def initUI(self):
        mainLayout = QGridLayout()

        languageSelectorLayout = QGridLayout()
        languageLabel = QLabel("Languages:")
        languageLabel.setStyleSheet("font: bold 15px 'Arial';")

        self.language1_ = QLineEdit()
        self.language1_.setFixedSize(430, 50)
        self.language1_.setText('English')
        apply_style(self.language1_, font_size=15)

        self.language2_ = QLineEdit()
        self.language2_.setFixedSize(430, 50)
        self.language2_.setText('English')
        apply_style(self.language2_, font_size=15)

        translateButton = create_button("Translate", slot=self.translate, size=(100, 50), font_size=15)

        languageSelectorLayout.addWidget(languageLabel, 0, 0)
        languageSelectorLayout.addWidget(self.language1_, 0, 1)
        languageSelectorLayout.addWidget(self.language2_, 0, 2)
        languageSelectorLayout.addWidget(translateButton, 0, 3)

        translateWindowLayout = QGridLayout()
        self.original = QTextEdit()
        self.original.setFixedSize(530, 645)
        apply_style(self.original, font_size=15)
        self.translated = QTextEdit()
        self.translated.setReadOnly(True)
        self.translated.setFixedSize(530, 645)
        apply_style(self.translated, font_size=15)

        translateWindowLayout.addWidget(self.original, 0, 0)
        translateWindowLayout.addWidget(self.translated, 0, 1)

        mainLayout.addLayout(languageSelectorLayout, 0, 0)
        mainLayout.addLayout(translateWindowLayout, 1, 0)
        self.setLayout(mainLayout)

    def _name_to_code(self, s: str) -> str:
        s = s.strip().lower()
        if not s or s == "auto":
            return "auto"
        if s in self.languages:
            return s
        for code, name in self.languages.items():
            if name.lower() == s:
                return code
        aliases = {"mandarin": "zh-cn", "chinese": "zh-cn", "spanish": "es", "french": "fr",
                   "english": "en", "hindi": "hi", "tamil": "ta"}
        return aliases.get(s, s)  

    def translate(self):
        self.translated.clear()
        try:
            src = self._name_to_code(self.language1_.text())
            dest = self._name_to_code(self.language2_.text())
            text = self.original.toPlainText().strip()
            if not text:
                return
            if src == dest:
                self.translated.setPlainText(text)
                return

            res = self.translator.translate(text, src=src, dest=dest)

            import asyncio, inspect
            if inspect.isawaitable(res):
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                res = loop.run_until_complete(res)

            self.translated.setPlainText(getattr(res, "text", str(res)))

        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, 'Error', f"Translation failed: {e}")

