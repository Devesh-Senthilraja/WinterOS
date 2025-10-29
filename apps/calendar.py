import calendar

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import QDate, Qt

from .common import create_button, widget_style

class Calendar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        today = QDate.currentDate()
        self.month = today.month()
        self.year = today.year()
        self.today = today
        self.initUI()

    def initUI(self):
        main_layout = QGridLayout(self)
        nav_layout = QGridLayout()
        self.prev_month_btn = create_button("<", slot=lambda: self.switchMonths(-1), size=(70, 50))
        self.next_month_btn = create_button(">", slot=lambda: self.switchMonths(1), size=(70, 50))
        self.month_year_label = QLabel()
        self.month_year_label.setAlignment(Qt.AlignCenter)
        self.month_year_label.setStyleSheet(widget_style(font_size=40, background="#ffffff", border=False))
        self.month_year_label.setMinimumHeight(50)

        nav_layout.addWidget(self.prev_month_btn, 0, 0)
        nav_layout.addWidget(self.month_year_label, 0, 1)
        nav_layout.addWidget(self.next_month_btn, 0, 2)
        nav_layout.setColumnStretch(0, 1)
        nav_layout.setColumnStretch(1, 8)
        nav_layout.setColumnStretch(2, 1)

        calendar_layout = QGridLayout()
        self.days_of_week = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        day_label_style = widget_style(background="#ffffff")
        self._default_day_style = f"{widget_style()} padding: 10px;"
        self._today_day_style = f"{widget_style(background='#787878')} padding: 10px;"

        for i, day in enumerate(self.days_of_week):
            label = QLabel(day)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(day_label_style)
            label.setMinimumHeight(50)
            calendar_layout.addWidget(label, 0, i, 1, 1)
            calendar_layout.setColumnStretch(i, 0)
            calendar_layout.setColumnMinimumWidth(i, 150)

        self.day_labels = []
        for row in range(1, 7):
            week = []
            for col in range(7):
                label = QLabel("")
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet(self._default_day_style)
                label.setMinimumHeight(90)
                week.append(label)
                calendar_layout.addWidget(label, row, col, 1, 1)
                calendar_layout.setColumnStretch(col, 0)
            self.day_labels.append(week)

        self.printMonthYear(self.month, self.year)
        self.monthGenerator()

        main_layout.addLayout(nav_layout, 0, 0)
        main_layout.addLayout(calendar_layout, 1, 0)

        self.setLayout(main_layout)

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
        self.monthGenerator()

    def monthGenerator(self):
        for week in self.day_labels:
            for label in week:
                label.setText("")
                label.setStyleSheet(self._default_day_style)

        first_weekday, number_of_days = calendar.monthrange(self.year, self.month)
        # calendar.monthrange uses Monday=0. our grid starts on Saturday
        start_index = (first_weekday - 5) % 7

        for day in range(1, number_of_days + 1):
            index = start_index + day - 1
            row, col = divmod(index, 7)
            label = self.day_labels[row][col]
            label.setText(str(day))
            if QDate(self.year, self.month, day) == self.today:
                label.setStyleSheet(self._today_day_style)
