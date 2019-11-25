import ctypes
import os
import re
import shutil
import sys
import time
from zipfile import ZipFile
from shutil import copy2
from guiutil import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import PyInstaller.__main__
import PyInstaller.config




 
class MyWindow(QMainWindow):
 
    path = "path"
 
    def __init__(self):
	
        super().__init__()
        self.setWindowTitle('Autograder Install Wizard') 
	
        
		       
        self.setWindowIcon(QIcon('.img/pythonBlugold.ico'))
		
        self.buildButton = QPushButton("Build", self)
        self.buildButton.setEnabled(False)
        self.buildButton.resize(50,32)	
        
        self.buildButton.clicked.connect(self.buildExecutable)
        self.browseButton = QPushButton("Browse", self)
        self.buildButton.resize(50,32)
        self.browseButton.clicked.connect(self.openDirectory)
		
        self.resultArea = QPlainTextEdit(self)
        self.resultArea.setReadOnly(True)
        self.resultArea.setPlainText("Add a path with browse. . .")
		
		
					
        layout = QVBoxLayout()
        layout.addWidget(self.buildButton)
        layout.addWidget(self.resultArea)		
        layout.addWidget(self.browseButton)
		
        		
	    
        widget = QWidget()
        # widget.setLayout(horizontalLayout)
        self.setCentralWidget(widget)    
        
        # dock = QDockWidget()
        # dock.setWidget(self.resultArea)
		
        # self.addDockWidget(Qt.TopDockWidgetArea, dock)
        
        widget.setLayout(layout)
		
        self.show()
	
    @pyqtSlot()
    def buildExecutable(self):
        if(self.path != 'path'):
            PyInstaller.__main__.run([
			    '-F',
                'autograder.py',
			    'commentSummary.py',
			    'guiutil.py',
			    'inlineCommentCounter.py',
			    'tester.py',
                '--onefile',
			    #'--add-data', 'img/pythonBlugold.png; %s/pythonBlugold.png' % self.path,
			    '--distpath', '%s/bin' % self.path,
			    '--workpath', '%s' % self.path + '/workpath',
         	    '--specpath', '%s' % self.path,
            ])
			
        os.mkdir(os.path.join(self.path, "target"))
        os.mkdir(os.path.join(self.path, "target", "key"))		
		
        self.resultArea.setPlainText("autograder build successfull")
        time.sleep(5)
        sys.exit(app.exec_())
		
	
    def openDirectory(self):
	
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName= QFileDialog.getExistingDirectory(self,"Please Select a Directory", options=options)
        self.resultArea.setPlainText(fileName)		
        self.path = fileName
        self.buildButton.setEnabled(True)
		
		
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_icon = QIcon('.img/pythonBlugold.ico')
    app.setWindowIcon(app_icon)
    ex = MyWindow()
    sys.exit(app.exec_())
		
