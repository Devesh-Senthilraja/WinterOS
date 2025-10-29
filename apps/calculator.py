from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import Qt

from .common import apply_style, create_button

class Calculator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.equation = ''

        layout = QGridLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        self.output_label = QLabel('', self)
        apply_style(self.output_label)
        self.output_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.output_label.setFixedHeight(210)
        layout.addWidget(self.output_label, 0, 0, 1, 4)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('C', 4, 0), ('0', 4, 1), ('=', 4, 2), ('+', 4, 3),
        ]

        for text, row, col in buttons:
            button = create_button(text, slot=lambda _, t=text: self.on_button_click(t), size=(105, 105))
            layout.addWidget(button, row, col)

    def on_button_click(self, text):
        if text == '=':
            try:
                result = str(eval(self.equation))
                self.output_label.setText(result)
                self.equation = result
            except Exception:
                self.output_label.setText('Error')
        elif text == 'C':
            self.equation = ''
            self.output_label.setText('')
        else:
            self.equation += text
            self.output_label.setText(self.equation)