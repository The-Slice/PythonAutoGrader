import unittest
import subprocess
import sys
from $assignment_instance_name import *


class DynamicAnalysis(unittest.TestCase):
    """ this class acts as a template for building an assignment's dynamic analysis suite"""

    def need(self):
        print("NEEEEEEED")

    def setUp(self):
        """ this method prepares the environment for testing"""
        pass

    def test_main(self):
        """ this test method is designed to run the assignment script as main and capture the output"""
        subprocess.run([sys.executable, "$assignment_instance"])

$method_test_stubs

    def tearDown(self):
        """ this method restores the environment after testing"""
        pass
