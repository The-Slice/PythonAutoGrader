from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functools import partial

class TestConfigOptionBox:
    """
    This class is primarily a holder for multiple TestConfigOption
    objects. It handles passing information between the interface 
    and the driver, as well as changing the checkbox locations when
    options are expanded
    Params:
    (int) xloc: the x axis on the parent GUI that the nested components will be drawn
    (int) yloc: the y axis on the parent GUI that the nested components will be drawn
    (PyQT5.QMainWindoe) parent: The gui that the box will attach to

    """
    def __init__(self, xloc, yloc, parent):
        self.x = xloc
        self.y = yloc
        self.lowerBound = yloc
        self.parent = parent
        self.children = []
        self.testdict = {}
        self.collapsed = []

    def add(self, name, opts=None):
        """
        Adds a child TestConfigOption to self
        Params:
        (str) name: label of the child dropdown ment
        (dictionary) opts: a dictionary of toggleable options for the dropdown menus
        """
        
        self.children.append(TestConfigOption(name, self.x, self.lowerBound, self.parent, opts=opts, opsbox=self))
        self.collapsed.append(self.children[-1].collapsed)
        self.lowerBound = self.children[-1].y + 20
        self.testdict[name] = [False, self.children[-1]]
        self.parent.setListener(self.testdict[name][1].testCheck, partial(self.toggleTest, name))

    def toggleTest(self, name):
        """
        This function takes a test in the testdict and reverses it's current boolean value
        Params:
        (str) name: name of the test to toggle
        """
        self.testdict[name][0] = not self.testdict[name][0]

    def getTestOptions(self, key):
        return self.testdict[key][1].getConfig()
    
    def reshape(self):
        for num, opt in enumerate(self.children):
            if self.collapsed[num] != opt.collapsed and num < len(self.children) - 1:
                self.collapsed[num] = opt.collapsed
                low = self.children[num].y
                if opt.collapsed:
                    self.children[num + 1].shiftUp(low + 20)
                else:
                    self.children[num + 1].shiftDown(low + 25)        

class TestConfigOption:
    def __init__(self, name, xloc, yloc, parent, opts=None, opsbox=None):
        if opsbox is not None:
            self.inBox = True
            self.opsbox = opsbox
        
        self.ybound = yloc
        self.tempbuttons = []
        self.collapsed = True
        self.parent = parent
        self.testCheck = QCheckBox(name, parent)
        self.x = xloc
        self.y = yloc
        self.dropdown = QToolButton(parent, checkable=True, checked=False)
        self.dropdown.setFixedSize(20,20)
        if opts is None:
            self.options = {}
        else:
            self.options = opts

        self.testCheck.move(xloc, yloc)
        self.dropdown.move(xloc + 140, yloc)
        self.dropdown.setArrowType(Qt.LeftArrow)
        self.dropdown.show()
        self.testCheck.adjustSize()
        self.testCheck.show()
        self.parent.setListener(self.dropdown, self.getExpandListener)
    
    def getConfig(self):
        return self.options

    def shiftDown(self, y):
        self.y = y
        self.testCheck.move(self.x, y)
        self.dropdown.move(self.x + 140, y)
        for temp in self.tempbuttons:
            self.y += temp[1]
            temp[0].move(self.x + 10, self.y)
    
    def shiftUp(self, y):
        self.y = y
        self.testCheck.move(self.x, y)
        self.dropdown.move(self.x + 140, y)
        for temp in self.tempbuttons:
            self.y += temp[1]
            temp[0].move(self.x + 10, self.y)


    def display_opts(self): #opts{name : [type constructor]}
        if self.collapsed:
            self.dropdown.setArrowType(Qt.DownArrow)
            for num, option in enumerate(self.options):
                yChange = None
                opt = self.options[option]
                if not isinstance(opt, list):
                    self.y += 17
                    yChange = 17
                    temp = QCheckBox(option, self.parent)
                    if self.options[option]:
                        temp.setChecked(True)
                    temp.move (self.x + 10, self.y)
                    temp.show()
                    self.parent.setListener(temp, partial(self.toggleOpts, option))
                else:
                    self.y += opt[2]
                    yChange = opt[2]
                    temp = opt[0](option, self.parent)
                    temp.move(self.x+15, self.y)
                    temp.setFixedSize(opt[1],opt[2])
                    temp.show()
                    self.parent.setListener(temp, opt[3])
                self.tempbuttons.append([temp, yChange])
                self.parent.show()
                
            self.collapsed = False

        else:
            self.collapsed = True
            self.dropdown.setArrowType(Qt.LeftArrow)
            while len(self.tempbuttons):
                temp = self.tempbuttons.pop()
                button = temp[0]
                button.hide()
                self.y -= temp[1]
        self.opsbox.reshape()

    def toggleOpts(self, name):
        self.options[name] = not self.options[name]

    def getExpandListener(self):
        return self.display_opts

    def getOptions(self):
        opts = []
        for option in self.options:
            opts.append(option)
        return options

