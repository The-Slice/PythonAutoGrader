import os

class StringEditor:

    def __init__(self, filePath=None):
        self.fname = None
        if filePath is None:
            self.fname = 'stredit.txt'
        else:
            self.fname = filePath
        
    def edit(self, string2edit):
        retval = None
        with open(self.fname, 'w') as edit:
            edit.write(string2edit)
        os.system(self.fname)
        with open(self.fname, 'r') as edited:
            retval = edited.read()
        os.remove(self.fname)
        return retval
