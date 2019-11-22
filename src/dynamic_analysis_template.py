import unittest
import subprocess
import sys
try:
    from $assignment_instance_name import *
except:
    print("ASSIGNMENT INSTANCE:", r"$assignment_instance", "FAILED TO INTERPRET")

class DynamicAnalysis(unittest.TestCase):
    """ this class acts as a template for building an assignment's dynamic analysis suite"""

    def setUp(self):
        """ this method prepares the environment for testing"""
        pass

    def test_main(self):
        """ this test method is designed to run the assignment script as main and capture the output"""
        try:
            subprocess.run([sys.executable, r"$assignment_instance"])
        except:
            print("ASSIGNMENT INSTANCE:", r"$assignment_instance", "FAILED TO COMPLETE")

$method_test_stubs

    def tearDown(self):
        """ this method restores the environment after testing"""
        pass
