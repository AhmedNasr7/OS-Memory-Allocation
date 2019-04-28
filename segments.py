from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import sys
from os import path
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton
from PyQt5.QtGui import QIcon


FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__), "segments.ui"))



class SegmentWindow(QMainWindow, FORM_CLASS):



    def __init__(self, parent= None):
        super(SegmentWindow, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setup_Ui()
        self.init_Buttons()





    def setup_Ui(self):
        self.setWindowTitle("Memory Management")
    





    def init_Buttons(self):
        pass

