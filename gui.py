from PyQt5 import QtGui, QtWidgets, uic
import sys, time
import serial_manager
import truffle
import re
from threading import Thread
import time


class Ui(QtWidgets.QDialog):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('MainWindow.ui', self)
        self.showMaximized()

        self.button_control_auto = self.findChild(QtWidgets.QPushButton, 'button_control_auto')
        self.button_control_auto.clicked.connect(self.auto)

        self.button_control_estop = self.findChild(QtWidgets.QPushButton, 'button_control_estop')
        self.button_control_estop.clicked.connect(self.estop)

        self.button_control_fire = self.findChild(QtWidgets.QPushButton, 'button_control_fire')
        self.button_control_fire.clicked.connect(self.fire)

        self.hardware_listview_ports = self.findChild(QtWidgets.QListView, 'hardware_listview_ports')
        # self.hardware_listview_ports.selectionModel().selectionChanged.connect(self.hardware_listview_ports())
        self.hardware_listview_portInfo = self.findChild(QtWidgets.QListView, 'hardware_listview_portInfo')
        self.listview_hardware_serial_monitor = self.findChild(QtWidgets.QListView, 'listview_hardware_serial_monitor')

        self.checkbox_hardware_autoscroll = self.findChild(QtWidgets.QCheckBox, 'checkbox_hardware_autoscroll')

        self.lcd_temperature = self.findChild(QtWidgets.QLCDNumber, 'lcd_temperature')

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
            payload = truffle.decode_data(text)
            if not (payload[0] == "" and payload[1] == "" and payload[2] == ""):
                print("%s >> %s: %s" % (payload[0], payload[1], payload[2]))
                serial_content = QtGui.QStandardItem("%s >> %s: %s" % (payload[0], payload[1], payload[2]))
                model_serial_monitor.appendRow(serial_content)

            self.lcd_temperature.display(80)

    def scroll_serial_monitor(self):
        while True:
            if self.checkbox_hardware_autoscroll.isChecked():
                self.listview_hardware_serial_monitor.scrollToBottom()
                time.sleep(1.5)

    def auto(self):
        print("auto function")
        serial_manager.srl.write('auto'.encode('utf-8'))

    def estop(self):
        print("estop function")
        serial_manager.srl.write('estop'.encode('utf-8'))

    def fire(self):
        print("fire function")
        serial_manager.srl.write('fire'.encode('utf-8'))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    serial_manager.get_serial('COM7')
    Ui.update_ports_list(window)
    Ui.start_serial_monitor(window)
    app.exec_()


main()
