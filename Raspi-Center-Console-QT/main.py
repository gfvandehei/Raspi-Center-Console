
import sys
from decimal import Decimal

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from views.mainview import MainWindow
from controller.viewcontroller import ViewController

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    controller = ViewController(MainWindow)
    sys.exit(app.exec_())