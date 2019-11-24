import unittest
import subprocess
import sys
try:
    from test import *
except:
    print("ASSIGNMENT INSTANCE:", r"E:\Programs\autograder\target\studentWork\snyderja8768\test.py", "FAILED TO INTERPRET")

class DynamicAnalysis(unittest.TestCase):
    """ this class acts as a template for building an assignment's dynamic analysis suite"""

    def setUp(self):
        """ this method prepares the environment for testing"""
        pass

    def test_main(self):
        """ this test method is designed to run the assignment script as main and capture the output"""
        try:
            subprocess.run([sys.executable, r"E:\Programs\autograder\target\studentWork\snyderja8768\test.py"])
        except:
            print("ASSIGNMENT INSTANCE:", r"E:\Programs\autograder\target\studentWork\snyderja8768\test.py", "FAILED TO COMPLETE")


    def test_setUp(self):
        self = None
        pass

    def test_test_main(self):
        self = None
        pass

    def test_test___init__(self):
        self = None
        pass

    def test_test_initUI(self):
        self = None
        pass

    def test_test_setListener(self):
        self = None
        pass

    def test_test_openDirectory(self):
        self = None
        pass

    def test_test_openFileNamesDialog(self):
        self = None
        pass

    def test_test_openKeyDialog(self):
        self = None
        pass

    def test_test_center(self):
        self = None
        pass

    def test_test_grade_on_click(self):
        self = None
        pass

    def test_test_zipdialog_on_click(self):
        self = None
        pass

    def test_test_zipdirectory_on_click(self):
        self = None
        pass

    def test_test_keydialog_on_click(self):
        self = None
        pass

    def test_test___init__(self):
        self = None
        pass

    def test_test_dragEnterEvent(self):
        self = None
        pass

    def test_test_dropEvent(self):
        self = None
        pass

    def test_tearDown(self):
        self = None
        pass



    def tearDown(self):
        """ this method restores the environment after testing"""
        pass
