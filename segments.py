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
        self.columns_count = 3
        self.rows_count = 0 # to be changed
        self.table_width = 390
        self.table_height = 590
        self.setup_Ui()
        self.init_Buttons()





    def setup_Ui(self):
        self.setWindowTitle("Memory Management")

    

    def setup_table(self):
     
        self.table.setRowCount(self.rows_count)
        self.table.setColumnCount(self.columns_count)
        columnsLabels = ['Index', 'Segment Name', 'Size']
        self.table.setHorizontalHeaderLabels(columnsLabels)
        self.table.setFixedSize(self.table_width, self.table_height)
        for i in range(self.columns_count):
            self.table.setColumnWidth(i, self.table_width/3)





    def init_Buttons(self):
        
        pass


    def set_segmentsNo(self, segmentsNo):
        self.rows_count = segmentsNo
        self.setup_table()
