from PyQt5 import QtGui, QtWidgets, uic
import sys, time
import serial_manager
import re
from threading import Thread
import time


def decode_data(raw_data):
    try:
        raw_payload = re.search("(?<=\#)(.*?)(?=\#)", raw_data.decode("utf-8"))
        payload = raw_payload[0].split(":")
        sender = payload[0]
        receiver = payload[1]
        data = payload[2].split("-")
        return [sender, receiver, data]
    except TypeError:
        return ["", "", ""]
    except Exception as e:
        print("Unable to decode payload data")
        print(e)
        return ["","",""]


class Ui(QtWidgets.QDialog):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('MainWindow.ui', self)
        self.showMaximized()

        self.button_control_auto = self.findChild(QtWidgets.QPushButton, 'button_control_auto')
        self.button_control_auto.clicked.connect(self.auto)

        self.button_control_estop = self.findChild(QtWidgets.QPushButton, 'button_control_estop')
        self.button_control_estop.clicked.connect(self.estop)

        self.hardware_listview_ports = self.findChild(QtWidgets.QListView, 'hardware_listview_ports')
        # self.hardware_listview_ports.selectionModel().selectionChanged.connect(self.hardware_listview_ports())
        self.hardware_listview_portInfo = self.findChild(QtWidgets.QListView, 'hardware_listview_portInfo')
        self.listview_hardware_serial_monitor = self.findChild(QtWidgets.QListView, 'listview_hardware_serial_monitor')

        self.checkbox_hardware_autoscroll = self.findChild(QtWidgets.QCheckBox, 'checkbox_hardware_autoscroll')

        self.show()

    def update_ports_list(self):
        model_portsList = QtGui.QStandardItemModel()
        self.hardware_listview_ports.setModel(model_portsList)

        # entries = ['one', 'two', 'three']
        ports_list = serial_manager.get_serial_ports()

        for i in ports_list:
            port_string = i[0] + " - " + i[1]
            item = QtGui.QStandardItem(port_string)
            model_portsList.appendRow(item)

    def view_port_info(self):
        model_portsInfo = QtGui.QStandardItemModel()
        self.hardware_listview_portInfo.setModel(model_portsInfo)

        # entries = ['one', 'two', 'three']
        port_info = serial_manager.get_serial_ports()

        for i in port_info:
            port_string = i[0] + " - " + i[1]
            item = QtGui.QStandardItem(port_string)
            model_portsInfo.appendRow(item)

    def start_serial_monitor(self):
        smt = Thread(target=self.update_serial_monitor)
        smt.start()
        smst = Thread(target=self.scroll_serial_monitor)
        smst.start()

    def update_serial_monitor(self):
        model_serial_monitor = QtGui.QStandardItemModel()
        self.listview_hardware_serial_monitor.setModel(model_serial_monitor)
        while True:
            text = serial_manager.srl.readline()
            payload = decode_data(text)
            if not (payload[0] == "" and payload[1] == "" and payload[2] == ""):
                print("%s >> %s: %s" % (payload[0], payload[1], payload[2]))
                serial_content = QtGui.QStandardItem("%s >> %s: %s" % (payload[0], payload[1], payload[2]))
                model_serial_monitor.appendRow(serial_content)

    def scroll_serial_monitor(self):
        while True:
            if self.checkbox_hardware_autoscroll.isChecked():
                self.listview_hardware_serial_monitor.scrollToBottom()
                time.sleep(1.5)

    def auto(self):
        print("auto function")

    def estop(self):
        print("estop function")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    serial_manager.get_serial('COM7')
    Ui.update_ports_list(window)
    Ui.start_serial_monitor(window)
    app.exec_()


main()
