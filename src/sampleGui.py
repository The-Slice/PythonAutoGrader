import sys
import ctypes
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from guiutil import *
from zipfile import ZipFile
from commentSummary import CommentSummary
BORDERSIZE = 10


class App(QWidget):

    def __init__(self):
        user32 = ctypes.windll.user32
        screenWidth = user32.GetSystemMetrics(0)
        screenHeight = user32.GetSystemMetrics(1)
        super().__init__()
        self.title = 'Python Auto Grader'
        self.width = screenWidth / 2
        self.height = screenHeight / 2
        self.left = screenWidth / 2 - self.width / 2
        self.top = screenHeight / 2 - self.height / 2
        self.testSuiteDict = {
            'Comment Analysis': False,
            'Dynamic Analysis': False
        }

        self.testSuiteRun = { # This dictionary assigns the string ID of the test to the constructor
            'Comment Analysis': CommentSummary
        }

        self.toBeGraded = []

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.center()
        # elements
        #button1 = QCheckBox('Comment Analysis', self)
        #self.button1 = TestConfigOption(
        #    'Comment Analysis', BORDERSIZE, 
        #    BORDERSIZE, self, 
        #    {"opt1": False, "opt2": False}
        #)
        self.optionBoxes = TestConfigOptionBox(BORDERSIZE, BORDERSIZE, self)
        self.optionBoxes.add('Comment Analysis', {'1': False, '2': False})
        self.optionBoxes.add('Dynamic Analysis', {'1': False, '2': False})
        for opt in self.optionBoxes.children:
            opt.dropdown.clicked.connect(opt.getExpandListener())
        #toggle_button1 = QToolButton(self, checkable=True, checked=False)
        #toggle_button1.setArrowType(Qt.RightArrow)
        #button2 = QCheckBox('Dynamic Analysis', self)
        button3 = QPushButton('Select Homework Zip(s)', self)
        button4 = QPushButton('Select Homework Directory', self)
		
        button5 = QPushButton('Grade', self)
		
        resultArea = QPlainTextEdit(self)

        # button 1
        #self.button1.dropdown.clicked.connect(self.comment_config_dropdown)
        #button1.setToolTip('This is an example button')
        #button1.move(BORDERSIZE, BORDERSIZE)
        #button1.clicked.connect(self.comment_on_click)
        #toggle_button1.move(BORDERSIZE + 130, BORDERSIZE)
        #Stoggle_button1.clicked.connect()
        # button 2
        #button2.setToolTip('This is an example button')
        #button2.move(BORDERSIZE, button1.height()+BORDERSIZE+3)
        #button2.clicked.connect(self.dynamic_on_click)	

        #Sbutton3.setToolTip('Select Homework Zip(s)')
        button3.move(200,40)
        button3.clicked.connect(self.zipdialog_on_click)

        button4.setToolTip('Select Homework Directory')
        button4.move(200,10)
        button4.clicked.connect(self.dirdialog_on_click)

        button5.setToolTip('Grade')
        button5.move(200,10)
        button5.clicked.connect(self.grade_assignments)

        # text result area
        resultArea.resize(self.width*0.75, self.height*0.75)

        # attempt to use pyqt auto element resizing
        resultArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        resultArea.insertPlainText("Hello World.\n")
        resultArea.move(self.width/4-BORDERSIZE, self.height-resultArea.height()-BORDERSIZE)

        resultArea.setReadOnly(True)
        self.show()

    def setListener(self, button, function):
        button.clicked.connect(function)

    #opens directory filled with students zipped assignments
    def openDirectory(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dirPath = QFileDialog.getExistingDirectory(self,"Please Select a Directory", options=options)
        if dirPath:
            for fileName in os.listdir(dirPath):
                print(dirPath + fileName)
                self.toBeGraded.append(dirPath + fileName)
			
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
    	for key in self.testSuiteDict:
            for assignment in self.toBeGraded:
                if self.testSuiteDict[key]:
                    test = self.testSuiteRun[key](assignment)
                    test.run()


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
    def comment_on_click(self):
        self.testSuiteDict['Comment Analysis'] = not self.testSuiteDict['Comment Analysis']
        print(self.testSuiteDict)
    
    @pyqtSlot()
    def comment_config_dropdown(self):
        self.button1.display_opts()
        

    @pyqtSlot()
    def dynamic_on_click(self):
        self.testSuiteDict['Dynamic Analysis'] = not self.testSuiteDict['Dynamic Analysis']
        print(self.testSuiteDict)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_icon = QIcon("path to file")
    app.setWindowIcon(app_icon)
    ex = App()
    sys.exit(app.exec_())
