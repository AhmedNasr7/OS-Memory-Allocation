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


    segmentsData_passingSig = pyqtSignal('QVariantList')



    def __init__(self, parent= None):
        super(SegmentWindow, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.columns_count = 3
        self.rows_count = 0 
        self.table_width = 430
        self.table_height = 590
        self.segments_list = [] # the list represents the memory contents of segments.
        self.setup_Ui()
        self.init_Buttons()
        #self.process_Num += 1
        #self.processNo_label.setText('Process:   P' + str(self.process_Num))


        




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
        
        self.cancel_button.clicked.connect(self.cancel)
        self.clear_button.clicked.connect(self.clear)
        self.addSegments_button.clicked.connect(self.add_segments)


    @pyqtSlot()
    def set_segmentsNo(self, segmentsNo):
        self.rows_count = segmentsNo
        self.setup_table()


    def add_segments(self):
        for i in range(self.rows_count):
            try:
                name = self.table.takeItem(i, 1).text()
                size =  int(self.table.takeItem(i, 2).text())
                segment = [name, size] # color is to be generated here
                self.segments_list.append(segment)
            except Exception as e:
                pass
        
        # emit signal
        if len(self.segments_list) > 0:
            self.segmentsData_passingSig.emit(self.segments_list)
            self.processes_Num += 1
        
        else:
            pass # a code should be added to handle the case with no enough data.
    

    def set_processesNum(self, num):
        self.processes_Num = num
        self.processNo_label.setText('Process:   P' + str(num))


        

    def clear(self):
          for i in range (self.rows_count):
            self.table.setItem(i, 0, QTableWidgetItem(''))
            self.table.setItem(i, 1, QTableWidgetItem(''))
            self.table.setItem(i, 2, QTableWidgetItem(''))


    def cancel(self):
        self.close()