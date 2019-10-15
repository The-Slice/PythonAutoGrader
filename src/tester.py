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

    def __init__(self):
        """ this __init__ realizes the dynamic_analysis_template using the given assignment's information, 
        then updates and reloads the dynamic_analysis module 
        """
        self.target_script = "sampleMain.py"
        self.out_capture = tempfile.TemporaryFile(mode="w+", delete=False)
        dynamic_analysis_template = Template(open("dynamic_analysis_template.py", "r").read())
        dynamic_analysis_template = dynamic_analysis_template.substitute(target_script=self.target_script)
        """
        tmp_module = tempfile.NamedTemporaryFile(suffix=".py", delete=False)
        print("BYETES", bytes(dynamic_analysis_template, encoding="utf-8"))
        tmp_module.write(bytes(dynamic_analysis_template, encoding="utf-8"))
        print("TMP MODULE", tmp_module.name)
        tmp_module.seek(0)
        #print("CONTENTS", tmp_module.read().decode("utf-8"))
        os.chdir(os.path.dirname(tmp_module.name))
        print("CURRDIR", os.getcwd())
        """
        #if(os.path.exists("dynamic_analysis.py")):
        #    os.remove("dynamic_analysis.py")
        tmp_module = open("dynamic_analysis.py", "w+")
        tmp_module.write(dynamic_analysis_template)
        tmp_module.close()
        #target_module = __import__(os.path.basename(tmp_module.name))
        #invalidate_caches()
        reload(dynamic_analysis)
        """
        target_module = import_module("dynamic_analysis.py")
        target_class = getattr(target_module, "DynamicAnalysis")
        dynamic_analysis_template = target_class()
        """

    def analyze_dynamically(self):
        """ this method performs the dynamic analysis routines that have been loaded in the dynamic_analysis module"""
        dynamic_test = unittest.TestLoader().loadTestsFromTestCase(dynamic_analysis.DynamicAnalysis)
        #unittest.TextTestRunner(stream=self.out_capture).run(dynamic_test)
        unittest.TextTestRunner(stream=self.out_capture).run(dynamic_test)

if __name__=="__main__":
    tester1 = Tester()
    tester1.analyze_dynamically()
    print(tester1.out_capture.read())
