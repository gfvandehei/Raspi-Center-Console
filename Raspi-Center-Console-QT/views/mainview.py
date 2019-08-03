import sys
from decimal import Decimal

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from controller.viewcontroller import ViewController
from views.mirrorview import MirrorWindow
qtCreatorFile = "views/mainwindow.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, viewController: ViewController):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.viewController = viewController
        self.btnMirror.clicked.connect(self.gotoMirror)
    
    def gotoMirror(self):
        self.viewController.show_view(MirrorWindow)