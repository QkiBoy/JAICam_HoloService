# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 10:07:52 2019
@author: fc397
"""

# use this script to save a video using a JAI camera and the Harvester module

import tkinter as tk
from tkinter import messagebox
import time
import screeninfo
import cv2
from harvesters.core import Harvester
import vision_service
from pynput import keyboard
from PyQt6 import QtCore, QtWidgets, QtGui
from threading import Thread


class Ui_SettingsWindow(object):
    def __init__(self):
        super(Ui_SettingsWindow).__init__()

    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("Camera Settings")
        SettingsWindow.resize(329, 189)
        self.ConfirmButtonBox = QtWidgets.QDialogButtonBox(SettingsWindow)
        self.ConfirmButtonBox.setGeometry(QtCore.QRect(150, 150, 156, 23))
        self.ConfirmButtonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel | QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.ConfirmButtonBox.setObjectName("ConfirmButtonBox")
        self.ExposureSlider = QtWidgets.QSlider(SettingsWindow)
        self.ExposureSlider.setGeometry(QtCore.QRect(20, 30, 160, 20))
        self.ExposureSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.ExposureSlider.setObjectName("ExposureSlider")
        self.ExposureLabel = QtWidgets.QLabel(SettingsWindow)
        self.ExposureLabel.setGeometry(QtCore.QRect(20, 10, 50, 15))
        self.ExposureLabel.setObjectName("ExposureLabel")
        self.GainSlider = QtWidgets.QSlider(SettingsWindow)
        self.GainSlider.setGeometry(QtCore.QRect(20, 100, 160, 20))
        self.GainSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.GainSlider.setObjectName("GainSlider")
        self.GainLabel = QtWidgets.QLabel(SettingsWindow)
        self.GainLabel.setGeometry(QtCore.QRect(20, 80, 50, 15))
        self.GainLabel.setObjectName("GainLabel")
        self.AutoExposureBox = QtWidgets.QCheckBox(SettingsWindow)
        self.AutoExposureBox.setGeometry(QtCore.QRect(260, 30, 70, 20))
        self.AutoExposureBox.setObjectName("AutoExposureBox")
        self.AutoGainBox = QtWidgets.QCheckBox(SettingsWindow)
        self.AutoGainBox.setGeometry(QtCore.QRect(260, 100, 70, 20))
        self.AutoGainBox.setObjectName("AutoGainBox")
        self.ExposureValueLabel = QtWidgets.QLabel(SettingsWindow)
        self.ExposureValueLabel.setGeometry(QtCore.QRect(190, 30, 50, 20))
        self.ExposureValueLabel.setObjectName("ExposureValueLabel")
        self.GainValueLabel = QtWidgets.QLabel(SettingsWindow)
        self.GainValueLabel.setGeometry(QtCore.QRect(190, 100, 47, 20))
        self.GainValueLabel.setObjectName("GainValueLabel")

        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "SettingsWindow"))
        self.ExposureLabel.setText(_translate("SettingsWindow", "Exposure"))
        self.GainLabel.setText(_translate("SettingsWindow", "Gain"))
        self.AutoExposureBox.setText(_translate("SettingsWindow", "Auto"))
        self.AutoGainBox.setText(_translate("SettingsWindow", "Auto"))
        self.ExposureValueLabel.setText(_translate("SettingsWindow", "TextLabel"))
        self.GainValueLabel.setText(_translate("SettingsWindow", "TextLabel"))




def change_spectrum():
    global view
    if view == 'image':
        view = 'spectrum'
        image_acquirer.remote_device.node_map.AcquisitionFrameRate.value = 10
    else:
        view = 'image'
        image_acquirer.remote_device.node_map.AcquisitionFrameRate.value = 16
    # print('DUPA')


def save_current_frame():

    image_name = r'C:\Users\RK_Dokt\Documents\current1.bmp'
    image = frame
    cv2.imwrite(image_name, image)


def open_settings():
    thread = Thread(target=settings_thread)
    thread.start()
    thread.join()



def settings_thread():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SettingsWindow = QtWidgets.QDialog()
    ui = Ui_SettingsWindow()
    ui.setupUi(SettingsWindow)
    SettingsWindow.show()
    k = 0


def no_camera(harv):
    answer = tk.messagebox.askretrycancel('Retry or Cancel action Box', 'Choose the action')
    if answer:
        harv.update()

        if not h.device_info_list:
            no_camera(harv)
        return
    else:
        exit()


def create_JAI_environment():
    harv = Harvester()  # create harvester object
    harv.add_file('C:/Program Files/JAI/SDK/bin/JaiUSB3vTL.cti')
    harv.update()

    tkinter_root = tk.Tk()  # create tkinter object for message box
    tkinter_root.withdraw()

    if not harv.device_info_list:  # Show Retry box if camera is not connected
        no_camera(harv)

    time.sleep(1)
    harv.update()
    # harv.device_info_list[0]
    width = 2560
    height = 1920

    image_acquirer = harv.create_image_acquirer(0)  # create image acquirer
    # image_acquirer.remote_device.node_map.Width= width
    # image_acquirer.remote_device.node_map.Height.value = height
    # image_acquirer.remote_device.node_map.
    image_acquirer.remote_device.node_map.AcquisitionFrameRate.value = 10
    image_acquirer.remote_device.node_map.PixelFormat.value = 'Mono8'
    return image_acquirer, harv


# start image aq
def start_JAI_preview(image_acquirer, harv):
    image_acquirer.start_image_acquisition()

    screen = screeninfo.get_monitors()[0]
    ts = time.time()

    global frame
    while True:
        try:
            with image_acquirer.fetch_buffer() as buffer:

                print(image_acquirer.statistics.fps)

                component = buffer.payload.components[0]  # Let's create an alias of the 2D image component:
                acc_frame = component.data.reshape(component.height, component.width)  # Reshape the NumPy array to 2D array
                global view
                if view == 'spectrum':
                    frame = vision_service.get_spectrum(acc_frame, [1080, 1440])
                    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
                else:
                    frame = acc_frame

                window_name = 'frame'
                cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
                cv2.moveWindow(window_name, screen.x, screen.y)
                cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow(window_name, frame)  # show live acquisition

                if cv2.waitKey(1) & 0xFF == ord('q'):  # exit live aq with "q"-key
                    break

        except:
            te = time.time()
            print(te - ts)
            exit()

    # out.release()
    cv2.destroyAllWindows()
    image_acquirer.stop_image_acquisition()
    image_acquirer.destroy()
    harv.reset()


view = 'image'
frame = None
listener = keyboard.GlobalHotKeys({
    '<ctrl>+f': change_spectrum,
    '<ctrl>+p': save_current_frame,
    '<ctrl>+e': open_settings})
listener.start()

[image_acquirer, h] = create_JAI_environment()
start_JAI_preview(image_acquirer, h)
