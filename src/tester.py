""" tester.py
This module contains the necessary routines to perform analysis of a single-script Python project.
@author Bryce Bjorkman
"""
from importlib import import_module, invalidate_caches, reload
import os
import sys
import io
import unittest
from shutil import copy2
import tempfile
import re
import editor
import inspect
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import imp
from string import Template
from contextlib import redirect_stdout

#DYNAMIC_ANALYSIS_TEMPLATE = 'import runpy\nimport unittest\nimport subprocess\nimport sys\ntry:\n\tfrom $assignment_instance_name import *\nexcept:\n\tprint("ASSIGNMENT INSTANCE:", r"$assignment_instance", "FAILED TO INTERPRET")\n\nclass DynamicAnalysis(unittest.TestCase):\n\n\tdef setUp(self):\n\t\tpass\n\n\tdef test_main(self):\n\t\ttry:\n\t\t\trunpy.run_path(r"$assignment_instance", {}, "__main__")#subprocess.run([sys.executable, r"$assignment_instance"])\n\t\texcept:\n\t\t\tprint("ASSIGNMENT INSTANCE:", r"$assignment_instance", "FAILED TO COMPLETE")\n\n$method_test_stubs\n\n\tdef tearDown(self):\n\t\tpass'
DYNAMIC_ANALYSIS_TEMPLATE = '''
import runpy
import unittest
import subprocess
import sys
try:
    from $assignment_instance_name import *
except:
    print("ASSIGNMENT INSTANCE:", r"$assignment_instance", "FAILED TO INTERPRET")
    
class DynamicAnalysis(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_main(self):
        GLOBALS = {} # This is a dictionary for passing global variables to the program
        try:
            runpy.run_path(r"$assignment_instance", GLOBALS, "__main__")
        except:
            print("ASSIGNMENT INSTANCE:", r"$assignment_instance", "FAILED TO COMPLETE")
$method_test_stubs
    def tearDown(self):
        pass
'''

def find_method_defs(fname):
    """ this method finds all method definitions within a file """
    lines = []                                                       # make a list for lines
    with open(fname, "r") as f:                                      # open the file containing method defs
        lines = f.readlines()                                        # get each line from the file
    method_defs = []                                                 # make a list for method definitions
    for line in lines:                                               # iterate through each line of the file
        matches = re.search(r"^.*def\s*(\w*)\((.*)\):.*$", line)     # match against the regex for a Python method definition
        if not matches is None:                                      # if the line is a method definition
            groups = matches.groups()                                # get the captured groups from the line        
            method_def = (groups[0],)                                # start our method definition tuple with the identifier
            if len(groups) > 1:                                      # if the current method definition included any parameters
                params = groups[1].split(',')                        # separate the parameters from the method definition
                for param in params:                                 # for each 'parameter'
                    if not param is "":                              # if the 'parameter' isn't just incident whitespace
                        method_def = method_def + (param.strip().split("=")[0],)   # add the stripped parameter to the method definition tuple
            method_defs.append(method_def)                           # add the complete method definition tuple to the list
    return method_defs                                               # return the method definitions list

def generate_method_test_stubs(method_defs):
    """ this method generates unit test stubs for a list of method definitions """
    method_test_stubs = "\n"                                                  # make a string for method test stubs
    for method_def in method_defs:                                            # iterate through each method definition
        method_test_stub = "\tdef test_" + method_def[0] + "(self):\n"      # begin method test stub with test method definition line
        if len(method_def) > 1:                                               # if the method definition includes parameters
            method_params = method_def[1:]                                    # grab just the parameters from the method definition
            for method_param in method_params:                                # iterate through the method parameters
                method_test_stub += "\t\t" + method_param + " = None\n"   # simply initialize a variable for each parameter to None
        method_test_stub += "\t\tpass\n\n"                                # add a line to pass as default
        method_test_stubs += method_test_stub                                 # append method test stub to the list 
    return method_test_stubs                                                  # return the method test stubs list

