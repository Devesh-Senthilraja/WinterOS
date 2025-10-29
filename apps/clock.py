from PyQt5.QtWidgets import QWidget, QGridLayout, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QPen, QColor
import math

class Clock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self._diameter = 600
        self._radius = self._diameter / 2
        layout = QGridLayout()
        self.setLayout(layout)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view, 0, 0, 1, 1)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateClock)
        self.timer.start(1000)

        self.resize(650, 650)
        self.setWindowTitle('Clock')

    def updateClock(self):
        self.scene.clear()
        now = QTime.currentTime()
        hour, minute, second = now.hour() % 12, now.minute(), now.second()

        pen = QPen(QColor("#373433"))
        pen.setWidth(2)
        diameter = self._diameter
        radius = self._radius
        self.scene.addEllipse(2, 2, diameter, diameter, pen)

        for hour_ in range(12):
            angle = hour_ * math.tau / 12 - math.pi / 2
            x = radius + 0.7 * radius * math.cos(angle)
            y = radius + 0.7 * radius * math.sin(angle)
            text = str(12 if hour_ == 0 else hour_)
            self.scene.addText(text).setPos(x, y - 10)

        for minute_ in range(60):
            angle = minute_ * math.tau / 60 - math.pi / 2
            x1 = radius + 0.8 * radius * math.cos(angle)
            y1 = radius + 0.8 * radius * math.sin(angle)
            x2 = radius + 0.9 * radius * math.cos(angle)
            y2 = radius + 0.9 * radius * math.sin(angle)
            self.scene.addLine(x1, y1, x2, y2, pen)

        center = (radius, radius)

        hourAngle = (hour + minute / 60) * math.tau / 12 - math.pi / 2
        hourX = radius + 0.5 * radius * math.cos(hourAngle)
        hourY = radius + 0.5 * radius * math.sin(hourAngle)
        self.scene.addLine(center[0], center[1], hourX, hourY, pen)

        minuteAngle = (minute + second / 60) * math.tau / 60 - math.pi / 2
        minuteX = radius + 0.7 * radius * math.cos(minuteAngle)
        minuteY = radius + 0.7 * radius * math.sin(minuteAngle)
        self.scene.addLine(center[0], center[1], minuteX, minuteY, pen)

        secondAngle = second * math.tau / 60 - math.pi / 2
        secondX = radius + 0.6 * radius * math.cos(secondAngle)
        secondY = radius + 0.6 * radius * math.sin(secondAngle)
        pen.setColor(QColor("red"))
        pen.setWidth(2)
        self.scene.addLine(center[0], center[1], secondX, secondY, pen)