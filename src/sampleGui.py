import ctypes
import os
import re
import shutil
import sys
from zipfile import ZipFile
from shutil import copy2
import glob

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from tester import Tester
BORDERSIZE = 10

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

        resultArea = QPlainTextEdit(self)
        
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
        openDir.triggered.connect(self.zipdirectory_on_click)


        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openDir)
        fileMenu.addAction(openFile)
        fileMenu.addAction(exitAct)

        labelA = QLabel('Assignment Key:', self)
        labelA.move(332, 175)
        labelA.resize(160,40)

        dragdrop = CustomLabel('Drop key here', self)
        dragdrop.move(495, 175)
        dragdrop.resize(500,40)

        # text result area
        resultArea.resize(self.width*0.75, self.height*0.75)

        # attempt to use pyqt auto element resizing
        resultArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        resultArea.insertPlainText("Hello World.\n")
        resultArea.move(self.width/4-BORDERSIZE, self.height-resultArea.height()-BORDERSIZE)

        resultArea.setReadOnly(True)
        self.show()


    #opens directory filled with students zipped assignments
    def openDirectory(self):
        
        options =  QFileDialog.Options()
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

    def runTests(self):
        t = Tester("../target/key")
        for assignment_instance in os.listdir("temp\\"):
            t.analyze_dynamically(assignment_instance)
        #TODO: pipe outpute content accessed as string via t.captured_output

    @pyqtSlot()
    def zipdialog_on_click(self):
        self.openFileNamesDialog()

    @pyqtSlot()
    def zipdirectory_on_click(self):
        self.openDirectory()

    @pyqtSlot()
    def run_tests_on_click(self):
        self.runTests()
    
class CustomLabel(QLabel):
    
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            filename = os.path.basename(path)
            dirname = "../target/key"
            filecheck = os.path.join(dirname, filename)
            if os.path.isfile(path) and os.path.exists(filecheck):
                self.setText("Oops, that key already exists")
            elif os.path.isfile(path) and not os.path.exists(filecheck):
                self.setText(path)
                shutil.rmtree(dirname)
                os.mkdir(dirname)
                copy2(path, dirname)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_icon = QIcon("path to file")
    app.setWindowIcon(app_icon)
    ex = App()
    sys.exit(app.exec_())
