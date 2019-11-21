import ctypes
import os
import re
import shutil
import sys
from zipfile import ZipFile
from shutil import copy2
from guiutil import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
BORDERSIZE = 10
DROPDOWN_LOC = 30

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

        self.testSuiteDict = {
            'Comment Analysis': True,
            'Dynamic Analysis': False
        }

        self.optionBoxes = TestConfigOptionBox(BORDERSIZE, DROPDOWN_LOC, self)
        self.optionBoxes.add('Comment Analysis', 
            { 
                'Display Docstring': True, 
                'Count Comments': False,
                'Display Comments': True 
            }
        )
        self.optionBoxes.add('Dynamic Analysis', {'1': False, '2': False})
        for opt in self.optionBoxes.children:
            opt.dropdown.clicked.connect(opt.getExpandListener())

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.center()
        self.setWindowIcon(QIcon('../img/pythonBlugold.ico'))
        
        gradeButton = QPushButton("Grade", self)
        gradeButton.move(300, 50)
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

        openKey = QAction(QIcon('exit.png'), '&Open Key', self)        
        openKey.setShortcut('Ctrl+F')
        openKey.setStatusTip('Open Key')
        openKey.triggered.connect(self.keydialog_on_click)


        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openDir)
        fileMenu.addAction(openFile)
        fileMenu.addAction(openKey)
        fileMenu.addAction(exitAct)
        
        self.dragdrop = KeyDrop('Drop key here', self)
        labelA = QLabel('Assignment Key:', self)
        labelA.move(332, 175)
        labelA.resize(160,40)

        
        self.dragdrop.move(495, 175)
        self.dragdrop.resize(500,40)

        # text result area
        resultArea.resize(self.width*0.75, self.height*0.75)

        # attempt to use pyqt auto element resizing
        resultArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        resultArea.insertPlainText("Hello World.\n")
        resultArea.move(self.width/4-BORDERSIZE, self.height-resultArea.height()-BORDERSIZE)

        resultArea.setReadOnly(True)
        self.show()

    #Utility for aloowing listeners to be set to functions on other classes without pyqt slots
    def setListener(self, button, function):
        button.clicked.connect(function)

    #opens directory filled with students zipped assignments
    def openDirectory(self):
	
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        ifileName = QFileDialog.getExistingDirectory(self,"Please Select an Input Directory", options=options)
        ofileName = QFileDialog.getExistingDirectory(self,"Please Select an Output Directory", options=options)
        
		#check if temp folder is created, if yes replace with new one
		#NOTE: crashes if file explorer is running in the background and is currently inside 'temp' directory
		#PermissionError exception fixes this issue           

        if (ifileName and ofileName):
            try:
                os.mkdir(ofileName + "/studentWork")
            except FileExistsError:
                try:
                    shutil.rmtree(ofileName + "/studentWork")
                    os.mkdir(ofileName + "/studentWork")
                except PermissionError:
                    print("studentWork folder is in use")
                    QMessageBox.about(self , "Attention" , "unzip failed") 
                    return 
        
            #for each zip folder unzip the folder
            for subdir, dirs, files in os.walk(ifileName):
                for file in files:
                    if(file.find('.zip') != -1):

                        zipfileName = re.search('[^/]+$', file)
                        zipfileNameParse = os.path.splitext(os.path.basename(zipfileName.group(0)))[0]
                        
                        with ZipFile(zipfileName.group(0) , 'r') as zippedObject:
                            zippedObject.extractall(zipfileNameParse)
                        
                        #file is moved to temp once zip file is extracted into its own filename			
                        os.rename(zipfileNameParse, ofileName +"/studentWork/" + zipfileNameParse)
        else:
            pass
                    
			
    #opens zipped directory filled with students zipped assignments
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"Please Select a Zip File(s)", "","Zip Files (*.zip *.7zip)", options=options)
        ofileName = QFileDialog.getExistingDirectory(self,"Please Select an Output Directory", options=options)
		#check if temp folder is created, if yes replace with new one
		#NOTE: crashes if file explorer is running in the background and is currently inside 'temp' directory
		#PermissionError exception fixes this issue
        if (files and ofileName):
            try:
                os.mkdir(ofileName + "/studentWork")
            except FileExistsError:
                try:
                    shutil.rmtree(ofileName + "/studentWork")
                    os.mkdir(ofileName + "/studentWork")
                except PermissionError:
                    print("studentWork folder is in use")
                    QMessageBox.about(self , "Attention" , "unzip failed") 
                    return 
                    
            #for each zip folder unzip the folder
            for file in files:

                zipfileName = re.search('[^/]+$', file)
                zipfileNameParse = os.path.splitext(os.path.basename(zipfileName.group(0)))[0]
                
                with ZipFile(zipfileName.group(0) , 'r') as zippedObject:
                    zippedObject.extractall(zipfileNameParse)
                
                #file is moved to temp once zip file is extracted into its own filename			
                os.rename(zipfileNameParse, ofileName + "/studentWork/" + zipfileNameParse)
        else:
            pass

    def openKeyDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        ifileName = QFileDialog.getOpenFileName(self,"Please Select a Key File", "","Key Files (*py)", options=options)
		#check if temp folder is created, if yes replace with new one
		#NOTE: crashes if file explorer is running in the background and is currently inside 'temp' directory
		#PermissionError exception fixes this issue
        
        if (ifileName[0] != ""):
            dirname = "../target/key"
            
            if (os.path.isfile(os.path.basename(ifileName[0]))):

                self.dragdrop.setText("Oops, that key already exists")

            else :
                self.dragdrop.setText(ifileName[0])
                copy2(ifileName[0], dirname)
            
        else:
            self.dragdrop.setText("Please select a key")

           
        
                
    def center(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    @pyqtSlot()
    def grade_on_click(self):
        # TODO: IMPLEMENT
        pass

    @pyqtSlot()
    def zipdialog_on_click(self):
        self.openFileNamesDialog()

    @pyqtSlot()
    def zipdirectory_on_click(self):
        self.openDirectory()

    @pyqtSlot()
    def keydialog_on_click(self):
        self.openKeyDialog()
        

class KeyDrop(QLabel):
    
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
