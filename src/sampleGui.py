import sys
import re
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from zipfile import ZipFile


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Auto_Grader'
        self.left = 10
        self.top = 10
        self.width = 350
        self.height = 300
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.center()
        
        button1 = QPushButton('samplebutton uno', self)
        button2 = QPushButton('samplebutton dos', self)
        button3 = QPushButton('Select Homework Zip(s)', self)
        button4 = QPushButton('Select Homework Directory', self)
		
        button5 = QPushButton('Grade', self)
        
        button1.setToolTip('This is an example button')
        button1.move(100, 100)
        button1.clicked.connect(self.uno_on_click)
        
        button2.setToolTip('This is an example button')
        button2.move(100,70)
        button2.clicked.connect(self.dos_on_click)

        button3.setToolTip('Select Homework Zip(s)')
        button3.move(200,40)
        button3.clicked.connect(self.zipdialog_on_click)

        button4.setToolTip('Select Homework Directory')
        button4.move(200,10)
        button4.clicked.connect(self.dirdialog_on_click)

        button5.setToolTip('Grade')
        button5.move(200,10)
        button5.clicked.connect(self.grade_assignments)
        
        self.show()


    #opens directory filled with students zipped assignments
    def openDirectory(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName= QFileDialog.getExistingDirectory(self,"Please Select a Directory", options=options)
        if fileName:
            print(fileName)
			
    #opens zipped directory filled with students zipped assignments
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"Please Select a Zip File(s)", "",".zip (*.zip *.7z)", options=options)
        for file in files:
            zipfileName = re.search('[^/]+$', file)

            with ZipFile(zipfileName.group(0) , 'r') as zippedObject:
                zippedObject.extractall('temp')
            
            #for fileName in os.listdir('temp'):
                #print(fileName)
                #with ZipFile(fileName , 'r') as zippedObject:
                    #zippedObject.extractall('studentWork')
                
			
    def grade_assignments(self):
	    var = 0

    def center(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    @pyqtSlot()
    def zipdialog_on_click(self):
        self.openFileNamesDialog()

    @pyqtSlot()
    def dirdialog_on_click(self):
        self.openDirectory() 
        
    @pyqtSlot()
    def uno_on_click(self):
        print('button 1 click')

    @pyqtSlot()
    def dos_on_click(self):
        print('button 2 click')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
