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
        
        button =  QPushButton('Select Homework Directory', self)
        button2 = QPushButton('Select Homework Zip(s)', self)
        	
        button.setToolTip('Select Homework Directory')
        button.move(200,10)
        button.clicked.connect(self.zipdirectory_on_click)    
        button2.setToolTip('Select Homework Zip(s)')
        button2.move(200,60)
        button2.clicked.connect(self.zipdialog_on_click)
        
        self.show()


    #opens directory filled with students zipped assignments
    def openDirectory(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.ShowDirsOnly
        fileName= QFileDialog.getExistingDirectory(self,"Please Select a Directory", options=options)
        
        for subdir, dirs, files in os.walk(fileName):
            for file in files:
                if(file.find('.zip') != -1):

                    zipfileName = re.search('[^/]+$', file)
                    zipfileNameParse = os.path.splitext(os.path.basename(zipfileName.group(0)))[0]
                    
                    with ZipFile(zipfileName.group(0) , 'r') as zippedObject:
                        zippedObject.extractall(zipfileNameParse)
                    
			
    #opens zipped directory filled with students zipped assignments
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"Please Select a Zip File(s)", "",".zip (*.zip *.7z) ;; .dir (*.dir *.FOLDER", options=options)
        for file in files:

            zipfileName = re.search('[^/]+$', file)
            zipfileNameParse = os.path.splitext(os.path.basename(zipfileName.group(0)))[0]
            
            with ZipFile(zipfileName.group(0) , 'r') as zippedObject:
                zippedObject.extractall(zipfileNameParse)
                
    def center(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    @pyqtSlot()
    def zipdialog_on_click(self):
        self.openFileNamesDialog()

    @pyqtSlot()
    def zipdirectory_on_click(self):
        self.openDirectory()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
