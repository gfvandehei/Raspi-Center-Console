import sys
from decimal import Decimal
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from controller.viewcontroller import ViewController
from threading import Thread
from queue import Queue

qtCreatorFile = "views/mirrorwindow.ui" # Enter file here.
Ui_MirrorWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MirrorWindow(QtWidgets.QMainWindow, Ui_MirrorWindow):
    def __init__(self, viewController: ViewController):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MirrorWindow.__init__(self)
        self.setupUi(self)

        self.left_queue = Queue()
        self.right_queue = Queue()
        self.running = True
        self.cam_thread_1 = Thread(
            target=self.startCameraFeed,
            args=(0, 1920/4, 1080/3, 30,))
        self.cam_thread_1.start()

        self.window_width = self.vidLeftMirror.frameSize().width()
        self.window_height = self.vidLeftMirror.frameSize().height()

        self.viewController = viewController
        self.left_image = ImageContainer(self.vidLeftMirror)
        self.right_image = ImageContainer(self.vidRightMirror)
        self.btnBack.clicked.connect(self.end)

        Thread(target=self.update_frame).start()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)

    def end(self):
        self.running = False
        self.viewController.show_back()

    def startCameraFeed(self, cam, width, height, fps):
        capture = cv2.VideoCapture(cam)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        capture.set(cv2.CAP_PROP_FPS, fps)

        while self.running:
            frame = {}
            retval, img = capture.read()
            frame['img'] = img

            if self.right_queue.qsize() < 10:
                self.right_queue.put(frame)
            else:
                print(self.right_queue.qsize())

    def calculate_tax(self):
        print("Mirrro")

    def update_frame(self):
        #while(True):
        if not self.right_queue.empty():
            frame = self.right_queue.get()
            img = frame['img']
            img_height, img_width, img_colors = img.shape
            scale_w = float(self.window_width) / float(img_width)
            scale_h = float(self.window_height) / float(img_height)
            scale = min([scale_w, scale_h])

            if scale == 0:
                scale = 1
            
            #img = cv2.resize(img, None, fx=scale, fy=scale, interpolation = cv2.INTER_CUBIC)
            img = cv2.resize(img, (self.window_width, self.window_height), interpolation = cv2.INTER_CUBIC)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width, bpc = img.shape
            bpl = bpc * width
            image = QtGui.QImage(img.data, width, height, bpl, QtGui.QImage.Format_RGB888)
            self.right_image.setImage(image)
            self.left_image.setImage(image)

class ImageContainer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ImageContainer, self).__init__(parent)
        self.image = None

    def setImage(self, image):
        self.image = image
        sz = image.size()
        self.setMinimumSize(sz)
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QtCore.QPoint(0, 0), self.image)
        qp.end()