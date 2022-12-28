"""
Created 2022
@author: BRDR
"""
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSignal, QObject, QRunnable
import tkinter as tk
from tkinter import messagebox
import time
import screeninfo
import cv2
from harvesters.core import Harvester
import SettingsWindow
import numpy as np
import vision_service
from pynput import keyboard
from threading import Thread


class Camera_service(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Camera_service, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = Camera_signals()

    @QtCore.pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        finally:
            self.signals.closed.emit(True)


class Camera_signals(QObject):
    # Declaration of signals for camera service
    error = pyqtSignal()
    closed = pyqtSignal(bool)
    connected = pyqtSignal()


class Ui_MainWindow(QObject):

    def __init__(self):
        super().__init__()
        self.threadpool_JAI = QtCore.QThreadPool()
        self.harv = Harvester()
        self.MainWindow = MainWindow


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("JAI Previewer")
        MainWindow.resize(500, 100)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ConnectButton = QtWidgets.QPushButton(self.centralwidget)
        self.ConnectButton.setGeometry(QtCore.QRect(10, 20, 180, 50))
        self.ConnectButton.setObjectName("ConnectButton")
        self.SettingsButton = QtWidgets.QPushButton(self.centralwidget)
        self.SettingsButton.setGeometry(QtCore.QRect(220, 20, 180, 50))
        self.SettingsButton.setObjectName("SettingsButton")
        MainWindow.setCentralWidget(self.centralwidget)

        # Connections of buttons with functions
        self.ConnectButton.clicked.connect(self.start_camera_run)
        self.SettingsButton.clicked.connect(self.open_settings)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ConnectButton.setText(_translate("MainWindow", "Connect with JAI camera"))
        self.SettingsButton.setText(_translate("MainWindow", "Settings"))

    def start_camera_run(self):

        view = 'image'
        frame = None
        #listener = keyboard.GlobalHotKeys({
            #'<ctrl>+f': change_spectrum,
            #'<ctrl>+p': save_current_frame,
            #'<ctrl>+e': open_settings})
        #listener.start()
        if self.harv.device_info_list:
            self.create_JAI_environment()
        self.start_JAI_preview()
        #self.JAI_preview_thread = Camera_service(
        #    lambda *args: self.start_JAI_preview())
        #self.threadpool_JAI.start(self.JAI_preview_thread)
        #self.JAI_preview_thread.signals.closed.connect(self.close_JAI(image_acquirer, h))



    def create_JAI_environment(self):
        self.harv = Harvester()  # create harvester object
        self.harv.add_file('C:/Program Files/JAI/SDK/bin/JaiUSB3vTL.cti')
        self.harv.update()

        tkinter_root = tk.Tk()  # create tkinter object for message box
        tkinter_root.withdraw()

        if not self.harv.device_info_list:  # Show Retry box if camera is not connected
            no_camera(self.harv)

        time.sleep(1)
        self.harv.update()
        # harv.device_info_list[0]
        width = 2560
        height = 1920


        pass


# start image aq
    def start_JAI_preview(self):
        self.image_acquirer = self.harv.create_image_acquirer(0)  # create image acquirer
        # image_acquirer.remote_device.node_map.Width= width
        # image_acquirer.remote_device.node_map.Height.value = height
        # image_acquirer.remote_device.node_map.
        self.image_acquirer.remote_device.node_map.AcquisitionFrameRate.value = 10
        self.image_acquirer.remote_device.node_map.PixelFormat.value = 'Mono8'

        self.image_acquirer.start_image_acquisition()
        self.image_acquirer.buffer_handling_mode = 'overwrite'
        screen = screeninfo.get_monitors()[0]
        ts = time.time()
        check = True

        while True:

            buffer = self.image_acquirer.fetch_buffer()

            print(self.image_acquirer.statistics.fps)

            component = buffer.payload.components[0]  # Let's create an alias of the 2D image component:
            acc_frame = component.data.reshape(component.height, component.width)  # Reshape the NumPy array to 2D array
            #acc_frame = np.resize(acc_frame, [int(acc_frame.shape[0]/4), int(acc_frame.shape[1]/4)] )
            #global view
            #if view == 'spectrum':
            #    frame = vision_service.get_spectrum(acc_frame, [1080, 1440])
            #    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            #else:
            #    frame = acc_frame
            overburned_index = np.where(acc_frame >= 255)
            frame_gray = acc_frame
            window_name = 'frame'
            cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
            cv2.moveWindow(window_name, screen.x, screen.y)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            #frame_color = cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2BGR)
            #frame_color[overburned_index[0],overburned_index[1],0] = 0
            #frame_color[overburned_index[0], overburned_index[1], 1] = 0
            #frame_color[overburned_index[0], overburned_index[1], 2] = 255
            cv2.imshow(window_name, frame_gray)  # show live acquisition
            buffer.queue()
            if cv2.waitKey(1) & 0xFF == ord('q'):  # exit live aq with "q"-key
                self.image_acquirer.stop_acquisition()
                cv2.destroyWindow(window_name)
                self.image_acquirer.destroy()
                break

                k = 0

    def open_settings(self):
        self.SettingsWindow = QtWidgets.QWidget()
        self.uiset = SettingsWindow.Ui_Settings()
        self.uiset.setupUi(self.SettingsWindow)
        self.uiset.exposure_auto_changed.connect(self.update_exposure_mode)
        self.uiset.exposure_value_changed.connect(self.update_exposure_value)


        if not self.harv.device_info_list:

            self.uiset.GainSlider.setDisabled(True)
            self.uiset.AutoGainBox.setDisabled(True)
            self.uiset.AutoExposureBox.setDisabled(True)
            self.uiset.ExposureSlider.setDisabled(True)
            self.uiset.ExposureValueLabel.setText('None')
            self.uiset.GainValueLabel.setText('None')
        else:
            if 'self.image_acquirer' !=None:
                self.uiset.AutoExposureBox.setChecked(self.image_acquirer.remote_device.node_map.ExposureAuto.value != 'Off')
                self.uiset.AutoGainBox.setChecked(self.image_acquirer.remote_device.node_map.GainAuto.value != 'Off')
                self.uiset.ExposureSlider.setValue(self.image_acquirer.remote_device.node_map.ExposureTime.value)
                self.uiset.GainSlider.setValue(self.image_acquirer.remote_device.node_map.Gain.value)
                self.uiset.ExposureValueLabel.setText(str(self.image_acquirer.remote_device.node_map.ExposureTime.value))
                self.uiset.GainValueLabel.setText(str(self.image_acquirer.remote_device.node_map.Gain.value))

        self.SettingsWindow.show()
        pass

    @QtCore.pyqtSlot(bool)
    def update_exposure_mode(self, checked):
        if checked == True:
            self.image_acquirer.remote_device.node_map.ExposureAuto.value = 'Continuous'
        else:
            self.image_acquirer.remote_device.node_map.ExposureAuto.value = 'Off'

    @QtCore.pyqtSlot(int)
    def update_exposure_value(self, value):
        self.image_acquirer.remote_device.node_map.ExposureTime.value = value



def no_camera(harv):
    answer = tk.messagebox.askretrycancel('Retry or Cancel action Box', 'Choose the action')
    if answer:
        harv.update()

        if not harv.device_info_list:
            no_camera(harv)
        return
    else:
        exit()






if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())