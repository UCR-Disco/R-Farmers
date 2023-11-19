import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from lxml import etree
import requests
import html
from twilio.rest import Client

class WeatherApp(QWidget):
    def __init__(self):
        super(WeatherApp, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("R'Farmers App")
        self.setGeometry(300, 300, 400, 200)

        self.label_city = QLabel('Enter city:', self)
        self.edit_city = QLineEdit(self)
        self.label_result = QLabel('Weather Information will be displayed here.', self)

        get_weather = QPushButton('Get Weather', self)
        get_weather.clicked.connect(self.get_weather)
        # btn_get_weather.clicked.connect(self.collect_info)

        exit = QPushButton('Exit', self)
        exit.clicked.connect(self.show_message)

        layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.label_city)
        input_layout.addWidget(self.edit_city)
        input_layout.addWidget(get_weather)

        layout.addLayout(input_layout)
        layout.addWidget(self.label_result)
        layout.addWidget(exit)

        self.setLayout(layout)

    def get_weather(self):
        user_input = self.edit_city.text().lower()
        url = "https://www.wunderground.com/weather/us/ca/" + user_input
        headers = {
            "user-agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN) AppleWebKit/537.36 (KHTML, like Gecko) Version/5.0.1 Safari/537.36"
        }

        response = requests.get(url, headers=headers).text
        html = etree.HTML(response)

        date = html.xpath("/html/body/app-root/app-today/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[3]/div[1]/div/div[3]/div/lib-city-today-forecast/div/div[1]/div/a/div/div[2]/span[2]")[0]
        rain_probability = html.xpath("/html/body/app-root/app-today/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[3]/div[1]/div/div[3]/div/lib-city-today-forecast/div/div[1]/div/div/div/a[1]")[0]
        summary = html.xpath("/html/body/app-root/app-today/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[3]/div[1]/div/div[3]/div/lib-city-today-forecast/div/div[1]/div/div/div/a[2]")[0]

        date = date.text
        precipitation = rain_probability.text
        summary = summary.text

        index = precipitation.find('%')
        new_precipitation = int(precipitation[:index])

        result_text = f"Date: {date}, Precipitation: {new_precipitation}%, Summary: {summary}"
        self.label_result.setText(result_text)
        your_phone_number, done1 = QtWidgets.QInputDialog.getText(
        self, 'Input Dialog', 'Enter your number:')
        account_sid = 'AC093bb99ccaae6e0a9540661767554e70'
        auth_token = 'a78f71eb640ca3162f9142514681fc3b'
        twilio_phone_number = '18556206360'
        if done1:
            client = Client(account_sid, auth_token)
            if new_precipitation >= 70:
                message = client.messages.create(
                body=f"weather information for {user_input} is {new_precipitation}%" + " " + "chance of rain" + "\n\n no need to water your crops today",
                from_=twilio_phone_number,
                to=your_phone_number)
            else:
                message = client.messages.create(
                body=f"weather information for {user_input} is {new_precipitation}%" + " " + "chance of rain" + "\n\n water your crops today",
                from_=twilio_phone_number,
                to=your_phone_number)
                     
    def show_message(self):
        alert = QMessageBox()
        alert.setText('Message has been sent!')
        alert.exec()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
