"""
Created 2022
@author: BRDR
"""
import scipy.io
import sys
import os
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import QObject
import tkinter as tk
from tkinter import messagebox, filedialog
import time
import screeninfo
import cv2
from harvesters.core import Harvester
import numpy as np
from pynput import keyboard
import vision_service
import serial
import serial.tools.list_ports
import threading
import thorlabs_apt_device as tapt


class UiMainWindow(QObject):

    def __init__(self, mainwindowjai):
        super().__init__()
        # self.threadpool_JAI = QtCore.QThreadPool()
        self.harv = Harvester()
        self.mainwindow = mainwindowjai
        self.iaexist = False
        self.rsexist = False
        self.dir = os.path.abspath(os.getcwd())
        self.spectrum = 0
        self.default_prefix = 'IMG'
        self.snapshot_counter = 0
        self.default_RSVoltage = 0
        self.tempSnapShots = np.zeros([5, 3840, 5120])
        self.TPSnum = 0


    def setupUi(self, mainwindowjai):
        mainwindowjai.setObjectName("JAIRun2")
        mainwindowjai.resize(420, 80)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mainwindowjai.sizePolicy().hasHeightForWidth())
        mainwindowjai.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(mainwindowjai)
        self.centralwidget.setObjectName("centralwidget")
        self.connectButton = QtWidgets.QPushButton(self.centralwidget)
        self.connectButton.setGeometry(QtCore.QRect(15, 15, 185, 40))
        self.connectButton.setObjectName("connectButton")
        self.settingsButton = QtWidgets.QPushButton(self.centralwidget)
        self.settingsButton.setGeometry(QtCore.QRect(220, 15, 185, 40))
        self.settingsButton.setObjectName("settingsButton")
        self.slider_exposure = QtWidgets.QSlider(self.centralwidget)
        self.slider_exposure.setEnabled(False)
        self.slider_exposure.setGeometry(QtCore.QRect(15, 125, 240, 22))
        self.slider_exposure.setMinimum(10)
        self.slider_exposure.setMaximum(62250)
        self.slider_exposure.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider_exposure.setObjectName("slider_exposure")
        self.label_exposure = QtWidgets.QLabel(self.centralwidget)
        self.label_exposure.setEnabled(False)
        self.label_exposure.setGeometry(QtCore.QRect(15, 100, 141, 16))
        self.label_exposure.setObjectName("label_exposure")
        self.label_exposure_value = QtWidgets.QLabel(self.centralwidget)
        self.label_exposure_value.setEnabled(False)
        self.label_exposure_value.setGeometry(QtCore.QRect(265, 125, 47, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_exposure_value.sizePolicy().hasHeightForWidth())
        self.label_exposure_value.setSizePolicy(sizePolicy)
        self.label_exposure_value.setObjectName("label_exposure_value")
        self.checkbox_exposure_mode = QtWidgets.QCheckBox(self.centralwidget)
        self.checkbox_exposure_mode.setEnabled(False)
        self.checkbox_exposure_mode.setChecked(True)
        self.checkbox_exposure_mode.setGeometry(QtCore.QRect(310, 125, 100, 20))
        self.checkbox_exposure_mode.setObjectName("checkbox_exposure_mode")
        self.label_gain = QtWidgets.QLabel(self.centralwidget)
        self.label_gain.setEnabled(False)
        self.label_gain.setGeometry(QtCore.QRect(15, 160, 100, 16))
        self.label_gain.setObjectName("label_gain")
        self.checkbox_gain_mode = QtWidgets.QCheckBox(self.centralwidget)
        self.checkbox_gain_mode.setEnabled(False)
        self.checkbox_gain_mode.setGeometry(QtCore.QRect(310, 185, 80, 20))
        self.checkbox_gain_mode.setObjectName("checkbox_gain_mode")
        self.label_gain_value = QtWidgets.QLabel(self.centralwidget)
        self.label_gain_value.setEnabled(False)
        self.label_gain_value.setGeometry(QtCore.QRect(265, 185, 47, 20))
        self.label_gain_value.setObjectName("label_gain_value")
        self.slider_gain = QtWidgets.QSlider(self.centralwidget)
        self.slider_gain.setEnabled(False)
        self.slider_gain.setGeometry(QtCore.QRect(15, 185, 240, 22))
        self.slider_gain.setMinimum(100)
        self.slider_gain.setMaximum(1600)
        self.slider_gain.setSingleStep(1)
        self.slider_gain.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider_gain.setObjectName("slider_gain")
        self.line_edit_current_dir = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit_current_dir.setEnabled(False)
        self.line_edit_current_dir.setGeometry(QtCore.QRect(15, 260, 280, 23))
        self.line_edit_current_dir.setReadOnly(False)
        self.line_edit_current_dir.setObjectName("line_edit_current_dir")
        self.line_edit_current_dir.setText(os.path.abspath(os.getcwd()))
        self.directory_changeButton = QtWidgets.QPushButton(self.centralwidget)
        self.directory_changeButton.setEnabled(False)
        self.directory_changeButton.setGeometry(QtCore.QRect(300, 259, 105, 25))
        self.directory_changeButton.setObjectName("directory_changeButton")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 70, 420, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(0, 76, 420, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_prefix = QtWidgets.QLabel(self.centralwidget)
        self.label_prefix.setGeometry(QtCore.QRect(15, 225, 100, 16))
        self.label_prefix.setObjectName("label_prefix")
        self.line_edit_prefix = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit_prefix.setEnabled(False)
        self.line_edit_prefix.setGeometry(QtCore.QRect(120, 225, 285, 20))
        self.line_edit_prefix.setObjectName("line_edit_prefix")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(0, 290, 420, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_3.sizePolicy().hasHeightForWidth())
        self.line_3.setSizePolicy(sizePolicy)
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(0, 296, 420, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_4.sizePolicy().hasHeightForWidth())
        self.line_4.setSizePolicy(sizePolicy)
        self.line_4.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_4.setObjectName("line_4")
        self.connectRSButton = QtWidgets.QPushButton(self.centralwidget)
        self.connectRSButton.setGeometry(QtCore.QRect(30, 330, 101, 23))
        self.connectRSButton.setObjectName("connectRSButton")
        self.editRSVoltage = QtWidgets.QLineEdit(self.centralwidget)
        self.editRSVoltage.setEnabled(False)
        self.editRSVoltage.setGeometry(QtCore.QRect(30, 390, 130, 20))
        self.editRSVoltage.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.editRSVoltage.setObjectName("editRSVoltage")
        self.label_RSVoltage = QtWidgets.QLabel(self.centralwidget)
        self.label_RSVoltage.setEnabled(False)
        self.label_RSVoltage.setGeometry(QtCore.QRect(30, 370, 90, 20))
        self.label_RSVoltage.setObjectName("label_RSVoltage")
        self.checkBox_autoTPS = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_autoTPS.setEnabled(False)
        self.checkBox_autoTPS.setGeometry(QtCore.QRect(30, 430, 70, 17))
        self.checkBox_autoTPS.setObjectName("checkBox_autoTPS")
        self.lineEdit_V1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_V1.setEnabled(False)
        self.lineEdit_V1.setGeometry(QtCore.QRect(30, 480, 100, 20))
        self.lineEdit_V1.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lineEdit_V1.setObjectName("lineEdit_V1")
        self.pushButton_startTPS = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_startTPS.setEnabled(False)
        self.pushButton_startTPS.setGeometry(QtCore.QRect(20, 570, 381, 23))
        self.pushButton_startTPS.setObjectName("pushButton_startTPS")
        self.label_V1 = QtWidgets.QLabel(self.centralwidget)
        self.label_V1.setEnabled(False)
        self.label_V1.setGeometry(QtCore.QRect(30, 460, 70, 16))
        self.label_V1.setObjectName("label_V1")
        self.lineEdit_Vstep = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Vstep.setEnabled(False)
        self.lineEdit_Vstep.setGeometry(QtCore.QRect(30, 540, 100, 20))
        self.lineEdit_Vstep.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lineEdit_Vstep.setObjectName("lineEdit_Vstep")
        self.label_Vstep = QtWidgets.QLabel(self.centralwidget)
        self.label_Vstep.setEnabled(False)
        self.label_Vstep.setGeometry(QtCore.QRect(30, 520, 81, 16))
        self.label_Vstep.setObjectName("label_Vstep")
        self.movestageButton = QtWidgets.QPushButton(self.centralwidget)
        self.movestageButton.setDisabled(True)
        self.movestageButton.setGeometry(QtCore.QRect(230, 433, 131, 23))
        self.movestageButton.setObjectName("movestageButton")
        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setGeometry(QtCore.QRect(183, 303, 51, 261))
        self.line_6.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_6.setObjectName("line_6")
        self.line_7 = QtWidgets.QFrame(self.centralwidget)
        self.line_7.setGeometry(QtCore.QRect(180, 303, 71, 261))
        self.line_7.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_7.setObjectName("line_7")
        self.StageButton = QtWidgets.QPushButton(self.centralwidget)
        self.StageButton.setGeometry(QtCore.QRect(230, 330, 121, 24))
        self.StageButton.setObjectName("StageButton")
        self.label_position = QtWidgets.QLabel(self.centralwidget)
        self.label_position.setGeometry(QtCore.QRect(230, 370, 63, 20))
        self.label_position.setObjectName("label_position")
        self.lineEdit_position = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_position.setGeometry(QtCore.QRect(230, 390, 113, 19))
        self.lineEdit_position.setObjectName("lineEdit_position")
        # self.homestageButton = QtWidgets.QPushButton(self.centralwidget)
        # self.homestageButton.setGeometry(QtCore.QRect(230, 470, 91, 23))
        # self.homestageButton.setObjectName("homestageButton")
        # self.homestageButton.setDisabled(True)

        mainwindowjai.setCentralWidget(self.centralwidget)

        # CONNECT FUNCTIONS
        self.connectButton.clicked.connect(self.startCameraPreview)
        self.settingsButton.clicked.connect(self.modeSettings)
        self.checkbox_exposure_mode.clicked.connect(self.changeExposureMode)
        self.checkbox_gain_mode.clicked.connect(self.changeGainMode)
        self.slider_exposure.valueChanged.connect(self.changeExposureValue)
        self.slider_gain.valueChanged.connect(self.changeGainValue)
        self.directory_changeButton.clicked.connect(self.changeCurrentDirectory)
        self.line_edit_prefix.textChanged.connect(self.changePrefix)
        self.connectRSButton.clicked.connect(self.setRSCommunication)
        self.editRSVoltage.textChanged.connect(self.changeRSVoltage)
        self.pushButton_startTPS.clicked.connect(self.runAutoTPS)
        self.checkBox_autoTPS.clicked.connect(self.changeRSVoltageMode)
        self.movestageButton.clicked.connect(self.movestage)
        #nowe rzeczy moje
        self.StageButton.clicked.connect(self.setStageCommunication) #must maek setStageCommunication function
        # self.homestageButton.clicked.connect(self.homestage)




        self.retranslateUi(mainwindowjai)
        QtCore.QMetaObject.connectSlotsByName(mainwindowjai)

    def retranslateUi(self, mainwindowjai):
        _translate = QtCore.QCoreApplication.translate
        mainwindowjai.setWindowTitle(_translate("mainwindow", "JAIRun2"))
        self.connectButton.setText(_translate("mainwindow", "Connect with JAI camera"))
        self.settingsButton.setText(_translate("mainwindow", "Show settings"))
        self.label_exposure.setText(_translate("mainwindow", "Exposure Time [10 - 62250]"))
        self.label_exposure_value.setText(_translate("mainwindow", "Auto"))
        self.checkbox_exposure_mode.setText(_translate("mainwindow", "Auto Exposure"))
        self.label_gain.setText(_translate("mainwindow", "Gain [1 - 16]"))
        self.checkbox_gain_mode.setText(_translate("mainwindow", "Auto Gain"))
        self.label_gain_value.setText(_translate("mainwindow", "Auto"))
        self.directory_changeButton.setText(_translate("mainwindow", "Change directory"))
        self.label_prefix.setText(_translate("mainwindow", "Saved image prefix:"))
        self.line_edit_prefix.setText(_translate("mainwindow", "IMG"))
        self.connectRSButton.setText(_translate("mainwindow", "RS Connection"))
        self.editRSVoltage.setText(_translate("mainwindow", "0"))
        self.label_RSVoltage.setText(_translate("mainwindow", "Set RS Voltage"))
        self.checkBox_autoTPS.setText(_translate("mainwindow", "Auto TPS"))
        self.lineEdit_V1.setText(_translate("mainwindow", "0"))
        self.pushButton_startTPS.setText(_translate("mainwindow", "Start TPS"))
        self.label_V1.setText(_translate("mainwindow", "Voltage 1"))
        self.lineEdit_Vstep.setText(_translate("mainwindow", "0"))
        self.label_Vstep.setText(_translate("mainwindow", "Voltage Step"))
        self.movestageButton.setText(_translate("MainWindow", "Move Stage"))
        self.StageButton.setText(_translate("MainWindow", "Stage Connection"))
        self.label_position.setText(_translate("MainWindow", "Position"))
        # self.homestageButton.setText(_translate("MainWindow", "Home Stage"))







    def modeSettings(self):
        if self.mainwindow.height() == 80:
            self.showSettings()
        else:
            self.hideSettings()

    def showSettings(self):
        self.settingsButton.setText('Hide settings')
        self.mainwindow.resize(420, 600)
        self.label_exposure.setEnabled(True)
        self.label_gain.setEnabled(True)
        self.label_exposure_value.setEnabled(True)
        self.label_gain_value.setEnabled(True)
        self.checkbox_exposure_mode.setEnabled(True)
        self.checkbox_gain_mode.setEnabled(True)
        self.label_prefix.setEnabled(True)
        self.line_edit_prefix.setEnabled(True)
        if self.checkbox_gain_mode.isChecked():
            self.slider_gain.setDisabled(True)
            self.label_gain_value.setText('Auto')
        else:
            self.slider_gain.setEnabled(True)
            self.slider_gain.setValue(100)
            self.label_gain_value.setText(str(self.slider_gain.value()/100))
        self.directory_changeButton.setEnabled(True)

    def hideSettings(self):
        self.settingsButton.setText('Show settings')
        self.mainwindow.resize(420, 80)
        self.label_exposure.setDisabled(True)
        self.label_gain.setDisabled(True)
        self.label_exposure_value.setDisabled(True)
        self.label_gain_value.setDisabled(True)
        self.checkbox_exposure_mode.setDisabled(True)
        self.checkbox_gain_mode.setDisabled(True)
        self.directory_changeButton.setDisabled(True)
        self.label_prefix.setDisabled(True)
        self.line_edit_prefix.setDisabled(True)

    def startCameraPreview(self):
        if not self.harv.device_info_list:
            self.connectToCamera()

        self.create_image_acquirer()
        self.image_acquirer.start_image_acquisition()
        self.run_preview()

    def connectToCamera(self):
        # Create Harvester object to connect with the JAI camera
        self.harv = Harvester()  # create harvester object
        self.harv.add_file('C:/Program Files/JAI/SDK/bin/JaiUSB3vTL.cti')
        self.harv.update()

        tkinter_root = tk.Tk()  # create tkinter object for message box
        tkinter_root.withdraw()
        if not self.harv.device_info_list:  # Show Retry box if camera is not connected
            self.no_camera_info()

        time.sleep(1)
        self.harv.update()
        # harv.device_info_list[0]
        # width = 2560
        # height = 1920
        pass

    def no_camera_info(self):
        answer = tk.messagebox.askretrycancel('Retry or Cancel action Box', 'Choose the action')
        if answer:
            self.harv.update()

            if not self.harv.device_info_list:
                self.no_camera_info()
            return
        else:
            return

    def create_image_acquirer(self):
        # Create Image Acquirer object using Harvester object method - create_image_acquirer
        self.image_acquirer = self.harv.create_image_acquirer(0)  # create image acquirer
        self.image_acquirer.remote_device.node_map.AcquisitionFrameRate.value = 16
        self.image_acquirer.remote_device.node_map.PixelFormat.value = 'Mono8'
        self.image_acquirer.remote_device.node_map.ExposureAuto.value = 'Continuous'
        self.image_acquirer.remote_device.node_map.GainAuto = 'Off'
        self.image_acquirer.remote_device.node_map.Gain.value = 1
        # self.image_acquirer.remote_device.node_map.Width.value = 1280
        # self.image_acquirer.remote_device.node_map.Height.value = 960
        # self.image_acquirer.remote_device.node_map.OffsetX.value = 1920
        # self.image_acquirer.remote_device.node_map.OffsetY.value = 1440
        self.iaexist = True
        self.setSettingsParams()
        listener = keyboard.GlobalHotKeys({
         '<ctrl>+f': self.changeSpectrum,
         '<ctrl>+p': self.saveSnapShot
        })
        listener.start()

    def run_preview(self):
        screen = screeninfo.get_monitors()[0]
        # ts = time.time()
        # check = True

        # Run live camera preview until user will not interupt preview
        # Use buffer to store incoming video data
        while True:
            buffer = self.image_acquirer.fetch_buffer()

            # print(self.image_acquirer.statistics.fps)

            component = buffer.payload.components[0]  # Let's create an alias of the 2D image component:
            acc_frame = component.data.reshape(component.height, component.width)  # Reshape the NumPy array to 2D array
            # acc_frame = cv2.resize(acc_frame, [1920, 2560], interpolation=cv2.INTER_CUBIC)
            # acc_frame = cv2.resize(acc_frame, [int(3840/2), int(5120/2)], interpolation=cv2.INTER_CUBIC)
            # global view
            if self.spectrum:
                acc_frame2 = acc_frame[int((3840 - 960) / 2):int((3840 + 960) / 2),
                           int((5120 - 1280) / 2):int((5120 + 1280) / 2)]
                # acc_frame2 = acc_frame[1:960,int((5120 - 1280) / 2):int((5120 + 1280) / 2)]
                acc_frame2 = vision_service.get_spectrum(acc_frame2)
                acc_frame2 = cv2.cvtColor(acc_frame2, cv2.COLOR_GRAY2BGR)
            else:
                acc_frame2 = acc_frame
                cv2.line(acc_frame2, (2560, 1890), (2560, 1950), (255, 0, 0), 2)
                cv2.line(acc_frame2, (2530, 1920), (2590, 1920), (255, 0, 0), 2)
            self.frame = acc_frame

            window_name = 'frame'
            cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
            cv2.moveWindow(window_name, screen.x, screen.y)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow(window_name, acc_frame2)  # show live acquisition
            buffer.queue()
            if cv2.waitKey(1) & 0xFF == ord('q'):  # exit live aq with "q"-key
                self.image_acquirer.stop_acquisition()
                cv2.destroyWindow(window_name)
                self.image_acquirer.destroy()
                break

    def setSettingsParams(self):
        if self.image_acquirer.remote_device.node_map.ExposureAuto.value == 'Off':
            self.checkbox_exposure_mode.setChecked(False)
            self.slider_exposure.setEnabled(True)
            self.label_exposure_value.setText(str(self.image_acquirer.remote_device.node_map.ExposureTime.value))
            self.slider_exposure.setValue(int(self.image_acquirer.remote_device.node_map.ExposureTime.value))
        else:
            self.checkbox_exposure_mode.setChecked(True)
            self.slider_exposure.setDisabled(True)
            self.label_exposure_value.setText('Auto')

        if self.image_acquirer.remote_device.node_map.GainAuto.value == 'Off':
            self.checkbox_gain_mode.setChecked(False)
            self.slider_gain.setEnabled(True)
            self.label_gain_value.setText(str(self.image_acquirer.remote_device.node_map.Gain.value))
            self.slider_gain.setValue(int(self.image_acquirer.remote_device.node_map.Gain.value*100))
        else:
            self.checkbox_gain_mode.setChecked(True)
            self.slider_gain.setDisabled(True)
            self.label_gain_value.setText('Auto')

    def changeExposureMode(self):
        if self.iaexist:
            if self.checkbox_exposure_mode.isChecked():
                self.image_acquirer.remote_device.node_map.ExposureAuto.value = 'Continuous'
                self.slider_exposure.setDisabled(True)
                self.label_exposure_value.setText('Auto')
            else:
                self.image_acquirer.remote_device.node_map.ExposureAuto.value = 'Off'
                self.slider_exposure.setEnabled(True)
                self.changeExposureValue()
        else:
            if self.checkbox_exposure_mode.isChecked():
                self.slider_exposure.setDisabled(True)
                self.label_exposure_value.setText('Auto')
            else:
                self.slider_exposure.setEnabled(True)
                self.slider_exposure.setValue(62250)
                self.label_exposure_value.setText(str(self.slider_exposure.value()))

    def changeGainMode(self):
        if self.iaexist:
            if self.checkbox_gain_mode.isChecked():
                self.image_acquirer.remote_device.node_map.GainAuto.value = 'Continuous'
                self.slider_gain.setDisabled(True)
                self.label_gain_value.setText('Auto')
            else:
                self.image_acquirer.remote_device.node_map.GainAuto.value = 'Off'
                self.slider_gain.setEnabled(True)
                self.changeGainValue()
        else:
            if self.checkbox_gain_mode.isChecked():
                self.slider_gain.setDisabled(True)
                self.label_gain_value.setText('Auto')
            else:
                self.slider_gain.setEnabled(True)
                self.slider_gain.setValue(100)
                self.label_gain_value.setText(str(self.slider_gain.value()/100))

    def changeExposureValue(self):
        if self.iaexist:
            self.image_acquirer.remote_device.node_map.ExposureTime.value = self.slider_exposure.value()
            self.image_acquirer.remote_device.node_map.ExposureTimeRaw.value = self.slider_exposure.value()
            self.label_exposure_value.setText(str(self.slider_exposure.value()))
        else:
            self.label_exposure_value.setText(str(self.slider_exposure.value()))

    def changeGainValue(self):
        if self.iaexist:
            self.image_acquirer.remote_device.node_map.Gain.value = self.slider_gain.value()/100
            self.image_acquirer.remote_device.node_map.GainRaw.value = self.slider_gain.value()
            self.label_gain_value.setText(str(self.slider_gain.value()/100))
        else:
            self.label_gain_value.setText(str(self.slider_gain.value()/100))

    def changeCurrentDirectory(self):
        root = tk.Tk()
        root.withdraw()
        newDirectory = filedialog.askdirectory(initialdir=self.dir)
        if bool(newDirectory):
            self.line_edit_current_dir.setText(newDirectory)
            self.dir = newDirectory
        else:
            pass

    def changeSpectrum(self):
        self.spectrum = abs(self.spectrum-1)
        print(self.spectrum)

    def saveSnapShot(self):
        if self.set_prefix != None:
            imprefix = self.set_prefix
        else:
            imprefix = self.default_prefix
        imname = imprefix+'_'+str(self.snapshot_counter)+'.bmp'
        buffer = self.image_acquirer.fetch_buffer()

        # print(self.image_acquirer.statistics.fps)

        component = buffer.payload.components[0]  # Let's create an alias of the 2D image component:
        image = component.data.reshape(component.height, component.width)  # Reshape the NumPy array to 2D array

        cv2.imwrite(self.dir+'/'+imname, image)
        buffer.queue()
        self.snapshot_counter +=1


    def changePrefix(self):
        self.set_prefix = self.line_edit_prefix.text()
        self.snapshot_counter = 0

    def setRSCommunication(self):
        self.serlist = list(serial.tools.list_ports.comports())
        self.serialRS = serial.Serial()
        self.serialRS.baudrate = 115200
        self.serialRS.port = self.serlist[0].device
        self.serialRS.timeout = 0.2
        if self.serialRS.is_open:
            self.checkBox_autoTPS.setChecked(True)
            self.checkBox_autoTPS.setEnabled(True)
            self.label_V1.setEnabled(True)
            self.lineEdit_V1.setEnabled(True)
            self.label_Vstep.setEnabled(True)
            self.lineEdit_Vstep.setEnabled(True)
            self.pushButton_startTPS.setEnabled(True)
            self.rsexist = True
        # self.serialRS.write(self.default_RSVoltage)


    def setStageCommunication(self):
        self.serlist = list(serial.tools.list_ports.comports())
        self.stage = tapt.BBD201(serial_number="5")
        self.stage.identify()
        self.movestageButton.setEnabled(True)
        # self.homestageButton.setEnabled(True)



    def calculateStageMoves(self):
        przesuwy = 12
        max0 = 414660
        step = int(max0 / przesuwy)
        max = step * przesuwy
        stagemoves = list(range(step, max+step, step))
        return stagemoves



    def movestage(self):
        przesuwy = 12
        max0 = 414660
        step = int(max0/przesuwy)
        max = step * przesuwy
        stagerange = list(range(step, 4*step, step))
        print(stagerange)

        # y = 1
        # z = 1
        # pomocnyrange = range(1, 6)
        #
        # for n in stagerange:
        #     for x in pomocnyrange:
        #         y += 1  # robi zdjecia
        #         print('y', y)
        #     self.stage.move_absolute(n)
        #     z += 1
        #     print('z', z)
        #     while (self.stage.status['position'] != n):
        #         time.sleep(.2)

        # for n in stagerange:
        #     self.stage.move_absolute(n)
        #     while(self.stage.status['position'] != n):
        #         time.sleep(.2)
        #     #time.sleep(ile trwa robienie zdjecia)
        #     print(n) #robimy zdjecie



        # hologram = self.calculateHologramTPS()
        # if self.set_prefix != None:
        #    imprefix = self.set_prefix
        # else:
        #    imprefix = self.default_prefix
        # hologramname = imprefix+str(self.snapshot_counter)+'.mat'
        # self.snapshot_counter +=1
        # scipy.io.savemat(hologramname, {'u': hologram})



    def changeRSVoltage(self):
        self.RSVoltage = self.editRSVoltage.text()
        if self.rsexist:
            if self.RSVoltage != '':
                RSVoltage_off = float(self.RSVoltage)-0.4
                if RSVoltage_off >= 0.4:
                    self.RSVoltage = str(float(self.RSVoltage)-0.4)
                else:
                    self.RSVoltage = str(float(self.RSVoltage))
                self.serialRS.write(bytes('av'+self.RSVoltage+'\r', 'utf-8'))

    def doSnapShot(self, snapnum):
        buffer = self.image_acquirer.fetch_buffer()
        component = buffer.payload.components[0]  # Let's create an alias of the 2D image component:
        image = component.data.reshape(component.height, component.width)  # Reshape the NumPy array to 2D array
        self.tempSnapShots[snapnum] = image
        buffer.queue()

    def calculateHologramTPS(self):
        im = self.tempSnapShots
        phase = np.arctan2(2*(im[1]-im[3]), im[0]-2*im[2]+im[4])
        amplitude = np.sqrt(np.power(im[0]-im[2], 2)+np.power(im[3]-im[1], 2))
        hologram = np.single(amplitude)*np.exp(1j*np.single(phase))
        return hologram


    def runAutoTPS(self):
        self.line_edit_prefix.setDisabled(True)
        if (self.movestageButton.isEnabled()):
             TPSthread = threading.Thread(target=self.autocountTPSShot)  # if stage enabled create new thread for autoTPS
             TPSthread.start()
        else:
            TPSthread = threading.Thread(target=self.countTPSShot)
            TPSthread.start()


    def autocountTPSShot(self):
        stage_moves_list = self.calculateStageMoves() #lista pozycji
        for n in stage_moves_list:
            time.sleep(0.5)
            for foo in range(5):
                self.RSVoltage = float(self.lineEdit_V1.text()) + foo * float(self.lineEdit_Vstep.text())
                if self.rsexist:
                    if self.RSVoltage != '':
                        RSVoltage_off = self.RSVoltage - 0.4
                        if RSVoltage_off >= 0.4:
                            self.RSVoltage = str(self.RSVoltage - 0.4)
                        else:
                            self.RSVoltage = str(self.RSVoltage)
                        self.serialRS.write(bytes('av' + self.RSVoltage + '\r', 'utf-8'))
                time.sleep(1)
                self.doSnapShot(foo)

            self.stage.move_absolute(n)

            self.RSVoltage = str(0)
            self.serialRS.write(bytes('av' + self.RSVoltage + '\r', 'utf-8'))
            hologram = self.calculateHologramTPS()
            if self.set_prefix != None:
                imprefix = self.set_prefix
            else:
                imprefix = self.default_prefix
            hologramname = imprefix + str(self.snapshot_counter) + '.mat'
            self.snapshot_counter += 1
            scipy.io.savemat(self.dir + '/' + hologramname, {'u': hologram})
            self.line_edit_prefix.setEnabled(True)
            while (self.stage.status['position'] != n):
                 time.sleep(.2)



    def countTPSShot(self):
        time.sleep(0.5)
        for foo in range(5):
            self.RSVoltage = float(self.lineEdit_V1.text()) + foo*float(self.lineEdit_Vstep.text())
            if self.rsexist:
                if self.RSVoltage != '':
                    RSVoltage_off = self.RSVoltage - 0.4
                    if RSVoltage_off >= 0.4:
                        self.RSVoltage = str(self.RSVoltage - 0.4)
                    else:
                        self.RSVoltage = str(self.RSVoltage)
                    self.serialRS.write(bytes('av' + self.RSVoltage + '\r', 'utf-8'))
            time.sleep(1)
            self.doSnapShot(foo)


        self.RSVoltage = str(0)
        self.serialRS.write(bytes('av' + self.RSVoltage + '\r', 'utf-8'))
        hologram = self.calculateHologramTPS()
        if self.set_prefix != None:
           imprefix = self.set_prefix
        else:
           imprefix = self.default_prefix
        hologramname = imprefix+str(self.snapshot_counter)+'.mat'
        self.snapshot_counter +=1
        scipy.io.savemat(self.dir+'/'+hologramname, {'u': hologram})
        self.line_edit_prefix.setEnabled(True)


    def changeRSVoltageMode(self):
        if self.checkBox_autoTPS.isChecked():
            self.editRSVoltage.setDisabled(True)
            self.label_RSVoltage.setDisabled(True)
            self.label_V1.setEnabled(True)
            self.lineEdit_V1.setEnabled(True)
            self.label_Vstep.setEnabled(True)
            self.lineEdit_Vstep.setEnabled(True)
            self.pushButton_startTPS.setEnabled(True)
        else:
            self.editRSVoltage.setEnabled(True)
            self.label_RSVoltage.setEnabled(True)
            self.label_V1.setDisabled(True)
            self.lineEdit_V1.setDisabled(True)
            self.label_Vstep.setDisabled(True)
            self.lineEdit_Vstep.setDisabled(True)
            self.pushButton_startTPS.setDisabled(True)


    # def homestage(self):
    #     print('f')



""" RUN APPLICATION """
if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    mainwindow = QtWidgets.QMainWindow()
    ui = UiMainWindow(mainwindow)
    ui.setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec())