from PyQt5.QtWidgets import QWidget, QGridLayout, QSlider, QColorDialog
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt

from .common import apply_style, create_button

class Paint(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(15)

        self.canvas = QWidget()
        apply_style(self.canvas)
        self.canvas.setMinimumSize(710, 850)
        self.path = []
        self.penWidth = 1
        self.color = Qt.black
        self.eraserOn = False

        self.canvas.mousePressEvent = self.mousePressEvent
        self.canvas.mouseMoveEvent = self.mouseMoveEvent
        self.canvas.paintEvent = self.paintEvent

        self.layout.addWidget(self.canvas, 0, 0, 1, 4)

        buttonLayout = QGridLayout()
        self.layout.addLayout(buttonLayout, 1, 0, 1, 4)

        self.penButton = create_button("Pen", slot=self.pen)
        buttonLayout.addWidget(self.penButton, 0, 0)

        self.eraserButton = create_button("Eraser", slot=self.eraser)
        buttonLayout.addWidget(self.eraserButton, 0, 1)

        self.colorButton = create_button("Color", slot=self.chooseColor)
        buttonLayout.addWidget(self.colorButton, 0, 2)

        self.sizeSlider = QSlider(Qt.Horizontal)
        self.sizeSlider.setFixedSize(200, 50)
        self.sizeSlider.setMinimum(1)
        self.sizeSlider.setMaximum(10)
        self.sizeSlider.valueChanged.connect(self.setPenSize)
        buttonLayout.addWidget(self.sizeSlider, 0, 3)

        self.activeButton = self.penButton

    def pen(self):
        self.activeButton = self.penButton
        self.eraserOn = False

    def eraser(self):
        self.activeButton = self.eraserButton
        self.eraserOn = True

    def chooseColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color
            if self.eraserOn:
                self.pen()
                self.eraserButton.setChecked(True)

    def setPenSize(self):
        self.penWidth = self.sizeSlider.value()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.path.append({'points': [event.pos()], 'color': self.color, 'penWidth': self.penWidth, 'eraser': self.eraserOn})

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.path[-1]['points'].append(event.pos())
            self.canvas.update()

    def paintEvent(self, event):
        painter = QPainter(self.canvas)
        painter.setRenderHint(QPainter.Antialiasing)

        for line in self.path:
            pen = QPen()
            pen.setWidth(line['penWidth'])
            pen.setColor(QColor("#f0f0f0") if line['eraser'] else line['color'])
            painter.setPen(pen)

            points = line['points']
            for i in range(1, len(points)):
                painter.drawLine(points[i - 1], points[i])