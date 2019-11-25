import ctypes
import os
import re
import shutil
import sys
import multiprocessing
from zipfile import ZipFile
from shutil import copy2
from guiutil import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from tester import *
from commentSummary import CommentSummary 
BORDERSIZE = 10
DROPDOWN_LOC = 30
AUTOGRADER_PATH = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))
print("AUTOGRADER_PATH:", AUTOGRADER_PATH)
TARGET_DIR_PATH = os.path.join(AUTOGRADER_PATH, "target")
KEY_DIR_PATH = os.path.join(TARGET_DIR_PATH, "key")
CURRENT_GRADING_KEY_PATH = None
STUDENTWORKSOURCE = None

class QOutputLog(QPlainTextEdit):
    def write(self, string):
        self.insertPlainText(string)

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
                'Display Docstring': False,
                'Count Comments': False
                #'Display Comments': True 
            }
        )
        self.optionBoxes.add('Dynamic Analysis',  
            { # Format for adding buttons and other components to dropdown
            #   'Button label' : [Constructor for component, component height, component width, listener]
                'Edit Key': [QPushButton, 80, 20, self.openDirectory] 
            }
        )
        for opt in self.optionBoxes.children:
            opt.dropdown.clicked.connect(opt.getExpandListener())
    

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.center()
        self.setWindowIcon(QIcon(os.path.join(AUTOGRADER_PATH, 'img', 'pythonBlugold.ico')))
        
        gradeButton = QPushButton("Grade", self)
        gradeButton.move(BORDERSIZE, self.height-gradeButton.height()-BORDERSIZE)
        gradeButton.clicked.connect(self.grade_on_click)
        # need to connect this button to grade_button_click function
        # if you want a gui element to exist in the scope of the program it must be declared as self
        self.resultArea = QOutputLog(self)

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        openDir = QAction(QIcon('exit.png'), '&Import Directory', self)        
        openDir.setShortcut('Ctrl+D')
        openDir.setStatusTip('Open Directory')
        openDir.triggered.connect(self.zipdirectory_on_click)

        openFile = QAction(QIcon('exit.png'), '&Import Zip(s)', self)        
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open Zip(s)')
        openFile.triggered.connect(self.zipdialog_on_click)

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

        # text result area
        self.resultArea.resize(self.width*0.75, self.height*0.75)

        # attempt to use pyqt auto element resizing
        self.resultArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        print("Log of program status displayed below:\n", file=self.resultArea)
        self.resultArea.move(self.width/4-BORDERSIZE, self.height-self.resultArea.height()-BORDERSIZE)

        self.resultArea.setReadOnly(True)

        labelA = QLabel('Assignment Key:', self)
        labelA.adjustSize()
        labelA.move(self.width/4-BORDERSIZE, self.height-self.resultArea.height()-BORDERSIZE*4)


        self.dragdrop = KeyDrop('Drop key here', self)
        self.dragdrop.move(self.width/4-BORDERSIZE+labelA.width()+BORDERSIZE, self.height-self.resultArea.height()-self.dragdrop.height()-BORDERSIZE)
        self.dragdrop.resize((self.resultArea.width()-100)-labelA.width()-BORDERSIZE, 20)

        addKeyButton = QPushButton("Add key", self)
        addKeyButton.move(self.width/4-BORDERSIZE+labelA.width()+self.dragdrop.width()+5+BORDERSIZE, self.height-self.resultArea.height()-self.dragdrop.height()-BORDERSIZE-15)
        addKeyButton.clicked.connect(self.keydialog_on_click)

        self.show()

    #Utility for aloowing listeners to be set to functions on other classes without pyqt slots
    def setListener(self, button, function):
        button.clicked.connect(function)

   #opens directory filled with students zipped assignments
    def openDirectory(self):
	
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        ifileName = QFileDialog.getExistingDirectory(self,"Please select an Input Directory", options=options)
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
            for filename in os.listdir(ifileName):
                    if(filename.endswith(".zip")):

                        zipfileName = re.search('[^/]+$', filename)
                        zipfileNameParse = os.path.splitext(os.path.basename(zipfileName.group(0)))[0]
                        
                        with ZipFile(ifileName + "/" + filename , 'r') as zippedObject:
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
        print(files)
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
                with ZipFile(file , 'r') as zippedObject:
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
            self.dragdrop.setText(ifileName[0])
            copy2(ifileName[0], KEY_DIR_PATH)
            CURRENT_GRADING_KEY_PATH = os.path.join(KEY_DIR_PATH, os.path.basename(ifileName[0]))
    
        else:
            self.dragdrop.setText("Please select a key")

    def center(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    @pyqtSlot()
    def grade_on_click(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        ifileName = QFileDialog.getExistingDirectory(self,"Please select a Directory to Grade", options=options)
        STUDENTWORKSOURCE = ifileName
        print("\nGrading Directory:", STUDENTWORKSOURCE, file=self.resultArea)
        keyFileName = os.path.basename(self.dragdrop.text())
        CURRENT_GRADING_KEY_PATH = os.path.join(KEY_DIR_PATH, keyFileName)
        print("Using Grading Key: ", CURRENT_GRADING_KEY_PATH, file=self.resultArea)
        if not STUDENTWORKSOURCE is None and not CURRENT_GRADING_KEY_PATH is None:
            dnt = Tester(CURRENT_GRADING_KEY_PATH, AUTOGRADER_PATH)
            print("Grading Key Output:\n", dnt.key_output, file=self.resultArea)
            for root, dirs, files in os.walk(STUDENTWORKSOURCE):
                for student_dir in dirs:
                    for student_file in os.listdir(os.path.join(root, student_dir)):
                        filename = os.path.join(root, student_dir, student_file)
                        if not re.match(".*\.py.*", student_file) is None:
                            print("Analyzing: ", os.path.join(root, student_dir, student_file), file=self.resultArea)
                            comments = CommentSummary(filename, self.optionBoxes.getTestOptions('Comment Analysis'))
                            print(filename)
                            comments.run()
                            try:
                                dnt.analyze_dynamically(os.path.join(root, student_dir, student_file))
                            except BaseException as e:
                                print(e)
                                print("Could not analyze:", student_dir, file=self.resultArea)
            print(dnt.captured_output, file=self.resultArea)             #NOTE: currently dnt.captured_output is a temporary file and is filled cumulatively
                        
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
        self.setStyleSheet("background-color: white; border: 1px inset grey")

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
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    app_icon = QIcon("path to file")
    app.setWindowIcon(app_icon)
    ex = App()
    sys.exit(app.exec_())
