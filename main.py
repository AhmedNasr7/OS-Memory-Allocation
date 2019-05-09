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
from memory import Memory


FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "MemoryV2.ui"))

class MainApp(QMainWindow, FORM_CLASS):

    process_Num = 0
    segments_list = []

    def __init__(self, parent= None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.processes_list = []
        self.memory_created = 0
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
        self.SizeEnter.clicked.connect(self.createMemory)
        self.deallocate_button.clicked.connect(self.deallocate_process)
        
    
    def createMemory(self):
        try:
            memory_size = int(self.MemorySize.text())
            if memory_size > 0:
                self.memory = Memory(memory_size)
                self.memory_created = 1
                
            else:
                pass # create error msg here
        except ValueError as e:
            print(e) # create error msg to write only number here



    def deallocate_process(self):
        process = self.processesBox.currentText()
        try:
            self.memory.deallocate(process)
            process_index = self.processesBox.currentIndex()
            self.processesBox.removeItem(process_index)

        except Exception as e:
            print(e) # create error msg, to choose memory size first

    def goToSegmentsWindow(self):
        
        segmentsNo = self.NumSegments.value()
        self.segments_window = SegmentWindow()
        self.segments_window.set_segmentsNo(segmentsNo)
        self.segments_window.show()
        self.segments_window.set_processesNum(self.process_Num + 1)

        self.segments_window.segmentsData_passingSig.connect(self.receive_segmentsData)
        
    
    def receive_segmentsData(self, segList):
        print(segList) # print for checking
        self.segments_list = segList
        self.process_Num += 1
        self.segments_window.close()
        self.processes_list.append('P' + str(self.process_Num))
        self.processesBox.addItem('P' + str(self.process_Num))
        
        

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


'''
self.scene = QGraphicsScene()
self.view.add(self.scene)
'''