import ctypes
import os
import re
import shutil
import sys
import time
from zipfile import ZipFile
from shutil import copy2
from shutil import copy
import subprocess

SRCROOT = os.path.dirname(os.path.realpath(sys.argv[0]))
REPOROOT = os.path.dirname(SRCROOT)
subprocess.run(["python", "-m", "pip", "install", "-r", os.path.join(REPOROOT, "config\\pyreqs.txt")]);



import pip
import winshell
import pyshortcuts
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
	
        
		       
        self.setWindowIcon(QIcon('../img/pythonBlugold.ico'))
		
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

        self.desktopShortcut = QCheckBox("Create desktop shortcut", self)
        self.desktopShortcut.setChecked(True)
        self.startbar = QCheckBox("Create start menu shortcut", self)
        self.startbar.setChecked(True)
					
        layout = QVBoxLayout()
        layout.addWidget(self.browseButton)
        layout.addWidget(self.resultArea)	
        layout.addWidget(self.buildButton)	
        layout.addWidget(self.desktopShortcut)
        layout.addWidget(self.startbar)
		
        		
	    
        widget = QWidget()
        # widget.setLayout(horizontalLayout)
        self.setCentralWidget(widget)    
        
        # dock = QDockWidget()
        # dock.setWidget(self.resultArea)
		
        # self.addDockWidget(Qt.TopDockWidgetArea, dock)
        
        widget.setLayout(layout)
		
        self.show()
	
    def appendPlainText(self, text2Append, end='\n'):
        current = self.resultArea.toPlainText()
        new = current + end + text2Append
        self.resultArea.setPlainText(new)
        self.resultArea.update()
        self.update()
        self.resultArea.repaint()
        self.repaint()

    @pyqtSlot()
    def buildExecutable(self):
        self.buildButton.setEnabled(False)
        self.browseButton.setEnabled(False)
        
        self.appendPlainText('Installing prerequisite modules ... ')
        self.appendPlainText("done", end='')
        self.appendPlainText("Compiling script ... ")
        if(self.path != 'path'):
            args = [
                '-F',
                'autograder.py',
                'commentSummary.py',
                'guiutil.py',
                'tester.py',
                '--onefile',
                '--distpath', '%s/bin' % self.path,
                '--workpath', '%s' % self.path + '/workpath',
                '--specpath', '%s' % self.path,
                '--windowed'
            ]
            try:
                if sys.argv[1] == '--debug':
                    args.pop()
            except IndexError:
                pass
            try:
                PyInstaller.__main__.run(args)
            except:
                QMessageBox.question(self, 'Install unsuccessful', "Try picking a new install location", QMessageBox.Ok)
                app.exit()
        self.appendPlainText("done", end='')
        try:
            os.mkdir(os.path.join(self.path, "target"))
            os.mkdir(os.path.join(self.path, "target", "key"))
            os.mkdir(os.path.join(self.path, "target", 'temp'))
            os.mkdir(os.path.join(self.path, "img"))
            os.mkdir(os.path.join(self.path, "results"))

        except:
            pass
        for filename in os.listdir(os.path.join(REPOROOT, 'img')):
            shutil.copy(
                os.path.join(REPOROOT, "img", filename),
                os.path.join(self.path, "img", filename)
            )
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        pyshortcuts.make_shortcut(
            os.path.join(self.path, "bin", "autograder.exe"),
            name="AutoGrader",
            description="Python AutoGrader",
            terminal=False,
            icon=os.path.join(self.path, 'img', 'pythonBlugold.ico'),
            desktop=self.desktopShortcut.isChecked(),
            startmenu=self.startbar.isChecked()
        )
        resp = QMessageBox.question(self, 'Install successful', "You may new exit the program", QMessageBox.Ok)
        app.quit()
		
		
	
    def openDirectory(self):
	
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName= QFileDialog.getExistingDirectory(self,"Please Select a Directory", options=options)
        self.resultArea.setPlainText(fileName)		
        self.path = fileName
        self.buildButton.setEnabled(True)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False	
		
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_icon = QIcon('.img/pythonBlugold.ico')
    app.setWindowIcon(app_icon)
    ex = MyWindow()
    sys.exit(app.exec_())
    #TODO: DIRECTORY PERMISSION CHECKING
		
