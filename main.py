import sys
from itertools import chain
from os import path

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox,
                             QGraphicsScene, QLabel, QLineEdit, QMainWindow,
                             QMenu, QMessageBox, QPushButton, QSizePolicy,
                             QVBoxLayout, QWidget)
from PyQt5.uic import loadUiType

from memory import Memory
# from segments import *

Ui_MainWindow, _ = loadUiType(path.join(path.dirname(__file__), "/home/rashad/Work/GitHub_Projects/OS-Memory-Allocation/MemoryV2.ui"))
Ui_Segments,_ = loadUiType(path.join(path.dirname(__file__), "/home/rashad/Work/GitHub_Projects/OS-Memory-Allocation/segments.ui"))


class MainApp(QMainWindow, Ui_MainWindow):

    process_Num = 0
    segments_list = []

    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.processes_list = []
        self.memory_created = 0  # use this variable as a flag
        self.process_name = ""
        self.scene = QGraphicsScene()
        self.red = QColor(qRgb(172, 50, 99))
        self.blue = QColor(qRgb(50, 150, 203))
        self.memory_width = 150
        self.memory_height = 600
        self.view.setScene(self.scene)
        self.setup_Ui()
        self.init_Buttons()

    def setup_Ui(self):
        """
        UI setup goes here
        """
        self.center_window()
        self.setWindowTitle("Memory Management")
        self.setFixedSize(530, 750)
        self.NumSegments.setMinimum(0)
        self.NumSegments.setMaximum(999)

    def center_window(self):
        # centering window
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def init_Buttons(self):
        """
        Buttons initializations and slots connections goes here
        """
        self.EnterSegments.clicked.connect(self.goToSegmentsWindow)
        self.SizeEnter.clicked.connect(self.createMemory)
        self.AddHole_button.clicked.connect(self.add_hole)
        self.deallocate_button.clicked.connect(self.deallocate_process)
        self.allocate_button.clicked.connect(self.allocate_memory)
        self.compact_button.clicked.connect(self.compact_memory)
        self.clear_button.clicked.connect(self.clear_memory)

    def DrawMemory(self):
        iterator = 0
        self.scene.clear()
        for element in self.memory.get_memoryContents():
            self.scene.addRect(
                0,  # x
                (iterator / self.memory.get_memorySize()) * self.memory_height,  # y
                self.memory_width,  # w
                (element[2] / self.memory.get_memorySize()) * self.memory_height,  # h
                self.red,
                hex_to_qcolor(self.memory.color_from_name(element[1])),
            )
            self.scene.addText(element[0]).setPos(
                0, (iterator / self.memory.get_memorySize()) * self.memory_height
            )
            self.scene.addText(str(iterator)).setPos(
                self.memory_width, (iterator / self.memory.get_memorySize()) * self.memory_height
            )
            iterator = iterator + element[2]

    def createMemory(self):

        try:
            memory_size = int(self.MemorySize.text())
            if memory_size > 0:
                self.memory = Memory(memory_size)
                self.memory_created = 1
                self.DrawMemory()
            else:
                self.show_msgBox(
                    "Memory Size error!\nSet Memory Size please!"
                )  # create error msg here
        except:
            self.show_msgBox(
                "Memory Size error!\nMemory Size Text Box accepts numeric values only."
            )  # create error msg to write only number here

    def add_hole(self):

        if self.memory_created:
            try:
                hole_address = int(self.HoleAddress.text())
                hole_size = int(self.HoleSize.text())
                if hole_size > 0:
                    self.memory.add_hole(hole_address, hole_size)
                    self.memory.Merge()
                    self.DrawMemory()
                else:
                    self.show_msgBox(
                        "Hole Size Value Error!\nHole cannot be of size 0"
                    )  # error msg here, plz add a proper hole size

            except ValueError:
                self.show_msgBox("Please Make sure you entered numeric values.")

            except AssertionError as error:
                if (
                    str(error)
                    == "Can't add a hole here! There's already a hole located in this address"
                ):
                    self.show_msgBox(str(error))
                else:
                    self.show_msgBox(
                        "Memory Limit Exceeded!\n" + str(error)
                    )  # error msg here, hole size or base address are beyond  memory size
        else:
            self.show_msgBox(
                "No Memory Found.\nPlease Create Memory before creating a hole!"
            )  # error msg here, plz create a memory by assigning its size above

    def allocate_memory(self):
        try:
            if self.memory_created:
                algorithm = self.algorithms_list.currentText()
                if len(self.process_name) > 0 and not (
                    self.memory.color_from_name(self.process_name)
                    in chain(*self.memory.get_memoryContents())
                ):
                    if algorithm == "First Fit":
                        self.memory.first_fit(self.segments_list, self.process_name)
                        self.DrawMemory()
                        self.NumSegments.setValue(0)
                    elif algorithm == "Best Fit":
                        self.memory.best_fit(self.segments_list, self.process_name)
                        self.DrawMemory()
                        self.NumSegments.setValue(0)
                    else:
                        self.memory.worst_fit(self.segments_list, self.process_name)
                        self.DrawMemory()
                        self.NumSegments.setValue(0)
                else:
                    self.show_msgBox(
                        "No Selected Process!\nAdd Segments First to be able to allocate a process"
                    )  # error msg here
            else:
                self.show_msgBox(
                    "No Memory Found.\nPlease Create Memory before allocate processes!"
                )  # error msg here, plz create a memory by assigning its size above
        except AssertionError as error:
            self.show_msgBox("Memory Limit Exceeded!\n" + str(error))

    def deallocate_process(self):

        process = self.processesBox.currentText()
        if self.memory_created:
            if len(process) > 0:
                self.memory.deallocate(process)
                process_index = self.processesBox.currentIndex()
                self.processesBox.removeItem(process_index)
                self.memory.Merge()
                self.DrawMemory()
            else:
                self.show_msgBox(
                    "No Process Found.\nPlease Add process first!"
                )  # msg error here, create memory first

        else:
            self.show_msgBox(
                "No Memory Found.\nPlease Create Memory first!"
            )  # msg error here, create memory first

    def goToSegmentsWindow(self):

        if self.memory_created:
            segmentsNo = self.NumSegments.value()
            if segmentsNo > 0:
                self.segments_window = SegmentWindow()
                self.segments_window.set_segmentsNo(segmentsNo)
                self.segments_window.show()
                self.segments_window.set_processesNum(self.process_Num + 1)

                self.segments_window.segmentsData_passingSig.connect(
                    self.receive_segmentsData
                )
            else:
                self.show_msgBox(
                    "Input Value Error\nNumber of segments must be more than 0"
                )  # error handling
        else:
            self.show_msgBox(
                "No Memory Found.\nPlease Create Memory first!"
            )  # error handling

    def receive_segmentsData(self, segList):
        print(segList)  # print for checking
        self.segments_list = segList
        self.process_Num += 1
        self.segments_window.close()
        self.processes_list.append("P" + str(self.process_Num))
        self.processesBox.addItem("P" + str(self.process_Num))
        self.process_name = "P" + str(self.process_Num)

    def compact_memory(self):
        if self.memory_created:
            self.memory.compact()
            self.memory.Merge()
            self.DrawMemory()
        else:
            self.show_msgBox("No Memory Found.\nPlease Create Memory first!")

    def clear_memory(self):
        if self.memory_created:
            del self.memory  # deleting memory object
            self.memory_created = 0  # set memory existence flag = 0
            self.clear_fields()
            # code to delete or remove memory contents in graphics should be added here
        else:
            self.show_msgBox("No Memory Found.\nPlease Create Memory first!")

    def clear_fields(self):
        self.MemorySize.setText("0")
        self.HoleAddress.setText("0")
        self.HoleSize.setText("0")
        self.NumSegments.setValue(0)
        processesNumber = int(self.processesBox.count())
        # print(processesNumber)
        if processesNumber > 0:
            for i in range(processesNumber):
                process = self.processesBox.currentText()
                if len(process) > 0:
                    process_index = self.processesBox.currentIndex()
                    self.processesBox.removeItem(process_index)
        self.process_Num = 0
        self.process_name = ""
        self.processes_list = []
        self.segments_list = []
        self.scene.clear()

    def show_msgBox(self, msg):
        self.msgBox = QMessageBox()
        self.msgBox.setWindowTitle("Error!")
        self.msgBox.setIcon(QMessageBox.Warning)
        self.msgBox.setText(msg)
        self.msgBox.setStandardButtons(QMessageBox.Ok)
        self.msgBox.exec_()


