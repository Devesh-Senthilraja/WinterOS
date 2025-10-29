from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
import requests
from datetime import datetime

from .common import apply_style, create_button

class Weather(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QGridLayout(self)

        search = QWidget(self)
        layout.addWidget(search, 1, 0, 1, 2)
        searchLayout = QGridLayout(search)
        searchLayout.setColumnStretch(1, 1)

        locationLabel = QLabel("Location:", self)
        locationLabel.setStyleSheet("font: bold 15px 'Arial';")
        searchLayout.addWidget(locationLabel, 0, 0)

        self.cityValue = QLineEdit(self)
        apply_style(self.cityValue, font_size=15)
        self.cityValue.setFixedSize(900, 50)
        searchLayout.addWidget(self.cityValue, 0, 1)

        searchButton = create_button("Search", slot=self.getWeather, size=(100, 50), font_size=15, parent=self)
        searchLayout.addWidget(searchButton, 0, 2)

        weather = QWidget(self)
        apply_style(weather)
        weather.setFixedSize(465, 620)
        layout.addWidget(weather, 2, 0)

        weatherLayout = QGridLayout(weather)
        self.temperatureLabel = QLabel("", self)
        self.temperatureLabel.setStyleSheet("font: bold 75px; color: black; border: 1px solid #f0f0f0;")
        weatherLayout.addWidget(self.temperatureLabel, 0, 0)

        weatherInfo = QWidget(self)
        apply_style(weatherInfo)
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

    def _clear_weather(self):
        for label in (
            self.temperatureLabel,
            self.humidityLabel,
            self.pressureLabel,
            self.cloudsLabel,
            self.sunriseLabel,
            self.sunsetLabel,
        ):
            label.clear()

    def timeZone(self, utc_tz):
        local_time = datetime.utcfromtimestamp(utc_tz)
        return local_time.time()

    def getWeather(self):
        cityName = self.cityValue.text()
        weatherURL = 'http://api.openweathermap.org/data/2.5/weather?q=' + cityName + '&appid='
        try:
            weatherInfo = requests.get(weatherURL).json()

            if weatherInfo['cod'] == 200:
                kelvin_offset = 273.15

                temp = int(weatherInfo['main']['temp'] - kelvin_offset)
                pressure = weatherInfo['main']['pressure']
                humidity = weatherInfo['main']['humidity']
                sunrise = weatherInfo['sys']['sunrise']
                sunset = weatherInfo['sys']['sunset']
                timezone = weatherInfo['timezone']
                clouds = weatherInfo['clouds']['all']

                sunriseTime = self.timeZone(sunrise + timezone)
                sunsetTime = self.timeZone(sunset + timezone)

                self.temperatureLabel.setText(f"{temp}°C")
                self.humidityLabel.setText(f"Humidity: {humidity}%")
                self.pressureLabel.setText(f"Pressure: {pressure} hPa")
                self.cloudsLabel.setText(f"Clouds: {clouds}%")
                self.sunriseLabel.setText(f"Sunrise: {sunriseTime}")
                self.sunsetLabel.setText(f"Sunset: {sunsetTime}")

            else:
                self._clear_weather()
                QMessageBox.critical(self, cityName + " not found", "Please enter a valid city name.")
        except Exception:
            self._clear_weather()
            QMessageBox.critical(self, 'No Internet', "Unable to connect to the internet at the moment.")
