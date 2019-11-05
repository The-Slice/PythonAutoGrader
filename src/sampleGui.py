import ctypes
import os
import re
import shutil
import sys
from zipfile import ZipFile

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class App(QMainWindow):

    def __init__(self, parent=None):
        user32 = ctypes.windll.user32
        screenWidth = user32.GetSystemMetrics(0)
        screenHeight = user32.GetSystemMetrics(1)
        super().__init__()
        self.title = 'Python Auto Grader'
        self.width = screenWidth / 2
        self.height = screenHeight / 2
        self.left = screenWidth / 2 - self.width / 2
        self.top = screenHeight / 2 - self.height / 2

        self.initUI()

    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.center()
    
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        openFile = QAction(QIcon('exit.png'), '&Open Zip(s)', self)        
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open Zip(s)')
        openFile.triggered.connect(self.zipdialog_on_click)

        openDir = QAction(QIcon('exit.png'), '&Open Directory', self)        
        openDir.setShortcut('Ctrl+D')
        openDir.setStatusTip('Open Directory')
        openDir.triggered.connect(self.zipdialog_on_click)


        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openDir)
        fileMenu.addAction(openFile)
        fileMenu.addAction(exitAct)

        self.show()


    #opens directory filled with students zipped assignments
    def openDirectory(self):
	
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName= QFileDialog.getExistingDirectory(self,"Please Select a Directory", options=options)
		
		#check if temp folder is created, if yes replace with new one
		#NOTE: crashes if file explorer is running in the background and is currently inside 'temp' directory
		#PermissionError exception fixes this issue
		
        try:
            os.mkdir("temp")
        except FileExistsError:
            try:
                shutil.rmtree("temp")
                os.mkdir("temp")
            except PermissionError:
                print("temp folder is in use")
                QMessageBox.about(self , "Attention" , "unzip failed") 
                return 
	
	    
	    #for each zip folder unzip the folder
        for subdir, dirs, files in os.walk(fileName):
            for file in files:
                if(file.find('.zip') != -1):

                    zipfileName = re.search('[^/]+$', file)
                    zipfileNameParse = os.path.splitext(os.path.basename(zipfileName.group(0)))[0]
                    
                    with ZipFile(zipfileName.group(0) , 'r') as zippedObject:
                        zippedObject.extractall(zipfileNameParse)
						
					#file is moved to temp once zip file is extracted into its own filename			
                    os.rename(zipfileNameParse, "temp\\" + zipfileNameParse) 
                    
			
    #opens zipped directory filled with students zipped assignments
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"Please Select a Zip File(s)", "","Zip Files (*.zip *.7zip)", options=options)
        
		#check if temp folder is created, if yes replace with new one
		#NOTE: crashes if file explorer is running in the background and is currently inside 'temp' directory
		#PermissionError exception fixes this issue
		
        try:
            os.mkdir("temp")
        except FileExistsError:
            try:
                shutil.rmtree("temp")
                os.mkdir("temp")
            except PermissionError:
                print("temp folder is in use")
                QMessageBox.about(self , "Attention" , "unzip failed") 
                return 
				
		#for each zip folder unzip the folder
        for file in files:

            zipfileName = re.search('[^/]+$', file)
            zipfileNameParse = os.path.splitext(os.path.basename(zipfileName.group(0)))[0]
            
            with ZipFile(zipfileName.group(0) , 'r') as zippedObject:
                zippedObject.extractall(zipfileNameParse)
			
			#file is moved to temp once zip file is extracted into its own filename			
            os.rename(zipfileNameParse, "temp\\" + zipfileNameParse)        
				
        
                
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
