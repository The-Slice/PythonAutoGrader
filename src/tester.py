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
from string import Template


class Tester():
    """ this class performs and logs static and/or dynamic analysis for a given assignment """

    def __init__(self, target_script):
        """ this __init__ realizes the dynamic_analysis_template using the given assignment's information, 
        then updates and reloads the dynamic_analysis module 
        """
        self.target_script = target_script
        self.out_capture = tempfile.TemporaryFile(mode="w+", delete=False)
        dynamic_analysis_template = Template(open("dynamic_analysis_template.py", "r").read())
        dynamic_analysis_template = dynamic_analysis_template.substitute(target_script=self.target_script)
        tmp_module = open("dynamic_analysis.py", "w+")
        tmp_module.write(dynamic_analysis_template)
        tmp_module.close()
        reload(dynamic_analysis)

    def analyze_dynamically(self):
        """ this method performs the dynamic analysis routines that have been loaded in the dynamic_analysis module"""
        dynamic_test = unittest.TestLoader().loadTestsFromTestCase(dynamic_analysis.DynamicAnalysis)
        unittest.TextTestRunner(stream=self.out_capture).run(dynamic_test)

if __name__=="__main__":
    args=sys.argv[1:]
    try:
        tester1 = Tester(str(args[0]))
        tester1.analyze_dynamically()
        print(tester1.out_capture.read())
    except:
        print("Could not locate script:", str(args[0]))