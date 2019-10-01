import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Auto_Grader'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        button1 = QPushButton('samplebutton uno', self)
        button2 = QPushButton('samplebutton dos', self)
        
        button1.setToolTip('This is an example button')
        button1.move(100,70)
        button1.clicked.connect(self.uno_on_click)
        
        button2.setToolTip('This is an example button')
        button2.move(100,40)
        button2.clicked.connect(self.dos_on_click)
        
        self.show()

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
