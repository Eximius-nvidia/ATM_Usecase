
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem
from PyQt5.QtCore import Qt
from ATM_Dashboard_ui import Ui_DashboardWindow as Ui_MainWindow
import sys
import time

import paho.mqtt.client as mqttClient
import datetime
import threading
import json
import os
from settings import broker, port, user, password, sleep_interval, topic, qos, locations

client_id = "ATM_Tester"
ATM_centers = {}
index = 0

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Fix window size
        # self.setFixedSize(1341, 601)
        # Add headers
        self.add_table_header()
        self.start_broker()


    def table_add_rows(self, dataList):
        """
        doc
        :param dataList:
        :return:
        """
        green_color = (92, 247, 108,)
        red_color = (255, 129, 120,)
        if dataList[5] == 'PASS':
            color = green_color
        elif dataList[5] == 'FAIL':
            color = red_color
        else:
            color = (225, 230, 226,)

        rowPosition = self.ui.tableWidget.rowCount()
        # Create a row
        self.ui.tableWidget.insertRow(rowPosition)

        for column,data in enumerate(dataList):
            # create the item
            item = QTableWidgetItem("{}".format(data))
            # change the alignment
            item.setTextAlignment(Qt.AlignHCenter)
            # Add the item
            self.ui.tableWidget.setItem(rowPosition, column, QTableWidgetItem(item))
            self.ui.tableWidget.item(rowPosition, column).setBackground(QtGui.QColor(color[0],color[1],color[2]))

        self.ui.tableWidget.scrollToBottom()

        # fnt.setPointSize(40)
        # self.table.setFont(fnt)

    def add_table_header(self):
        """
        doc
        :return:
        """
        # Disable maximize
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

        # Setting Table font
        fnt = self.ui.tableWidget.font()
        fnt.setPointSize(10)
        fnt.setBold(True)
        self.ui.tableWidget.setFont(fnt)

        # Disable cell editing in GUI
        self.ui.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        # Column count
        self.ui.tableWidget.setColumnCount(7)

        # self.ui.tableWidget.setHorizontalHeaderLabels()

        columns = ["Location ID", "Name of the location", "Last update", "Present temperature", "AC status", "Test result", "Report"]
        for index, column in enumerate(columns):
            item1 = QtWidgets.QTableWidgetItem(column)
            item1.setBackground(QtGui.QColor(255, 0, 0))
            item1.setForeground(QtGui.QColor(0, 0, 0))

            self.ui.tableWidget.setHorizontalHeaderItem(index, item1)

        # Table will fit the screen horizontally
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.ui.tableWidget.cellClicked.connect(self.show_report)

    def show_report(self, row, column):
        if column == 6:
            location_id = self.ui.tableWidget.item(row, 0).text()
            # print(item, row, column)
            file_name = datetime.datetime.now().strftime("%Y-%m-%d") + "-" + str(location_id) + ".log"
            path = os.path.join(os.getcwd(),"reports",file_name)
            # print(path)
            if os.path.exists(path):
                os.system("start notepad "+ path)


    def start_broker(self):
        self.client = mqttClient.Client(client_id)  # create new instance
        # client.username_pw_set(user, password=password)  # set username and password
        self.client.on_connect = self.on_connect  # attach function to callback
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.connect(broker, port=port)  # connect to broker
        self.client.subscribe("ATM/location/measurements/#")
        self.client.subscribe("ATM/location/status/#")
        self.client.loop_start()  # start the loop

        while not self.client.is_connected():  # Wait for connection
            time.sleep(0.1)

    def on_connect(self, client, userdata, flags, rc):
        """
        doc
        :param client:
        :param userdata:
        :param flags:
        :param rc:
        :return:
        """
        status = {0: "Connection successful",
                  1: "Connection refused – incorrect protocol version",
                  2: "Connection refused – invalid client identifier",
                  3: "Connection refused – server unavailable",
                  4: "Connection refused – bad username or password",
                  5: "Connection refused – not authorised",
                  6 - 255: "Currently unused"
                  }
        # print("-" * 60)
        # text = "{:<27} : {}\n{:<27} : {}\n{:<27} : {}".format("Client connected to broker", self.client._host, "Client ID",
        #                                                       str(self.client._client_id, "UTF-8"), "Client status",
        #                                                       status[rc])
        # print(text)
        # print("-" * 60)
        #
        # header = "{:^15}|{:^20}|{:^20}|{:^4}|{:^6}".format("Location ID", "Time stamp", "Present temperature", "AC",
        #                                                    "Test Status")
        # print("-" * 80)
        # print(header)
        # print("-" * 80)

    def closeEvent(self, event):
        self.client.disconnect()
        self.client.loop_stop()

    def on_disconnect(self, client, userdata, rc):
        """
        On client disconnect
        :param client:
        :param userdata:
        :param rc:
        :return:
        """
        if self.client.is_connected() == False:
            print("Client disconnected------------------")

    def on_message(self, client, usrdata, msg):
        """
        doc
        :param client:
        :param usrdata:
        :param msg:
        :return:
        """
        if "ATM/location/measurements" in msg.topic:
            a = threading.Thread(target=self.process_messages, args=(msg.topic, json.loads(str(msg.payload, "UTF-8")),))
            a.start()
        elif "ATM/location/status" in msg.topic:
            location_id = int(msg.topic.split("/")[-1])
            payload_dictionary = json.loads(str(msg.payload, "UTF-8"))
            # ATM_centers[location_id] = str(msg.payload, "UTF-8")
            # print(f"{payload_dictionary}")

            if ATM_centers.get(location_id, None) == None:
                ATM_centers[location_id] = payload_dictionary
                ATM_centers[location_id].update({"rowId":self.ui.tableWidget.rowCount()})
                # Add this center to GUI table and get rowId
                self.table_add_rows([location_id,payload_dictionary["location"],"","","","","Click here"])

            elif ATM_centers.get(location_id, None) != None and payload_dictionary["status"] == 0:
                ATM_centers[location_id].update(payload_dictionary)
                # Update the GUI table row to empty for present temp column as ATM is inactive
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.table_update_rows([location_id, timestamp, "", "", ""],)

            elif ATM_centers.get(location_id, None) != None and payload_dictionary["status"] == 1:
                ATM_centers[location_id].update(payload_dictionary)

            # Update the Lcd panel
            self.update_lcd_panel()

    def update_lcd_panel(self):
        on = 0
        off = 0
        for value in ATM_centers.values():
            if value["status"] == 1:
                on +=1
            else:
                off +=1
        self.ui.lcdNumber_Online.display(on)
        self.ui.lcdNumber_Offline.display(off)
        self.ui.lcdNumber_Total.display(len(ATM_centers))
        # print(f"{ATM_centers}")

    def process_messages(self, topic, kwargs):
        """
        Method to validate AC status and report generation
        :param kwargs:
        :return:
        """
        location_id = int(topic.split("/")[-1])
        try:
            temp_low = ATM_centers[location_id]["temp_low"]
            temp_high = ATM_centers[location_id]["temp_high"]
            status = self.control_ac(temp_low, temp_high, kwargs['temp_present'],kwargs['ac_status'])
        except KeyError:
            status = "NA"
        except IndexError:
            status = "NA"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text = "{:^15}|{}|{:^20}|{:^6}|{:^6}\n".format(location_id, timestamp, kwargs['temp_present'],
                                                       kwargs['ac_status'], status)
        # print(text, end="")

        # GUI Table data update
        self.table_update_rows([location_id, timestamp, kwargs['temp_present'], kwargs['ac_status'], status])

        path = os.path.join(os.getcwd(), "reports",
                            "{}.log".format(datetime.datetime.now().strftime("%Y-%m-%d") + "-" + str(location_id)))
        with open(path, "a") as file:
            if file.tell() == 0:
                self.write_header(file,location_id)
            file.write("{}".format(text))



    def table_update_rows(self,dataList):
        """
        doc
        :param datalist:
        :return:
        """
        green_color = (92, 247, 108,)
        red_color = (255, 129, 120,)
        if dataList[4] == 'PASS':
            color = green_color
        elif dataList[4] == 'FAIL':
            color = red_color
        else:
            color = (225, 230, 226,)

        # Time stamp column
        # self.ui.tableWidget.setItem(ATM_centers[dataList[0]]["rowId"], 2, QTableWidgetItem("{}".format(dataList[1])))
        self.ui.tableWidget.item(ATM_centers[dataList[0]]["rowId"], 2).setText("{}".format(dataList[1]))
        # self.ui.tableWidget.item(ATM_centers[dataList[0]]["rowId"], 2).setBackground(QtGui.QColor(color[0],color[1],color[2]))

        # # AC present temp
        self.ui.tableWidget.item(ATM_centers[dataList[0]]["rowId"], 3).setText("{}".format(dataList[2]))
        # self.ui.tableWidget.item(ATM_centers[dataList[0]]["rowId"], 3).setBackground(
        #     QtGui.QColor(color[0], color[1], color[2]))

        # # AC on/off
        self.ui.tableWidget.item(ATM_centers[dataList[0]]["rowId"], 4).setText("{}".format(dataList[3]))
        # self.ui.tableWidget.item(ATM_centers[dataList[0]]["rowId"], 4).setBackground(
        #     QtGui.QColor(color[0], color[1], color[2]))

        # # test status
        self.ui.tableWidget.item(ATM_centers[dataList[0]]["rowId"], 5).setText("{}".format(dataList[4]))
        self.ui.tableWidget.item(ATM_centers[dataList[0]]["rowId"], 5).setBackground(
            QtGui.QColor(color[0], color[1], color[2]))

        self.ui.tableWidget.viewport().update()
        #-------------------------------------------------------------------
        # rowPosition = self.ui.tableWidget.rowCount()
        # # Create a row
        # self.ui.tableWidget.insertRow(rowPosition)

        # for column,data in enumerate(dataList):
        #     # create the item
        #     item = QTableWidgetItem("{}".format(data))
        #     # change the alignment
        #     item.setTextAlignment(Qt.AlignHCenter)
        #     # Add the item
        #     self.ui.tableWidget.setItem(rowPosition, column, QTableWidgetItem(item))
        #     self.ui.tableWidget.item(rowPosition, column).setBackground(QtGui.QColor(color[0],color[1],color[2]))
        #
        # self.ui.tableWidget.scrollToBottom()

        # fnt.setPointSize(40)
        # self.table.setFont(fnt)


    def control_ac(self, temp_low=0, temp_high=0, present_temp=0, ac_status='Off'):
        """
        Methos to Decides AC On/Off status
        :param temp_low:
        :param temp_high:
        :param present_temp:
        :return: On/Off Based on the validation rule
        """
        if temp_low < present_temp < temp_high:
            status = "PASS"
        else:
            status = "FAIL"
            
        if  present_temp < temp_low and ac_status == 'Off':
            status = "PASS"
        elif present_temp > temp_high and ac_status == 'On':
            status = "PASS"
        elif temp_low <= present_temp <= temp_high and ac_status == "On":
            status = "PASS"
        elif temp_low <= present_temp <= temp_high and ac_status == "Off":
            status = "PASS"
        else:
            status = "FAIL"
        
        return status

    def write_header(self, file,location_id):
        """
        Write header to test report file
        :return:
        """
        file.write("-" * 60)
        text = "\n{:<27} : {}\n{:<27} : {}\n{:<27} : {}\n{:<27} : {}\n".format("Client connected to broker", broker, "Client ID",
                                                                  client_id, "Location",ATM_centers[location_id]["location"],"Client status", "Connection successful")
        file.write(text)
        file.write("-" * 60)
        file.write("\n")

        header = "\n{:^15}|{:^20}|{:^20}|{:^4}|{:^6}\n".format("Location ID", "Time stamp", "Present temperature", "AC",
                                                               "Test Status")
        file.write("-" * 80)
        file.write(header)
        file.write("-" * 80)
        file.write("\n")


if __name__ == "__main__" :
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    sys.exit(app.exec())

