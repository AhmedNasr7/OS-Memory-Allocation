import sys
from PyQt5 import QtWidgets, QtGui, QtCore

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

#######global variables#####################################
memorysize=None #total memory
numberofholes=None #number of empty places in memory
start_address=[] #start address of each hole
hole_size=[] #size of each hole
no_of_process=None #no of process to be allocated
number_segements=[]#number of segements for each process
name_segements=[]#name of each segement in each process
size_segements=[]#size of each segement in each process
####################################################################
class Window(QWidget):
    def __init__(self,parent=None):
        super(Window,self).__init__(parent)
        self.setWindowTitle("Memory Management")
        self.setGeometry(50,50,500,300)
        self.home()
       
        

    def home(self):
########UI of first page ########################################################
        self.grid=QGridLayout()
        self.setLayout(self.grid)
        
        self.memory=QLabel(self)
        self.memory.setText("Total Memory size")
        self.grid.addWidget(self.memory,0,0)

        self.memoryinput=QLineEdit(self)
        self.grid.addWidget(self.memoryinput,0,20)

        self.holes=QLabel(self)
        self.holes.setText("Number of holes")
        self.grid.addWidget(self.holes,5,0)

        self.inputholes=QLineEdit(self)
        self.grid.addWidget(self.inputholes,5,20)

        self.submit=QPushButton("OK",self)
        self.grid.addWidget(self.submit,10,0)

#################Action on clicking submit###########################
        self.submit.clicked.connect(self.getholes)
    def getholes(self):
        global memorysize
        global numberofholes
        memorysize=float(self.memoryinput.text())
        numberofholes=int(self.inputholes.text())
        self.close()
        self.window2=Window2()

   
