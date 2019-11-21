import sys
import ctypes
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from zipfile import ZipFile
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

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.center()
        # elements
        button1 = QPushButton('samplebutton uno', self)
        button2 = QPushButton('samplebutton dos', self)
        button3 = QPushButton('Select Homework Zip(s)', self)
        button4 = QPushButton('Select Homework Directory', self)
		
        button5 = QPushButton('Grade', self)
		
        resultArea = QPlainTextEdit(self)

        # button 1
        button1.setToolTip('This is an example button')
        button1.move(BORDERSIZE, BORDERSIZE)
        button1.clicked.connect(self.uno_on_click)

        # button 2
        button2.setToolTip('This is an example button')
        button2.move(BORDERSIZE, button1.height()+BORDERSIZE+3)
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
    app_icon = QIcon("path to file")
    app.setWindowIcon(app_icon)
    ex = App()
    sys.exit(app.exec_())
