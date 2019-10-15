import sys
import ctypes
import sre_constants
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QPlainTextEdit, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
# The border that all pieces will abide by
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

        # elements
        button1 = QPushButton('samplebutton first', self)
        button2 = QPushButton('samplebutton second', self)
        resultArea = QPlainTextEdit(self)

        # button 1
        button1.setToolTip('This is an example button')
        button1.move(BORDERSIZE, BORDERSIZE)
        button1.clicked.connect(self.uno_on_click)

        # button 2
        button2.setToolTip('This is an example button')
        button2.move(BORDERSIZE, button1.height()+BORDERSIZE+3)
        button2.clicked.connect(self.dos_on_click)

        # text result area
        resultArea.resize(self.width*0.75, self.height*0.75)

        # attempt to use pyqt auto element resizing
        resultArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        resultArea.insertPlainText("Hello World.\n")
        resultArea.move(self.width/4-BORDERSIZE, self.height-resultArea.height()-BORDERSIZE)

        resultArea.setReadOnly(True)
        self.show()

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