##############second window for holes input##########################
class Window2(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Holes information")
        self.setGeometry(50,50,500,300)
        self.home()
        self.show()
    def home(self):
        global numberofholes
        self.grid=QGridLayout()
        self.setLayout(self.grid)
        global start_address
        global hole_size
        for n in range (numberofholes):
            self.start_add=QLabel(self)
            self.start_add.setText("Starting Address")
            
            self.inputstart=QLineEdit(self)
            
            self.size=QLabel(self)
            self.size.setText("Size")

            self.inputsize=QLineEdit(self)
            
            self.grid.addWidget(self.start_add,2*n+1,0)
            self.grid.addWidget(self.inputstart,2*n+1,1)
            self.grid.addWidget(self.size,2*n+1,2)
            self.grid.addWidget(self.inputsize,2*n+1,3)
            
            self.inputstart.textChanged.connect(lambda text,i=n:self.startaddress(text,i))
            self.inputsize.textChanged.connect(lambda text,i=n:self.holesize(text,i))
            start_address.append('')
            hole_size.append('')
######interaction with next and previous window##################
        self.back=QPushButton("Back",self)
        self.grid.addWidget(self.back,2*n+5,0)
        self.next=QPushButton("OK",self)
        self.grid.addWidget(self.next,2*n+5,1)

        self.back.clicked.connect(self.back_main)
        self.next.clicked.connect(self.next_window)
######getting information from segements textboxes#####################
    def startaddress(self,text,i):
        global start_address
        start_address[i]=text
    def holesize(self,text,i):
        global hole_size
        hole_size[i]=text

######functions of interaction with windows############################
    def back_main(self):
        self.hide()
        self.window=Window()
        self.window.show()
    def next_window(self):
       global start_address
       global hole_size
       start_address=[float(i) for i in start_address]
       hole_size=[float(i) for i in hole_size]
       self.hide()
       self.window=Window3()
       self.window.show()

##############third window for process#################################           
class Window3(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Process information")
        self.setGeometry(50,50,500,300)
        self.home()
        self.show()
    def home(self):
        self.grid=QGridLayout()
        self.setLayout(self.grid)
       
        self.no_of_process=QLabel(self)
        self.no_of_process.setText("Number of Processes")
        
        self.grid.addWidget(self.no_of_process,0,0)
        
        self.inputprocess=QLineEdit(self)
        
        self.grid.addWidget(self.inputprocess,0,1)
        self.inputprocess.textChanged.connect(lambda text:self.segement(text))
#####interaction with previous and next window#########
        self.next=QPushButton("Ok",self)
        self.back=QPushButton("Back",self)
        self.grid.addWidget(self.back,1,0)
        self.grid.addWidget(self.next,1,1)
        self.next.clicked.connect(self.open_window)
        self.back.clicked.connect(self.back_window)
########input for number of segements per process#############################
    def segement(self,text):
        global no_of_process
        global number_segements
        no_of_process=(text)
        no_of_process=int(no_of_process)
        self.grid.removeWidget(self.next)
        self.grid.removeWidget(self.back)
        self.next.deleteLater()
        self.back.deleteLater()
        self.next=None
        self.back=None
        
        for n in range(no_of_process):
            self.number_segment=QLabel(self)
            self.number_segment.setText("Number of segements of Process {}".format(n))
            self.input_segement=QLineEdit(self)

            self.grid.addWidget(self.number_segment,2*n+1,0)
            self.grid.addWidget(self.input_segement,2*n+1,1)
            number_segements.append('')

            self.input_segement.textChanged.connect(lambda text,i=n:self.generate_seg(text,i))
            
###########interaction with next and previous window########
        self.next=QPushButton("Ok",self)
        self.back=QPushButton("Back",self)
        self.grid.addWidget(self.back,2*n+2,0)
        self.grid.addWidget(self.next,2*n+2,1)
        self.next.clicked.connect(self.open_window)
        self.back.clicked.connect(self.back_window)
    def generate_seg(self,text,i):
        global number_segements
        number_segements[i]=text
    def open_window(self):
        global number_segements
        number_segements=[int (i) for i in number_segements]
        self.hide()
        self.window=Window4()
        self.window.show()
    def back_window(self):
        self.hide()
        self.window=Window2()
        self.window.show()
############4th window of segment information################
class Window4(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Process segment information")
        self.setGeometry(50,50,500,300)
        self.home()
        self.show()
    def home(self):
        self.grid=QGridLayout()
        self.setLayout(self.grid)
        
        global no_of_process
        global number_segements
        global name_segements
        global size_segements
        index=0
        index2=0
###########name_segements and size_segements initialization############################
        for n in range (no_of_process):
            name_segements.append([''])
            size_segements.append([''])
            for k in range(number_segements[n]-1):
                name_segements[n].append('')
                size_segements[n].append('')

                
        for n in range (no_of_process):
            for k in range(number_segements[n]):
                self.seg_name=QLabel(self)
                self.seg_name.setText("Name of Segement {} of Process {}" . format(k,n))

                self.seg_size=QLabel(self)
                self.seg_size.setText("Size of Segement {} of Process {}".format(k,n))

                self.seg_name_input=QLineEdit()
                self.seg_size_input=QLineEdit()

                self.grid.addWidget(self.seg_name,index+index2,0)
                self.grid.addWidget(self.seg_name_input,index+index2,1)
                self.grid.addWidget(self.seg_size,index+index2,2)
                self.grid.addWidget(self.seg_size_input,index+index2,3)
                index=index+1
                index2=index2+1
##########gettting data ###################################################3
                self.seg_name_input.textChanged.connect(lambda text, i=n,j=k:self.getname(text,i,j))
                self.seg_size_input.textChanged.connect(lambda text,i=n,j=k:self.getsize(text,i,j))

###########interaction with previous and next window###############
        self.next=QPushButton("OK",self)
        self.back=QPushButton("Back",self)
        self.grid.addWidget(self.back,index+index2+1,0)
        self.grid.addWidget(self.next,index+index2+1,1)
        self.next.clicked.connect(self.open_window)
        self.back.clicked.connect(self.back_window)
###########getting information from textboxes#####################
    def getname(self,text,i,j):
        global name_segements
        name_segements[i][j]=(text)
        #print(name_segements)
    def getsize(self,text,i,j):
        global size_segements
        size_segements[i][j]=(text)
        #print(size_segements)
###########functions for interaction##################################3
    def open_window(self):
        global name_segements
        global size_segements
        size_segements=[float(i) for i in size_segements]
        self.hide()
        self.window=Window5()
        self.window.show()
    def back_window(self):
        self.hide()
        self.window=Window3()
        self.window.show()
                
                
       
        





def main():
     app = QApplication(sys.argv)
     main = Window()
     main.show()
     sys.exit(app.exec_())


if __name__ == '__main__':
    main()
