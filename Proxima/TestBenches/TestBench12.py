import sys
import os
import folium
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class Map(QWidget):
    def __init__(self):
        super().__init__()

        self.initWidgets()

    def initWidgets(self):
        # Create the main grid layout
        main_layout = QGridLayout(self)

        # Create search bar components
        location_label = QLabel("Location:", self)
        location_label.setStyleSheet("font-family: Comic Sans MS; font-size: 14px;")

        self.address_input = QLineEdit(self)
        self.address_input.setStyleSheet("font-family: Comic Sans MS; font-size: 12px;")
        self.address_input.setFixedHeight(40)

        search_button = QPushButton("Search", self)
        search_button.setStyleSheet("""
            font-family: Comic Sans MS; font-size: 14px;
            background-color: #F7F6F5; color: #373433;
            height: 40px; width: 60px;
            hover { background-color: #E2E2E2; }
        """)
        search_button.clicked.connect(self.update_map)

        # Add search bar components to the main layout
        main_layout.addWidget(location_label, 0, 0, 1, 1)
        main_layout.addWidget(self.address_input, 0, 1, 1, 8)
        main_layout.addWidget(search_button, 0, 9, 1, 1)

        # Create map frame and add it to the main layout
        self.map_view = QWebEngineView(self)
        main_layout.addWidget(self.map_view, 1, 0, 1, 10)
        
        # Update the map with the initial location
        self.update_map(initial=True)

        self.setLayout(main_layout)
        self.setWindowTitle('Map Viewer')
        self.resize(960, 600)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Map()
    window.show()
    sys.exit(app.exec_())
