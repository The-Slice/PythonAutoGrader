class CommentSummary:

    def __init__(self, filename, opts):
        self.fileName = filename
        self.opts = opts

    def run(self):
        if self.opts[0] == 'Count Docstring':
            return self.count_docstrings(self.fileName)
        if self.opts[0] == 'Display Docstring':
            return self.comment_summary_docstrings(self.fileName)
        comments = self.inlineCommentCounter(self.fileName)
        if self.opts[0] == 'Count Comments':
            return "Number of comments: {}".format(str(len(comments)))
            
        #if self.opts['Display Comments'] is not None and self.opts['Display Comments']:
        #    for comment in comments:
        #        print("\t {}".format(comment))

    def comment_summary_docstrings(self, path):
        ''' This method performs a comment summary for all docstring comments in a file.

        Parameters:
            path (str) : Relative path to the file being graded

        '''
        docStrings = self.comment_summary_get_docstrings(path)
        return self.display_docstrings(docStrings)


    def comment_summary_get_docstrings(self, path):
        ''' This method returns a list of all docString style comments

        Parameters:
            path (str) : Relative path to the file being graded

        Returns:
            docStrings (list) : A list containing the content of each docString comment
        '''
        file = open(path, encoding="utf-8")
        text = file.read()
        #print(text)

        indices = []        # Holds indices of comments
        docStrings = []     # Holds content of comments

        # Search for indices starting w/ '''
        index = 0
        while index < len(text):
            index = text.find("'''", index)
            if index == -1:
                break
            indices.append(index)
            index += 3  # 3 characters '''

        # Search for indices starting w/ """
        index = 0
        while index < len(text):
            index = text.find('"""', index)
            if index == -1:
                break
            indices.append(index)
            index += 3  # 3 characters '''

        indices.sort() # Keeps comments in order if both """ and ''' are used

        # Build list of comment content
        while len(indices) > 1:
            start = indices.pop(0)
            end = indices.pop(0)
            end += 3
            docStrings.append(text[start:end])

        return docStrings
    
    def count_docstrings(self, path):
        docStrings = self.comment_summary_get_docstrings(path)
        return "Number of docstrings: " + str(len(docStrings)) 

    def display_docstrings(self, docStrings):
        ''' This method prints a list of docString style comments

        Parameters:
            docStrings (list) : A list of all docString style comments
        '''
        string = "";

        for i in range(len(docStrings)):
            string = string + ("\n    -> " + docStrings[i])
            
        if(string == ""):
            string = " -> No Docstring detected"
            
        return string + "\n"

    def inlineCommentCounter(self, fileName):
        comments = []
        commentCount = 0
        for line in open(fileName, encoding='utf-8'):
            li = line.strip()
            if li.startswith("#"):
                commentCount += 1
                comments.append(li)
            else:
                isComment = False
                count = 0
                for letter in li:
                    if letter == '\"' and isComment == False:
                        isComment = True
                    elif letter == '\"' and isComment == True:
                        isComment = False
                    if letter == '#' and isComment == False:
                        commentCount += 1
                        word = li[count:len(li)]
                        comments.append(word)
                        count = 0
                    count+=1
        return comments