class SegmentWindow(QMainWindow, Ui_Segments):


    segmentsData_passingSig = pyqtSignal('QVariantList')

    def __init__(self, parent= None):
        super(SegmentWindow, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.columns_count = 2
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
        columnsLabels = ['Segment Name', 'Size']
        self.table.setHorizontalHeaderLabels(columnsLabels)
        self.table.setFixedSize(self.table_width, self.table_height)
        for i in range(self.columns_count):
            self.table.setColumnWidth(i, self.table_width/2)



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
                name = self.table.takeItem(i, 0).text()
                size =  int(self.table.takeItem(i, 1).text())
                segment = [name, size] # color is to be generated here
                self.segments_list.append(segment)
            except ValueError as e:
                self.show_msgBox("Input Value Error!\nSize must be numerical value.") # a code should be added to handle the case with no enough data.
            
            # code to handle sizes that exceed memory limit?
        
        if len(self.segments_list) > 0:
            self.segmentsData_passingSig.emit(self.segments_list)
            self.processes_Num += 1
        
        else:
            self.show_msgBox("Input Error!\nYou can't leave segment data table empty!") # a code should be added to handle the case with no enough data.
    

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


    def show_msgBox(self, msg):
        self.msgBox = QMessageBox()
        self.msgBox.setWindowTitle("Error!")
        self.msgBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.msgBox.setIcon(QMessageBox.Warning)
        self.msgBox.setText(msg)
        self.msgBox.setStandardButtons(QMessageBox.Ok)
        self.msgBox.exec_()

def hex_to_qcolor(value):
    value = value.lstrip("#")
    lv = len(value)
    R, G, B = tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))
    return QColor(R, G, B)


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
