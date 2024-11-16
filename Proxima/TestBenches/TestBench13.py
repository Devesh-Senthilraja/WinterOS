from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton, QGraphicsView, QGraphicsScene, QTextEdit, QLineEdit, QMessageBox, QFileDialog, QInputDialog, QColorDialog, QSlider, QSizePolicy, QTextBrowser
from PyQt5.QtCore import Qt, QPoint, QTimer, QDate, QTime, QDir, QUrl
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from datetime import datetime
from difflib import get_close_matches
import math
import random
import vlc
import cv2
import googletrans
from textblob import TextBlob
import folium
import json
import requests
import subprocess
import os
import sys

class Calculator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.equation = ''  # Equation being input by the user

        # Layout
        layout = QGridLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Output display
        self.output_label = QLabel('', self)
        self.output_label.setStyleSheet("background-color: #f0f0f0; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        self.output_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.output_label.setFixedHeight(210) #150
        layout.addWidget(self.output_label, 0, 0, 1, 4)

        # Buttons
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('C', 4, 0), ('0', 4, 1), ('=', 4, 2), ('+', 4, 3),
        ]

        for text, row, col in buttons:
            button = QPushButton(text, self)
            button.setStyleSheet("background-color: #d9d9d9; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
            button.setFixedSize(105, 105) # 70, 70
            button.clicked.connect(lambda _, t=text: self.on_button_click(t))
            layout.addWidget(button, row, col)

    def on_button_click(self, text):
        if text == '=':
            try:
                result = str(eval(self.equation))
                self.output_label.setText(result)
                self.equation = result
            except Exception as e:
                self.output_label.setText('Error')
        elif text == 'C':
            self.equation = ''
            self.output_label.setText('')
        else:
            self.equation += text
            self.output_label.setText(self.equation)

class Calendar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        today = QDate.currentDate()
        self.month = today.month()
        self.year = today.year()
        self.today = today
        self.initUI()
    
    def initUI(self):
        # Main layout
        main_layout = QGridLayout(self)
        
        # 1st Layout for navigation and month/year display
        nav_layout = QGridLayout()
        self.prev_month_btn = QPushButton("<")
        self.next_month_btn = QPushButton(">")
        self.month_year_label = QLabel()
        self.month_year_label.setAlignment(Qt.AlignCenter)

        # Styles and sizing for buttons
        btn_style = "background-color: #d9d9d9; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;"
        self.prev_month_btn.setStyleSheet(btn_style)
        self.next_month_btn.setStyleSheet(btn_style)
        self.prev_month_btn.setFixedSize(70, 50)
        self.next_month_btn.setFixedSize(70, 50)

        # Style and sizing for month/year label
        month_label_style = "background-color: #ffffff; font: bold 40px 'Arial'; border-radius: 10px;"
        self.month_year_label.setStyleSheet(month_label_style)
        self.month_year_label.setMinimumHeight(50)

        nav_layout.addWidget(self.prev_month_btn, 0, 0)
        nav_layout.addWidget(self.month_year_label, 0, 1)
        nav_layout.addWidget(self.next_month_btn, 0, 2)
        nav_layout.setColumnStretch(0, 1)
        nav_layout.setColumnStretch(1, 8)
        nav_layout.setColumnStretch(2, 1)

        # Unified Layout for days of the week and calendar days
        calendar_layout = QGridLayout()
        self.days_of_week = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        day_label_style = "background-color: #ffffff; font: bold 20px 'Arial'; border-radius: 10px;"
        day_style = "background-color: #f0f0f0; font: bold 20px 'Arial'; border-radius: 10px; padding: 10px;"

        # Add day labels
        for i, day in enumerate(self.days_of_week):
            label = QLabel(day)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(day_label_style)
            label.setMinimumHeight(50)
            calendar_layout.addWidget(label, 0, i, 1, 1)  # First row for day names
            calendar_layout.setColumnStretch(i, 0)  # Set equal column width
            calendar_layout.setColumnMinimumWidth(i, 150)  # Set minimum width to 150 pixels

        # Add day numbers
        self.day_labels = []
        for row in range(1, 7):  # Rows 1 to 6 for days of the month
            week = []
            for col in range(7):  # 7 columns for each day
                label = QLabel("")
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet(day_style)
                label.setMinimumHeight(90)
                week.append(label)
                calendar_layout.addWidget(label, row, col, 1, 1)
                calendar_layout.setColumnStretch(col, 0)  # Set equal column width
            self.day_labels.append(week)

        self.printMonthYear(self.month, self.year)
        self.monthGenerator(self.dayMonthStarts(self.month, self.year), self.daysInMonth(self.month, self.year))

        # Add sublayouts to main layout
        main_layout.addLayout(nav_layout, 0, 0)
        main_layout.addLayout(calendar_layout, 1, 0)

        self.setLayout(main_layout)

        self.prev_month_btn.clicked.connect(lambda: self.switchMonths(-1))
        self.next_month_btn.clicked.connect(lambda: self.switchMonths(1))

    def printMonthYear(self, month, year):
        date = QDate(year, month, 1)
        self.month_year_label.setText(f"{date.longMonthName(month)} {year}")

    def switchMonths(self, direction):
        if self.month == 12 and direction == 1:
            self.month, self.year = 1, self.year + 1
        elif self.month == 1 and direction == -1:
            self.month, self.year = 12, self.year - 1
        else:
            self.month += direction
        
        self.printMonthYear(self.month, self.year)
        self.monthGenerator(self.dayMonthStarts(self.month, self.year), self.daysInMonth(self.month, self.year))  # Add your method for generating the month

    def monthGenerator(self, startDate, numberOfDays):
        # Clear existing day labels
        for week in self.day_labels:
            for label in week:
                label.setText("")  # Clear the previous month's days

        # Initialize day count and row and column tracking
        index = 0
        day = 1
        for row in range(6):
            for col in range(7):
                # Fill in the day number if we are within the month's date range
                if index >= startDate and index <= startDate + numberOfDays - 1:
                    self.day_labels[row][col].setText(str(day))

                    # Highlight today's date
                    if QDate(self.year, self.month, day) == self.today:
                        self.day_labels[row][col].setStyleSheet("background-color: #787878; font: bold 20px 'Arial'; border-radius: 10px; padding: 10px;")
                    else:
                        self.day_labels[row][col].setStyleSheet("background-color: #f0f0f0; font: bold 20px 'Arial'; border-radius: 10px; padding: 10px;")
                    
                    day += 1
                index += 1

    def isLeapYear(self, year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def dayMonthStarts(self, month, year):
        lastTwoYear = year - 2000
        calculation = lastTwoYear // 4 + 1
        if month == 1 or month == 10:
            calculation += 1
        elif month in [2, 3, 11]:
            calculation += 4
        elif month == 5:
            calculation += 2
        elif month == 6:
            calculation += 5
        elif month == 8:
            calculation += 3
        elif month in [9, 12]:
            calculation += 6
        leapYear = self.isLeapYear(year)
        if leapYear and (month == 1 or month == 2):
            calculation -= 1
        calculation += 6 + lastTwoYear
        return calculation % 7

    def daysInMonth(self, month, year):
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month in [4, 6, 9, 11]:
            return 30
        else:
            leapYear = self.isLeapYear(year)
            return 29 if leapYear else 28
        
class Clock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
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
        self.scene.addEllipse(2, 2, 600, 600, pen)

        for hour_ in range(12):
            angle = hour_ * math.pi / 6 - math.pi / 2
            x = 600 / 2 + 0.7 * 600 / 2 * math.cos(angle)
            y = 600 / 2 + 0.7 * 600 / 2 * math.sin(angle)
            if hour_ == 0:
                self.scene.addText(str(hour_ + 12)).setPos(x, y - 10)
            else:
                self.scene.addText(str(hour_)).setPos(x, y)

        for minute_ in range(60):
            angle = minute_ * math.pi / 30 - math.pi / 2
            x1, y1 = 600 / 2 + 0.8 * 600 / 2 * math.cos(angle), 600 / 2 + 0.8 * 600 / 2 * math.sin(angle)
            x2, y2 = 600 / 2 + 0.9 * 600 / 2 * math.cos(angle), 600 / 2 + 0.9 * 600 / 2 * math.sin(angle)
            if minute_ % 5 == 0:
                self.scene.addLine(x1, y1, x2, y2, pen)
            else:
                self.scene.addLine(x1, y1, x2, y2, pen)

        hourAngle = (hour + minute / 60) * math.pi / 6 - math.pi / 2
        hourX, hourY = 600 / 2 + 0.5 * 600 / 2 * math.cos(hourAngle), 600 / 2 + 0.5 * 600 / 2 * math.sin(hourAngle)
        self.scene.addLine(600 / 2, 600 / 2, hourX, hourY, pen)

        minuteAngle = (minute + second / 60) * math.pi / 30 - math.pi / 2
        minuteX, minuteY = 600 / 2 + 0.7 * 600 / 2 * math.cos(minuteAngle), 600 / 2 + 0.7 * 600 / 2 * math.sin(minuteAngle)
        self.scene.addLine(600 / 2, 600 / 2, minuteX, minuteY, pen)

        secondAngle = second * math.pi / 30 - math.pi / 2
        secondX, secondY = 600 / 2 + 0.6 * 600 / 2 * math.cos(secondAngle), 600 / 2 + 0.6 * 600 / 2 * math.sin(secondAngle)
        pen.setColor(QColor("red"))
        pen.setWidth(2)
        self.scene.addLine(600 / 2, 600 / 2, secondX, secondY, pen)

class Notepad(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        layout = QGridLayout(self)
        layout.setSpacing(15)

        self.textEdit = QTextEdit()
        self.textEdit.setStyleSheet("background-color: #f0f0f0; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        self.textEdit.setFixedSize(710, 850)  # Set fixed size for QTextEdit
        layout.addWidget(self.textEdit, 0, 0, 1, 4)

        buttonLayout = QGridLayout()
        layout.addLayout(buttonLayout, 1, 0, 1, 4)

        btn_style = "background-color: #d9d9d9; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;"

        newButton = QPushButton('New')
        newButton.setStyleSheet(btn_style)
        newButton.setFixedSize(100, 50)  # Set fixed size for QPushButton
        newButton.clicked.connect(self.new)
        buttonLayout.addWidget(newButton, 0, 0)

        openButton = QPushButton('Open')
        openButton.setStyleSheet(btn_style)
        openButton.setFixedSize(100, 50)  # Set fixed size for QPushButton
        openButton.clicked.connect(self.open)
        buttonLayout.addWidget(openButton, 0, 1)

        saveButton = QPushButton('Save')
        saveButton.setStyleSheet(btn_style)
        saveButton.setFixedSize(100, 50)  # Set fixed size for QPushButton
        saveButton.clicked.connect(self.save)
        buttonLayout.addWidget(saveButton, 0, 2)

        findButton = QPushButton('Find')
        findButton.setStyleSheet(btn_style)
        findButton.setFixedSize(100, 50)  # Set fixed size for QPushButton
        findButton.clicked.connect(self.find)
        buttonLayout.addWidget(findButton, 0, 3)

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

# Implement new, open and save
class Paint(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(15)

        self.canvas = QWidget()
        self.canvas.setStyleSheet("background-color: #f0f0f0; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
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

        btn_style = "background-color: #d9d9d9; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;"

        self.penButton = QPushButton("Pen")
        self.penButton.setStyleSheet(btn_style)
        self.penButton.setFixedSize(100, 50)
        self.penButton.clicked.connect(self.pen)
        buttonLayout.addWidget(self.penButton, 0, 0)

        self.eraserButton = QPushButton("Eraser")
        self.eraserButton.setStyleSheet(btn_style)
        self.eraserButton.setFixedSize(100, 50)
        self.eraserButton.clicked.connect(self.eraser)
        buttonLayout.addWidget(self.eraserButton, 0, 1)

        self.colorButton = QPushButton("Color")
        self.colorButton.setStyleSheet(btn_style)
        self.colorButton.setFixedSize(100, 50)
        self.colorButton.clicked.connect(self.chooseColor)
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
            if line['eraser']:
                pen.setColor(QColor("#f0f0f0"))
            else:
                pen.setColor(line['color'])
            painter.setPen(pen)

            points = line['points']
            for i in range(1, len(points)):
                painter.drawLine(points[i - 1], points[i])

class ImageViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.originalHeight, self.originalWidth = None, None

        self.initUI()

    def initUI(self):
        main_layout = QGridLayout(self)
        main_layout.setSpacing(15)

        # Image Label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)  # Center the label contents
        self.image_label.setFixedSize(1105, 635)
        self.image_label.setStyleSheet("background-color: #f0f0f0; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")  # Rounded corners style
        main_layout.addWidget(self.image_label, 0, 0, 1, 3)

        btn_style = "background-color: #d9d9d9; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;"

        # Buttons Layout
        buttons_layout = QGridLayout()

        # Zoom In Button
        zoom_in_button = QPushButton("Zoom In")
        zoom_in_button.setFixedSize(100, 50)
        zoom_in_button.clicked.connect(self.zoom_in)
        zoom_in_button.setStyleSheet(btn_style)
        buttons_layout.addWidget(zoom_in_button, 1, 0)

        # Browse Button
        browse_button = QPushButton("Browse")
        browse_button.setFixedSize(100, 50)
        browse_button.setStyleSheet(btn_style)
        browse_button.clicked.connect(self.open_image)
        buttons_layout.addWidget(browse_button, 1, 1)

        # Zoom Out Button
        zoom_out_button = QPushButton("Zoom Out")
        zoom_out_button.setFixedSize(100, 50)
        zoom_out_button.clicked.connect(self.zoom_out)
        zoom_out_button.setStyleSheet(btn_style)
        buttons_layout.addWidget(zoom_out_button, 1, 2)

        main_layout.addLayout(buttons_layout, 1, 0, 1, 3)

        self.setLayout(main_layout)

    def open_image(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")

        if file_path:
            image = QImage(file_path)
            if not image.isNull():
                pixmap = QPixmap.fromImage(image)
                pixmap = self.scale_image(pixmap)
                self.image_label.setPixmap(pixmap)
                self.originalHeight, self.originalWidth = pixmap.height(), pixmap.width()

    def scale_image(self, pixmap):
        window_size = self.size()
        width_ratio = window_size.width() / pixmap.width()
        height_ratio = window_size.height() / pixmap.height()

        if width_ratio > 1 and height_ratio > 1:
            return pixmap
        else:
            if width_ratio < height_ratio:
                scaled_width = window_size.width()
                scaled_height = int(pixmap.height() * width_ratio)
            else:
                scaled_width = int(pixmap.width() * height_ratio)
                scaled_height = window_size.height()

            return pixmap.scaled(scaled_width, scaled_height, Qt.KeepAspectRatio)
        
    def zoom_in(self):
        pixmap = self.image_label.pixmap()
        if pixmap:
            new_width = int(pixmap.width() * 1.5)
            new_height = int(pixmap.height() * 1.5)
            pixmap = pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)

    def zoom_out(self):
        pixmap = self.image_label.pixmap()
        if pixmap:
            new_width = int(pixmap.width() * 0.5)
            new_height = int(pixmap.height() * 0.5)

            if new_width <= self.originalWidth or new_height <= self.originalHeight:
                new_width, new_height = self.originalWidth, self.originalHeight

            pixmap = pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)

# Implement timeline
class VideoPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        main_layout = QGridLayout(self)
        main_layout.setSpacing(15)

        # Initialize VLC player
        self.vlcInstance = vlc.Instance()
        self.mediaPlayer = self.vlcInstance.media_player_new()

        # Set up a widget for video output
        self.videoFrame = QWidget(self)
        self.videoFrame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.videoFrame.setFixedSize(1105, 635)
        self.videoFrame.setStyleSheet("background-color: #f0f0f0; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")

        if sys.platform.startswith('linux'):  # for Linux using the X Window System
            self.mediaPlayer.set_xwindow(self.videoFrame.winId())
        elif sys.platform == "win32":  # for Windows
            self.mediaPlayer.set_hwnd(self.videoFrame.winId())

        main_layout.addWidget(self.videoFrame, 0, 0, 1, 4)

        btn_style = "background-color: #d9d9d9; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;"

        # Buttons Layout
        buttons_layout = QGridLayout()

        # Browse Button
        browse_button = QPushButton("Browse")
        browse_button.setFixedSize(100, 50)
        browse_button.clicked.connect(self.open_video)
        browse_button.setStyleSheet(btn_style)
        buttons_layout.addWidget(browse_button, 0, 0)

        # Play/Pause Button
        self.play_pause_button = QPushButton("Play")
        self.play_pause_button.setFixedSize(100, 50)
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        self.play_pause_button.setStyleSheet(btn_style)
        buttons_layout.addWidget(self.play_pause_button, 0, 1)

        # Volume Up Button
        volume_up_button = QPushButton("Volume Up")
        volume_up_button.setFixedSize(160, 50)
        volume_up_button.clicked.connect(self.volume_up)
        volume_up_button.setStyleSheet(btn_style)
        buttons_layout.addWidget(volume_up_button, 0, 2)

        # Volume Down Button
        volume_down_button = QPushButton("Volume Down")
        volume_down_button.setFixedSize(160, 50)
        volume_down_button.clicked.connect(self.volume_down)
        volume_down_button.setStyleSheet(btn_style)
        buttons_layout.addWidget(volume_down_button, 0, 3)

        main_layout.addLayout(buttons_layout, 1, 0, 1, 4)

    def open_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Movie", QDir.homePath())
        if file_path:
            media = self.vlcInstance.media_new(file_path)
            self.mediaPlayer.set_media(media)
            self.mediaPlayer.play()
            self.play_pause_button.setText("Pause")

    def toggle_play_pause(self):
        if self.mediaPlayer.is_playing():
            self.mediaPlayer.pause()
            self.play_pause_button.setText("Play")
        else:
            self.mediaPlayer.play()
            self.play_pause_button.setText("Pause")

    def volume_up(self):
        volume = self.mediaPlayer.audio_get_volume()
        self.mediaPlayer.audio_set_volume(min(volume + 10, 100))

    def volume_down(self):
        volume = self.mediaPlayer.audio_get_volume()
        self.mediaPlayer.audio_set_volume(max(volume - 10, 0))

# Implement timeline
class AudioPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        grid_layout = QGridLayout(self)
        grid_layout.setSpacing(15)

        # Thumbnail Label
        thumbnail = QLabel(self)
        thumbnail.setFixedSize(625, 560)  # Fixed size for thumbnail
        thumbnail.setStyleSheet("background-color: #f0f0f0; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")  # Border to visualize the QLabel if no image is loaded
        pixmap = QPixmap("audio.png")
        # Scale the image to fit the size of the label while preserving its aspect ratio
        scaled_pixmap = pixmap.scaled(thumbnail.size(), aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        # Set the scaled pixmap as the label's pixmap
        thumbnail.setPixmap(scaled_pixmap)
        grid_layout.addWidget(thumbnail, 0, 0, 1, 4)  # Span across 4 columns

        # Initialize VLC player for audio
        self.vlcInstance = vlc.Instance()
        self.mediaPlayer = self.vlcInstance.media_player_new()

        btn_style = "background-color: #d9d9d9; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;"

        button_layout = QGridLayout()

        # Browse Button
        browse_button = QPushButton("Browse")
        browse_button.setFixedSize(100, 50)
        browse_button.clicked.connect(self.open_audio)
        browse_button.setStyleSheet(btn_style)
        button_layout.addWidget(browse_button, 0, 0)

        # Play/Pause Button
        self.play_pause_button = QPushButton("Play")
        self.play_pause_button.setFixedSize(100, 50)
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        self.play_pause_button.setStyleSheet(btn_style)
        button_layout.addWidget(self.play_pause_button, 0, 1)

        # Volume Up Button
        volume_up_button = QPushButton("Volume Up")
        volume_up_button.setFixedSize(160, 50)
        volume_up_button.clicked.connect(self.volume_up)
        volume_up_button.setStyleSheet(btn_style)
        button_layout.addWidget(volume_up_button, 0, 2)

        # Volume Down Button
        volume_down_button = QPushButton("Volume Down")
        volume_down_button.setFixedSize(160, 50)
        volume_down_button.clicked.connect(self.volume_down)
        volume_down_button.setStyleSheet(btn_style)
        button_layout.addWidget(volume_down_button, 0, 3)

        grid_layout.addLayout(button_layout, 1, 0, 1, 4)


    def open_audio(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Audio", QDir.homePath(), "Audio Files (*.mp3 *.wav *.flac)")
        if file_path:
            media = self.vlcInstance.media_new(file_path)
            self.mediaPlayer.set_media(media)
            self.mediaPlayer.play()
            self.play_pause_button.setText("Pause")
            
    def toggle_play_pause(self):
        if self.mediaPlayer.is_playing():
            self.mediaPlayer.pause()
            self.play_pause_button.setText("Play")
        else:
            self.mediaPlayer.play()
            self.play_pause_button.setText("Pause")

    def volume_up(self):
        volume = self.mediaPlayer.audio_get_volume()
        self.mediaPlayer.audio_set_volume(min(volume + 10, 100))

    def volume_down(self):
        volume = self.mediaPlayer.audio_get_volume()
        self.mediaPlayer.audio_set_volume(max(volume - 10, 0))

class Camera(QWidget):
    def __init__(self, parent=None):
        super(Camera, self).__init__(parent)

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1080)  # Set the width
        self.cap.set(4, 720)   # Set the height
        self.existingIDs = []

        self.initUI()

    def initUI(self):
        grid = QGridLayout(self)  # Main layout

        # Frame for showing video feed
        self.photoViewer = QLabel(self)
        self.photoViewer.setFixedSize(1105, 635)
        self.photoViewer.setStyleSheet("background-color: #f0f0f0; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        grid.addWidget(self.photoViewer, 0, 0, 1, 3)  # Row 0, Column 0, Span 1 row, Span 3 columns

        # Capture button
        captureButton = QPushButton("Capture", self)
        captureButton.setStyleSheet("background-color: #d9d9d9; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        captureButton.setFixedSize(100, 50)
        captureButton.clicked.connect(self.capture)
        grid.addWidget(captureButton, 1, 1)  # Row 1, Column 1

        # Add stretches to layout to center the button horizontally
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(2, 1)

        # Set up a timer to pull data from the video capture
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showFrames)
        self.timer.start(20)  # Update interval

    def checkID(self):
        if not os.path.exists("Photos"):
            os.mkdir("Photos")
        for x in os.listdir("Photos"):
            if x.endswith(".jpg"):
                id = x.replace("picture", "")
                id = id.replace(".png", "")
                self.existingIDs.append(id)

    def capture(self):
        self.checkID()
        ret, frame = self.cap.read()
        id = str(random.randint(1, 1000))
        while id in self.existingIDs:
            id = str(random.randint(1, 1000))
        if ret:
            outpath = os.path.join("Photos", f"picture{id}.png")
            cv2.imwrite(outpath, frame)
            cv2.waitKey(0)

    def showFrames(self):
        ret, frame = self.cap.read()
        if ret:
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(self.photoViewer.width(), self.photoViewer.height(), Qt.KeepAspectRatio)
            self.photoViewer.setPixmap(QPixmap.fromImage(p))

class Terminal(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parentFrame = parent
        self.initUI()

    def initUI(self):
        layout = QGridLayout(self)

        # Controls frame
        controls = QGridLayout()
        layout.addLayout(controls, 0, 0)

        address_label = QLabel("WinterOS:~", self)
        address_label.setStyleSheet("font: bold 15px 'Arial';")
        controls.addWidget(address_label, 0, 0)

        self.commandLine = QLineEdit(self)
        self.commandLine.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        self.commandLine.setFixedSize(900, 50)
        controls.addWidget(self.commandLine, 0, 1)

        runButton = QPushButton("Run", self)
        runButton.setStyleSheet("background-color: #d9d9d9; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        runButton.setFixedSize(100, 50)
        runButton.clicked.connect(self.runCommand)
        controls.addWidget(runButton, 0, 2)

        # Viewer frame
        viewer = QTextEdit(self)
        viewer.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        viewer.setFixedSize(1105, 645)
        layout.addWidget(viewer, 1, 0)

        self.commandOutput = viewer

    def runCommand(self):
        command = self.commandLine.text()
        self.commandLine.clear()

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        self.commandOutput.append("WinterOS:~ " + command)

        cmdResults, cmdErrors = process.communicate()
        self.commandOutput.append(cmdResults.decode())
        self.commandOutput.append(cmdErrors.decode())

class Weather(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QGridLayout(self)

        # Search frame
        search = QWidget(self)
        layout.addWidget(search, 1, 0, 1, 2)

        searchLayout = QGridLayout(search)
        searchLayout.setColumnStretch(1, 1)

        locationLabel = QLabel("Location:", self)
        locationLabel.setStyleSheet("font: bold 15px 'Arial';")
        searchLayout.addWidget(locationLabel, 0, 0)

        self.cityValue = QLineEdit(self)
        self.cityValue.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        self.cityValue.setFixedSize(900, 50)
        searchLayout.addWidget(self.cityValue, 0, 1)

        searchButton = QPushButton("Search", self)
        searchButton.setStyleSheet("background-color: #d9d9d9; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        searchButton.setFixedSize(100, 50)
        searchButton.clicked.connect(self.getWeather)
        searchLayout.addWidget(searchButton, 0, 2)

        # Weather frame
        weather = QWidget(self)
        weather.setStyleSheet("background-color: #f0f0f0; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        weather.setFixedSize(465, 620)
        layout.addWidget(weather, 2, 0)

        weatherLayout = QGridLayout(weather)
        self.temperatureLabel = QLabel("", self)
        self.temperatureLabel.setStyleSheet("font: bold 75px; color: black; border: 1px solid #f0f0f0;")
        weatherLayout.addWidget(self.temperatureLabel, 0, 0)

        # Weather info frame
        weatherInfo = QWidget(self)
        weatherInfo.setStyleSheet("background-color: #f0f0f0; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        weatherInfo.setFixedSize(630, 620)
        layout.addWidget(weatherInfo, 2, 1)

        weatherInfoLayout = QGridLayout(weatherInfo)
        self.humidityLabel = QLabel("", self)
        self.humidityLabel.setStyleSheet("border: 1px solid #f0f0f0;")
        self.pressureLabel = QLabel("", self)
        self.pressureLabel.setStyleSheet("border: 1px solid #f0f0f0;")
        self.cloudsLabel = QLabel("", self)
        self.cloudsLabel.setStyleSheet("border: 1px solid #f0f0f0;")
        self.sunriseLabel = QLabel("", self)
        self.sunriseLabel.setStyleSheet("border: 1px solid #f0f0f0;")
        self.sunsetLabel = QLabel("", self)
        self.sunsetLabel.setStyleSheet(" border: 1px solid #f0f0f0;")

        weatherInfoLayout.addWidget(self.humidityLabel, 0, 0)
        weatherInfoLayout.addWidget(self.pressureLabel, 1, 0)
        weatherInfoLayout.addWidget(self.cloudsLabel, 2, 0)
        weatherInfoLayout.addWidget(self.sunriseLabel, 3, 0)
        weatherInfoLayout.addWidget(self.sunsetLabel, 4, 0)

    def timeZone(self, utc_tz):
        local_time = datetime.utcfromtimestamp(utc_tz)
        return local_time.time()

    def getWeather(self):
        cityName = self.cityValue.text()
        weatherURL = 'http://api.openweathermap.org/data/2.5/weather?q=' + cityName + '&appid=ec44b8c08ba22cabb5c57e7ba03f7851'
        try:
            weatherInfo = requests.get(weatherURL).json()

            if weatherInfo['cod'] == 200:
                kelvin = 273

                temp = int(weatherInfo['main']['temp'] - kelvin)
                pressure = weatherInfo['main']['pressure']
                humidity = weatherInfo['main']['humidity']
                sunrise = weatherInfo['sys']['sunrise']
                sunset = weatherInfo['sys']['sunset']
                timezone = weatherInfo['timezone']
                clouds = weatherInfo['clouds']['all']
 
                sunriseTime = self.timeZone(sunrise + timezone)
                sunsetTime = self.timeZone(sunset + timezone)

                self.temperatureLabel.setText(str(temp)+"°C")
                self.humidityLabel.setText("Humidity: "+str(humidity)+"%")
                self.pressureLabel.setText("Pressure: "+str(pressure)+" hPa")
                self.cloudsLabel.setText("Clouds: "+str(clouds)+"%")
                self.sunriseLabel.setText("Sunrise: "+str(sunriseTime))
                self.sunsetLabel.setText("Sunset: "+str(sunsetTime))

            else: 
                self.temperatureLabel.setText("")
                self.humidityLabel.setText("")
                self.pressureLabel.setText("")
                self.cloudsLabel.setText("")
                self.sunriseLabel.setText("")
                self.sunsetLabel.setText("")
                QMessageBox.critical(self, cityName + " not found", "Please enter a valid city name.")
        except Exception: 
            QMessageBox.critical(self, 'No Internet', "Unable to connect to the internet at the moment.")

class Translate(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.languages = googletrans.LANGUAGES
        self.initUI()

    def initUI(self):
        # Create main layout
        mainLayout = QGridLayout()

        # Language selector layout
        languageSelectorLayout = QGridLayout()
        languageLabel = QLabel("Languages:")
        languageLabel.setStyleSheet("font: bold 15px 'Arial';")

        self.language1_ = QLineEdit()
        self.language1_.setFixedSize(430, 50)
        self.language1_.setText('English')
        self.language1_.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")

        self.language2_ = QLineEdit()
        self.language2_.setFixedSize(430, 50)
        self.language2_.setText('English')
        self.language2_.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")

        translateButton = QPushButton("Translate")
        translateButton.setFixedSize(100, 50)
        translateButton.setStyleSheet("background-color: #d9d9d9; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        translateButton.clicked.connect(self.translate)

        languageSelectorLayout.addWidget(languageLabel, 0, 0)
        languageSelectorLayout.addWidget(self.language1_, 0, 1)
        languageSelectorLayout.addWidget(self.language2_, 0, 2)
        languageSelectorLayout.addWidget(translateButton, 0, 3)

        # Translation window layout
        translateWindowLayout = QGridLayout()
        self.original = QTextEdit()
        self.original.setFixedSize(530, 645)
        self.original.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        self.translated = QTextEdit()
        self.translated.setFixedSize(530, 645)
        self.translated.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")

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
            language1 = self.language1_.text().strip().lower()
            language2 = self.language2_.text().strip().lower()
            original_text = self.original.toPlainText().strip()
            words = TextBlob(original_text)

            if language1 != language2:
                language1key = next(key for key, value in self.languages.items() if value.lower() == language1)
                language2key = next(key for key, value in self.languages.items() if value.lower() == language2)
                words = words.translate(from_lang=language1key, to=language2key)

            self.translated.setPlainText(str(words))

        except StopIteration:
            QMessageBox.critical(self, 'Error', 'Invalid language code')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

class Dictionary(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.wordsData = json.load(open("words.json"))
        self.initUI()

    def initUI(self):
        # Create main layout
        mainLayout = QGridLayout()

        # Search frame layout
        searchLayout = QGridLayout()
        searchLabel = QLabel("Word:")
        searchLabel.setStyleSheet("font: bold 15px 'Arial';")

        self.word_ = QLineEdit()
        self.word_.setFixedSize(900, 50)
        self.word_.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")

        findButton = QPushButton("Search")
        findButton.setFixedSize(100, 50)
        findButton.setStyleSheet("background-color: #d9d9d9; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        findButton.clicked.connect(lambda: self.wordMeaning(self.word_.text()))

        searchLayout.addWidget(searchLabel, 0, 0)
        searchLayout.addWidget(self.word_, 0, 1)
        searchLayout.addWidget(findButton, 0, 2)

        # Viewer layout
        viewerLayout = QGridLayout()
        self.info = QTextEdit()
        self.info.setFixedSize(1105, 645)
        self.info.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
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

#Implement connection to Browser
class News(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.popups = []
        self.initUI()

    def initUI(self):
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
            button.setStyleSheet("background-color: #d9d9d9; font: bold 13px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
            button.setFixedSize(150, 50)
            button.clicked.connect(lambda _, cat=category: self.getNews(cat))
            categoryLayout.addWidget(button, 0, i+1)

        categoryLayout.setColumnStretch(0, 1)
        categoryLayout.setColumnStretch(len(buttons)+1, 1)

        # News frame layout
        newsLayout = QGridLayout()
        self.newsOutput = QTextBrowser()
        self.newsOutput.setFixedSize(1105, 645)
        self.newsOutput.setStyleSheet("background-color: #f0f0f0; font: bold 17px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
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
                    self.newsOutput.append(f'<a href="{url}">{headline}</a><br>')

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

class Browser(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        # Create main layout
        mainLayout = QGridLayout(self)

        # Top layout for controls
        topLayout = QGridLayout()
        
        # Bottom layout for the web view
        bottomLayout = QGridLayout()

        # WebEngineView
        self.webView = QWebEngineView()
        self.webView.setFixedSize(1105, 645)
        self.webView.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        self.webView.setUrl(QUrl("https://www.google.com"))

        # Buttons and LineEdit
        backButton = QPushButton()
        backButton.setIcon(QIcon("Icons/arrow1.png"))  # Use appropriate path or resource
        backButton.setFixedHeight(50)
        backButton.clicked.connect(self.webView.back)

        forwardButton = QPushButton()
        forwardButton.setIcon(QIcon("Icons/arrow2.png"))  # Use appropriate path or resource
        forwardButton.setFixedHeight(50)
        forwardButton.clicked.connect(self.webView.forward)

        homeButton = QPushButton()
        homeButton.setIcon(QIcon("Icons/home.png"))  # Use appropriate path or resource
        homeButton.setFixedHeight(50)
        homeButton.clicked.connect(lambda: self.webView.setUrl(QUrl("https://www.google.com")))

        self.urlLineEdit = QLineEdit()
        self.urlLineEdit.setFixedSize(850, 50)
        self.urlLineEdit.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        
        goButton = QPushButton("Go")
        goButton.setFixedSize(100, 50)
        goButton.setStyleSheet("background-color: #d9d9d9; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        goButton.clicked.connect(self.navigate)

        # Add widgets to top layout
        topLayout.addWidget(backButton, 0, 0)
        topLayout.addWidget(forwardButton, 0, 1)
        topLayout.addWidget(homeButton, 0, 2)
        topLayout.addWidget(self.urlLineEdit, 0, 3)
        topLayout.addWidget(goButton, 0, 4)

        # Add web view to bottom layout
        bottomLayout.addWidget(self.webView, 0, 0)

        # Add layouts to main layout
        mainLayout.addLayout(topLayout, 0, 0)
        mainLayout.addLayout(bottomLayout, 1, 0)

    def navigate(self):
        url = self.urlLineEdit.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://www.google.com/search?q=" + url
        self.webView.setUrl(QUrl(url))

class Map(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        # Create the main grid layout
        main_layout = QGridLayout(self)

        # Create search bar components
        location_label = QLabel("Location:", self)
        location_label.setStyleSheet("font: bold 15px 'Arial';")
        self.address_input = QLineEdit(self)
        self.address_input.setFixedSize(900, 50)
        self.address_input.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        self.address_input.setFixedHeight(40)

        search_button = QPushButton("Search", self)
        search_button.setFixedSize(100, 50)
        search_button.setStyleSheet("background-color: #d9d9d9; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        search_button.clicked.connect(self.update_map)

        # Add search bar components to the main layout
        main_layout.addWidget(location_label, 0, 0, 1, 1)
        main_layout.addWidget(self.address_input, 0, 1, 1, 8)
        main_layout.addWidget(search_button, 0, 9, 1, 1)

        # Create map frame and add it to the main layout
        self.map_view = QWebEngineView(self)
        self.map_view.setFixedSize(1105, 645)
        self.map_view.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        main_layout.addWidget(self.map_view, 1, 0, 1, 10)
        
        # Update the map with the initial location
        self.update_map(initial=True)

    def update_map(self, initial=False):
        if initial:
            address = "Pleasanton, CA"
        else:
            address = self.address_input.text()

        # Create the folium map centered on the given address
        self.create_map(address)

    def create_map(self, address):
        # Use geopy to get the coordinates for the address
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="map_app")
        location = geolocator.geocode(address)

        # Check if the location is found
        if location:
            map = folium.Map(location=[location.latitude, location.longitude], zoom_start=15)
            folium.Marker([location.latitude, location.longitude], tooltip=address).add_to(map)
        else:
            map = folium.Map(location=[0, 0], zoom_start=2)
            folium.Marker([0, 0], tooltip="Location not found").add_to(map)

        # Save the map as an HTML file
        map_file = 'map.html'
        map.save(map_file)

        # Set the map file to the QWebEngineView
        self.map_view.setUrl(QUrl.fromLocalFile(os.path.abspath(map_file)))

class Window(QWidget):
    def __init__(self, width, height, title, app_widget_class):
        super().__init__()
        self.width_ = width
        self.height_ = height
        self.title = title
        self.app_widget_class = app_widget_class
        self.initUI()

    def initUI(self):
        # Set the fixed size of the window
        self.setFixedSize(self.width_, self.height_)
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove window borders
        self.setAttribute(Qt.WA_TranslucentBackground) # Allow background transparency

        # Create a grid layout and set it to the window
        layout = QGridLayout()
        layout.setSpacing(0)  # Remove padding between columns
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.setLayout(layout)

        # Create the title bar and application space
        title_bar = QWidget(self)
        title_bar.setStyleSheet("background-color: gray; border-top-left-radius: 10px; border-top-right-radius: 10px;")
  # Gray background for the title bar
        title_bar.setFixedHeight(50)  # Height of the title bar is 10 pixels

        app_space = QWidget(self)
        app_space.setStyleSheet("background-color: white; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")  # White background for the application space
        self.app_widget_class(app_space)

        # Add widgets to the grid
        layout.addWidget(title_bar, 0, 0, 1, -1)  # Span across the entire width
        layout.addWidget(app_space, 1, 0, 1, -1)  # Span across the entire width and remaining height

        # Setting up the title bar layout
        title_layout = QGridLayout()
        title_bar.setLayout(title_layout)

        # Title label
        title_label = QLabel(self.title)
        title_label.setStyleSheet("color: white; font: 20px 'Bernoru'")  # White text color
        title_layout.addWidget(title_label, 0, 0)  # Add to the left

        # Close button
        close_button = QPushButton('X')
        close_button.setStyleSheet("background-color: red; color: white; border-radius: 10px;")  # Red background, white text
        close_button.setFixedSize(30, 30)
        title_layout.addWidget(close_button, 0, 1)  # Add to the right
        title_layout.setColumnStretch(0, 1)  # Make the title stretch
        title_layout.setColumnStretch(1, 0)  # Close button does not stretch

        # Connect the close button to the close function
        close_button.clicked.connect(self.close)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.draggable = True
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.draggable and event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = False
            self.oldPos = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #mainWindow = Window(470, 740, "Calculator", Calculator)
    #mainWindow = Window(1130, 780, "Calendar", Calendar)
    #mainWindow = Window(650, 700, "Clock", Clock)
    #mainWindow = Window(735, 990, "Notepad", Notepad)
    #mainWindow = Window(735, 990, "Paint", Paint)
    #mainWindow = Window(1130, 780, "Image Viewer", ImageViewer)
    #mainWindow = Window(1130, 780, "Video Player", VideoPlayer)
    #mainWindow = Window(650, 700, "Audio Player", AudioPlayer)
    #mainWindow = Window(1130, 780, "Camera", Camera)
    #mainWindow = Window(1130, 780, "Terminal", Terminal)
    #mainWindow = Window(1130, 780, "Weather", Weather)
    mainWindow = Window(1130, 780, "Translator", Translate)
    #mainWindow = Window(1130, 780, "Dictionary", Dictionary)
    #mainWindow = Window(1130, 780, "News", News)
    #mainWindow = Window(1130, 780, "Browser", Browser)
    #mainWindow = Window(1130, 780, "Map", Map)
    mainWindow.show()
    sys.exit(app.exec_())