class Tester():
    """ this class performs and logs static and/or dynamic analysis for a given assignment """

    def __init__(self, grading_key, parent_dir):
        """ this __init__ realizes the dynamic_analysis_template using the given assignment's information, 
        then updates and reloads the dynamic_analysis module 
        """
        self.tempdir= os.path.join(parent_dir, "target", "temp")
        sys.path.insert(0,self.tempdir)
        self.grading_key = grading_key                                                                  # keep the handle to the grading key
        self.captured_output = ""                                                                       # a place to write a test's output to
        dynamic_analysis_template = Template(DYNAMIC_ANALYSIS_TEMPLATE)                                 # load generic unit test suite 
        self.method_defs = find_method_defs(self.grading_key)                                           # get all method defs from grading key
        self.method_test_stubs = generate_method_test_stubs(self.method_defs)                           # make a list of unit test stubs for each key method defs
        self.dynamic_analysis_template = dynamic_analysis_template.substitute(grading_key=self.grading_key.replace("\\", "\\\\"), 
                                                                         method_test_stubs=self.method_test_stubs,
                                                                         output_path="$output_path",
                                                                         assignment_instance_name="$assignment_instance_name",
                                                                         assignment_instance="$assignment_instance")  # substitute key fields
        self.analyze_dynamically(self.grading_key)
        self.key_output = self.captured_output
        self.captured_output = ""
        #editor.edit("dynamic_analysis.py")

    def analyze_dynamically(self, target_script):
        """ this method performs the dynamic analysis routines that have been loaded in the dynamic_analysis module"""
        output_buffer = io.StringIO()                                            # a place to write a test's output to
        #sys.stdout = output_buffer
        copy2(target_script, self.tempdir)                                       #copy the target script to the tempdir 
        target_script_name = os.path.basename(target_script).split('.py')[0]
        target_script_test_suite_path = os.path.join(self.tempdir, target_script_name + "_dynamic_analysis.py")
        target_script_test_suite_name = target_script_name  + "_dynamic_analysis"
        target_script_test_suite = open(target_script_test_suite_path, "w+")
        target_script_test_suite.write(Template(self.dynamic_analysis_template).substitute(output_path=os.path.abspath(os.path.join(self.tempdir, "output.txt")),
                                                                                           assignment_instance=os.path.abspath(target_script),
                                                                                           assignment_instance_name=target_script_name))
        target_script_test_suite.close()
        print("BEFORE LOADING IMP")
        sys.stdout = open(os.devnull, "w")
        module = imp.load_source(target_script_test_suite_name, os.path.abspath(target_script_test_suite_path))
        sys.stdout = sys.__stdout__
        print("AFTER LOADING IMP")
        dynamic_analysis = getattr(module, "DynamicAnalysis")
        dynamic_test = unittest.TestLoader().loadTestsFromTestCase(dynamic_analysis)    # grab tests from the test module instance
        print("BEFORE MAKING TESTRUNNER")
        testrunner = unittest.TextTestRunner(stream = sys.stdout)
        print("BEFORE RUNNING TESTRUNNER")
        with redirect_stdout(output_buffer):
            testrunner.run(dynamic_test)                                                # run tests and pipe to captured_output
        sys.stdout = sys.__stdout__
        print("CAPTURED_OUTPUT:\n", output_buffer.getvalue())
        self.captured_output = output_buffer.getvalue()
        try:
            os.remove(os.path.join(self.tempdir, os.path.basename(target_script_name)))
        except:
            pass

if __name__=="__main__":
    try:
        args=sys.argv[1:]
        tester1 = Tester(str(args[0]))
        tester1.analyze_dynamically(".\\fakemain_instance.py")
        print(tester1.captured_output.read())

    except BaseException as e:
        if len(args) < 1:
            print("No arguments provided")
            sys.exit(1)
        raise e
