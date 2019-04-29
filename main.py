from PyQt5.uic import loadUiType
import sys
from os import path
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QCheckBox, QLabel, QLineEdit, QComboBox
from PyQt5.QtGui import QIcon
from segments import *
from algorithms import *



FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "Memory.ui"))

class MainApp(QMainWindow, FORM_CLASS):

    process_Num = 0

    def __init__(self, parent= None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setup_Ui()
        self.init_Buttons()
    


    def setup_Ui(self):
        '''
        UI setup goes here
        '''
        self.center_window()
        self.setWindowTitle("Memory Management")
        self.NumSegments.setMinimum(0)
        self.NumSegments.setMaximum(999)

        
        

    def center_window(self):
        # centering window
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        


    def init_Buttons(self):
        '''
        Buttons initializations and slots connections goes here
        '''
        self.EnterSegments.clicked.connect(self.goToSegmentsWindow)



    def goToSegmentsWindow(self):
        segmentsNo = self.NumSegments.value()
        self.segments_window = SegmentWindow()
        self.segments_window.set_segmentsNo(segmentsNo)
        self.segments_window.show()
        self.segments_window.set_processesNum(self.process_Num + 1)

        self.segments_window.segmentsData_passingSig.connect(self.receive_segmentsData)
        
    
    def receive_segmentsData(self, segList):
        print(segList) # print as a proof of concept.
        self.process_Num += 1
        self.segments_window.close()
        


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


