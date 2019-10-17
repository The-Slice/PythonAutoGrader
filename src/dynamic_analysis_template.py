import unittest
import subprocess
import sys

class DynamicAnalysis(unittest.TestCase):
    """ this class acts as a template for building an assignment's dynamic analysis suite"""

    def setUp(self):
        """ this method prepares the environment for testing"""
        pass

    def test_main(self):
        """ this test method is designed to run the assignment script as main and capture the output"""
        #exec_str = open("$target_script", "r").read()
        #print(exec_str)
        #exec(exec_str)
        subprocess.run([sys.executable, "$target_script"])

    def tearDown(self):
        """ this method restores the environment after testing"""
