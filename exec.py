import  sys
from PyQt5 import QtGui, QtCore, QtWidgets
import thermostatUI # put testUI.py in the same dir as this code
import bme280sense as bme
# from threading import Thread
import time, datetime

class Worker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    date = QtCore.pyqtSignal(str)
    tme = QtCore.pyqtSignal(str)
    otemp = QtCore.pyqtSignal(str)
    ohumid = QtCore.pyqtSignal(str)
    itemp = QtCore.pyqtSignal(str)
    ihumid = QtCore.pyqtSignal(str)


    def updateValues(self):
        while True:
            outsidetemp = str(bme.OutTemp())
            outsidehumid = str(bme.OutHumid()) + (" % humidity")
            insidetemp = str(bme.InTemp())
            insidehumid = str(bme.InHumid()) + (" % humidity")
            now = datetime.datetime.now()
            datenow = now.strftime("%d/%m/%Y")
            timenow = now.strftime("%H:%M")

            self.otemp.emit(outsidetemp)
            self.ohumid.emit(outsidehumid)
            self.itemp.emit(insidetemp)
            self.ihumid.emit(insidehumid)
            self.date.emit(datenow)
            self.tme.emit(timenow)

            time.sleep(5)
        self.finished.emit()

class ThermostatWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ThermostatWindow, self).__init__()
        self.ui = thermostatUI.Ui_MainWindow() # in this and next line you say that you will use all widgets from testUI over self.ui
        self.ui.setupUi(self)
        #
        outsidetemp = str(bme.OutTemp())
        outsidehumid = str(bme.OutHumid()) + (" % humidity")
        insidetemp = str(bme.InTemp())
        insidehumid = str(bme.InHumid()) + (" % humidity")
        now = datetime.datetime.now()
        datenow = now.strftime("%d/%m/%Y")
        timenow = now.strftime("%H:%M")
        self.ui.LabOutTemp.setText(outsidetemp)
        self.ui.labOutHumid.setText(outsidehumid)
        self.ui.labIndoorTemp.setText(insidetemp)
        self.ui.labInHumid.setText(insidehumid)
        #
        self.ui.btnHome.clicked.connect(self.gotoHomePage)
        self.ui.btnFan.clicked.connect(self.gotoFanPage)
        self.ui.btnMode.clicked.connect(self.gotoModePage)
        self.ui.btnSettings.clicked.connect(self.gotoSettingsPage)
        self.ui.btnDoneFP.clicked.connect(self.gotoHomePage)
        self.ui.btnDoneMP.clicked.connect(self.gotoHomePage)
        self.ui.btnHelpFP.clicked.connect(self.actionHelpFan)
        self.ui.btnHelpMP.clicked.connect(self.actionHelpMode)
        self.ui.btnPlusTemp.clicked.connect(self.actionPlusTemp)
        self.ui.btnMinusTemp.clicked.connect(self.actionMinusTemp)
        self.ui.btnFanOn.clicked.connect(self.actionFanOn)
        self.ui.btnFanAuto.clicked.connect(self.actionFanAuto)
        self.ui.btnFanCirculate.clicked.connect(self.actionFanCirculate)
        self.ui.btnModeHeat.clicked.connect(self.actionModeHeat)
        self.ui.btnModeCool.clicked.connect(self.actionModeCool)
        self.ui.btnModeOff.clicked.connect(self.actionModeOff)
        self.ui.btnClose.clicked.connect(lambda:self.close())

        self.thread = QtCore.QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.updateValues)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.date.connect(lambda: self.ui.labDateSP.setText(datenow))
        self.worker.tme.connect(lambda: self.ui.labTimeHP.setText(timenow))
        self.worker.otemp.connect(lambda: self.ui.LabOutTemp.setText(outsidetemp))
        self.worker.ohumid.connect(lambda: self.ui.labOutHumid.setText(outsidehumid))
        self.worker.itemp.connect(lambda: self.ui.labIndoorTemp.setText(insidetemp))
        self.worker.ihumid.connect(lambda: self.ui.labInHumid.setText(insidehumid))
        self.thread.start()


    def gotoHomePage(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.btnHome.setEnabled(False)
        self.ui.btnFan.setEnabled(True)
        self.ui.btnMode.setEnabled(True)
        self.ui.btnSettings.setEnabled(True)

    def gotoFanPage(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.btnHome.setEnabled(True)
        self.ui.btnFan.setEnabled(False)
        self.ui.btnMode.setEnabled(True)
        self.ui.btnSettings.setEnabled(True)

    def gotoModePage(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.btnHome.setEnabled(True)
        self.ui.btnFan.setEnabled(True)
        self.ui.btnMode.setEnabled(False)
        self.ui.btnSettings.setEnabled(True)

    def gotoSettingsPage(self):
        self.ui.stackedWidget.setCurrentIndex(3)
        self.ui.btnHome.setEnabled(True)
        self.ui.btnFan.setEnabled(True)
        self.ui.btnMode.setEnabled(True)
        self.ui.btnSettings.setEnabled(False)

    def actionClose(self):
        print("Closing Application...")

    def actionHelpFan(self):
        print("Helping with fan...")

    def actionHelpMode(self):
        print("Helping with mode...")

    def actionPlusTemp(self):
        print("Increasing target temperature...")

    def actionMinusTemp(self):
        print("Decreasing target temperature...")

    def actionFanOn(self):
        print("Fan set to On")

    def actionFanAuto(self):
        print("Fan set to Auto")

    def actionFanCirculate(self):
        print("Fan set to Circulate")

    def actionModeHeat(self):
        print("Setting mode to Heat")

    def actionModeCool(self):
        print("Setting mode to Cool")

    def actionModeOff(self):
        print("Setting mode to Off")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ThermostatWindow()
    window.showFullScreen()
    sys.exit(app.exec())
