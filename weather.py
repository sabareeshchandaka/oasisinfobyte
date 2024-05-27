import sys
import requests
from PyQt5 import QtWidgets, QtGui, QtCore
from geopy.geocoders import Nominatim
from io import BytesIO
from PIL import Image

API_KEY = "ee83b991d135f816939d698683099b97"


class WeatherApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Weather App')
        self.setGeometry(100, 100, 600, 400)

        self.layout = QtWidgets.QVBoxLayout()

        self.locationInput = QtWidgets.QLineEdit(self)
        self.locationInput.setPlaceholderText("Enter location")
        self.layout.addWidget(self.locationInput)

        self.getWeatherButton = QtWidgets.QPushButton("Get Weather", self)
        self.getWeatherButton.clicked.connect(self.showWeather)
        self.layout.addWidget(self.getWeatherButton)

        self.weatherIcon = QtWidgets.QLabel(self)
        self.weatherIcon.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.weatherIcon)

        self.weatherDetails = QtWidgets.QLabel(self)
        self.weatherDetails.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.weatherDetails)

        self.setLayout(self.layout)

    def showWeather(self):
        location = self.locationInput.text()
        if not location:
            location = self.getLocation()
        if location:
            self.fetchWeather(location)
        else:
            self.weatherDetails.setText("Unable to detect location.")

    def getLocation(self):
        try:
            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.geocode("current location")
            return location.address
        except:
            return None

    def fetchWeather(self, location):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            self.displayWeather(data)
        else:
            self.weatherDetails.setText("Error fetching weather data.")

    def displayWeather(self, data):
        temp = data['main']['temp']
        weather = data['weather'][0]['description']
        wind_speed = data['wind']['speed']
        icon_url = f"https://openweathermap.org/img/wn/01n@2x.png"

        icon_response = requests.get(icon_url)
        icon_image = Image.open(BytesIO(icon_response.content))
        icon_qimage = QtGui.QImage(icon_image.tobytes(), icon_image.width, icon_image.height,
                                   QtGui.QImage.Format_ARGB32)
        pixmap = QtGui.QPixmap.fromImage(icon_qimage)

        self.weatherIcon.setPixmap(pixmap)
        self.weatherDetails.setText(f"Temperature: {temp}°C\nWeather: {weather}\nWind Speed: {wind_speed} m/s")


def main():
    app = QtWidgets.QApplication(sys.argv)
    weatherApp = WeatherApp()
    weatherApp.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()