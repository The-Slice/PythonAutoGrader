""" tester.py
This module contains the necessary routines to perform analysis of a single-script Python project.
@author Bryce Bjorkman
"""
from importlib import import_module, invalidate_caches, reload
import os
import sys
if(os.path.exists("dynamic_analysis.py")):
    os.remove("dynamic_analysis.py")
with open("dynamic_analysis.py", "w+") as f:
    f.write("pass")
import dynamic_analysis
import unittest
import tempfile
import re
from string import Template

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
                        method_def = method_def + (param.strip(),)   # add the stripped parameter to the method definition tuple
            method_defs.append(method_def)                           # add the complete method definition tuple to the list
    return method_defs                                               # return the method definitions list

def generate_method_test_stubs(method_defs):
    """ this method generates unit test stubs for a list of method definitions """
    method_test_stubs = "\n"                                                  # make a string for method test stubs
    for method_def in method_defs:                                            # iterate through each method definition
        method_test_stub = "    def test_" + method_def[0] + "(self):\n"      # begin method test stub with test method definition line
        if len(method_def) > 1:                                               # if the method definition includes parameters
            method_params = method_def[1:]                                    # grab just the parameters from the method definition
            for method_param in method_params:                                # iterate through the method parameters
                method_test_stub += "        " + method_param + " = None\n"   # simply initialize a variable for each parameter to None
        method_test_stub += "        pass\n\n"                                # add a line to pass as default
        method_test_stubs += method_test_stub                                 # append method test stub to the list 
    return method_test_stubs                                                  # return the method test stubs list

class Tester():
    """ this class performs and logs static and/or dynamic analysis for a given assignment """

    def __init__(self, grading_key):
        """ this __init__ realizes the dynamic_analysis_template using the given assignment's information, 
        then updates and reloads the dynamic_analysis module 
        """
        self.grading_key = grading_key                                                                  # keep the handle to the grading key
        self.captured_output = tempfile.TemporaryFile(mode="w+", delete=False)                          # a place to write a test's output to
        dynamic_analysis_template = Template(open("dynamic_analysis_template.py", "r").read())          # load the generic unit test suite template
        self.method_defs = find_method_defs(self.grading_key)                                           # get all method defs from grading key
        self.method_test_stubs = generate_method_test_stubs(self.method_defs)                           # make a list of unit test stubs for each key method defs
        dynamic_analysis_template = dynamic_analysis_template.substitute(grading_key=self.grading_key, 
                                                                         method_test_stubs = self.method_test_stubs)  # substitute key fields
        tmp_module = open("dynamic_analysis.py", "w+")                                                  # open the unit test module instance
        tmp_module.write(dynamic_analysis_template)                                                     # write the new unit test module to the test module instance
        tmp_module.close()                                                                              # close the test module instance's file
        reload(dynamic_analysis)                                                                        # reload the test module instance so this Tester has access

    def analyze_dynamically(self):
        """ this method performs the dynamic analysis routines that have been loaded in the dynamic_analysis module"""
        dynamic_test = unittest.TestLoader().loadTestsFromTestCase(dynamic_analysis.DynamicAnalysis)    # grab tests from the test module instance
        unittest.TextTestRunner(stream=self.captured_output).run(dynamic_test)                          # run tests and pipe to captured_output

if __name__=="__main__":
    try:
        args=sys.argv[1:]
        tester1 = Tester(str(args[0]))
        tester1.analyze_dynamically()
        print(tester1.captured_output.read())
    except BaseException as e:
        if len(args) < 1:
            print("No arguments provided")
            sys.exit(1)
        raise e
