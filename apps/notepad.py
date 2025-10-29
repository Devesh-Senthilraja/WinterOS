from PyQt5.QtWidgets import QWidget, QGridLayout, QTextEdit, QMessageBox, QFileDialog, QInputDialog

from .common import apply_style, create_button

class Notepad(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QGridLayout(self)
        layout.setSpacing(15)

        self.textEdit = QTextEdit()
        apply_style(self.textEdit)
        self.textEdit.setFixedSize(710, 850)
        layout.addWidget(self.textEdit, 0, 0, 1, 4)

        buttonLayout = QGridLayout()
        layout.addLayout(buttonLayout, 1, 0, 1, 4)

        for column, (text, handler) in enumerate(
            (("New", self.new), ("Open", self.open), ("Save", self.save), ("Find", self.find))
        ):
            button = create_button(text, slot=handler)
            buttonLayout.addWidget(button, 0, column)

    def new(self):
        if self.textEdit.toPlainText():
            reply = QMessageBox.question(self, 'Notepad', 'Do you want to save changes?',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.save()
            elif reply == QMessageBox.Cancel:
                return
        self.textEdit.clear()

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt)')
        if fileName:
            with open(fileName, 'r') as file:
                self.textEdit.setText(file.read())

    def save(self):
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text Files (*.txt)')
        if fileName:
            with open(fileName, 'w') as file:
                file.write(self.textEdit.toPlainText())

    def find(self):
        text, ok = QInputDialog.getText(self, 'Find Text', 'Find:')
        if ok:
            cursor = self.textEdit.document().find(text)
            if not cursor.isNull():
                cursor.select(cursor.WordUnderCursor)
                self.textEdit.setTextCursor(cursor)
            else:
                QMessageBox.information(self, '', 'Text not found.', QMessageBox.Ok)