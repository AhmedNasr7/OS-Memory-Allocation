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
        self.memory_created = 0 # use this variable as a flag
        self.process_name = ''
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
        self.AddHole_button.clicked.connect(self.add_hole)
        self.deallocate_button.clicked.connect(self.deallocate_process)
        self.allocate_button.clicked.connect(self.allocate_memory)
        self.compact_button.clicked.connect(self.compact_memory)
        self.clear_button.clicked.connect(self.clear_memory)
    
    def createMemory(self):

        try:
            memory_size = int(self.MemorySize.text())
            if memory_size > 0:
                self.memory = Memory(memory_size)
                self.memory_created = 1
                
            else:
                self.show_msgBox('Memory Size error!\nSet Memory Size please!') # create error msg here
        except ValueError as e:
            self.show_msgBox('Memory Size error!\nMemory Size Text Box accepts numeric values only.') # create error msg to write only number here


    def add_hole(self):

        if(self.memory_created):
            try:
                hole_address = int(self.HoleAddress.text())
                hole_size = int(self.HoleSize.text())
                if hole_size > 0:
                    self.memory.add_hole(hole_address, hole_size)
                else:
                    self.show_msgBox('Hole Size Value Error!\nHole cannot be of size 0') # error msg here, plz add a proper hole size
            except ValueError as e:
                self.show_msgBox(self.wrong_input_text, 'Please Make sure you entered numeric values.') # error msg here, plz write numeric value in the address or/and the size of the hole.
            except AssertionError as error:
                if str(error) == "Can't add a hole here! There's already a hole located in this address":
                    self.show_msgBox(str(error))
                else:
                    self.show_msgBox('Memory Limit Exceeded!\n' + str(error)) #error msg here, hole size or base address are beyond  memory size
            except Exception as e:
                self.show_msgBox("Error!\nSorry, We're facing unexpected error") # erorr msg here, unxpected error
        else:
            self.show_msgBox('No Memory Found.\nPlease Create Memory before creating a hole!') # error msg here, plz create a memory by assigning its size above


    def allocate_memory(self):
        try:
            if(self.memory_created):
                algorithm = self.algorithms_list.currentText()
                if len(self.process_name) > 0:
                    if algorithm == 'First Fit':
                        self.memory.first_fit(self.segments_list, self.process_name)
                    elif algorithm == 'Best Fit':
                        self.memory.best_fit(self.segments_list, self.process_name)
                    else:
                        self.memory.worst_fit(self.segments_list, self.process_name)
                else:
                    self.show_msgBox('No Selected Process!\nAdd Segments First to be able to allocate a process') # error msg here
            else:
                self.show_msgBox('No Memory Found.\nPlease Create Memory before allocate processes!') # error msg here, plz create a memory by assigning its size above
        except Exception as e:
            pass # error code handling to be added
        except AssertionError as error:
            self.show_msgBox('Memory Limit Exceeded!\n' + str(error))



    def deallocate_process(self):

        process = self.processesBox.currentText()
        if(self.memory_created):
            if len(process) > 0:
                self.memory.deallocate(process)
                process_index = self.processesBox.currentIndex()
                self.processesBox.removeItem(process_index)
            else:
                self.show_msgBox('No Process Found.\nPlease Add process first!') # msg error here, create memory first

        else:
            self.show_msgBox('No Memory Found.\nPlease Create Memory first!') # msg error here, create memory first


    def goToSegmentsWindow(self):
        
        if (self.memory_created):
            segmentsNo = self.NumSegments.value()
            if(segmentsNo > 0):
                self.segments_window = SegmentWindow()
                self.segments_window.set_segmentsNo(segmentsNo)
                self.segments_window.show()
                self.segments_window.set_processesNum(self.process_Num + 1)

                self.segments_window.segmentsData_passingSig.connect(self.receive_segmentsData)
            else:
                self.show_msgBox("Input Value Error\nNumber of segments must be more than 0") # error handling
        else:
            self.show_msgBox("No Memory Found.\nPlease Create Memory first!") # error handling
        
    
    def receive_segmentsData(self, segList):
        print(segList) # print for checking
        self.segments_list = segList
        self.process_Num += 1
        self.segments_window.close()
        self.processes_list.append('P' + str(self.process_Num))
        self.processesBox.addItem('P' + str(self.process_Num))
        self.process_name = 'P' + str(self.process_Num)


    def compact_memory(self):
        if(self.memory_created):
            self.memory.compact()
        else:
            self.show_msgBox("No Memory Found.\nPlease Create Memory first!")


    def clear_memory(self):
        if(self.memory_created):
            del self.memory # deleting memory object
            self.memory_created = 0 # set memory existence flag = 0
            self.clear_fields()
            # code to delete or remove memory contents in graphics should be added here 
        else:
            self.show_msgBox("No Memory Found.\nPlease Create Memory first!")

    def clear_fields(self):
        self.MemorySize.setText('0')
        self.HoleAddress.setText('0')
        self.HoleSize.setText('0')
        self.NumSegments.setValue(0)
        processesNumber = int(self.processesBox.count())
        print(processesNumber)
        if processesNumber > 0:
            for i in range(processesNumber):
                process = self.processesBox.currentText()
                if len(process) > 0:
                    process_index = self.processesBox.currentIndex()
                    self.processesBox.removeItem(process_index)
        self.process_Num = 0
        self.process_name = ''
        self.processes_list = []
        self.segments_list = []



    def show_msgBox(self, msg):
        self.msgBox = QMessageBox()
        self.msgBox.setWindowTitle("Error!")
        self.msgBox.setIcon(QMessageBox.Warning)
        self.msgBox.setText(msg)
        self.msgBox.setStandardButtons(QMessageBox.Ok)
        self.msgBox.exec_()


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