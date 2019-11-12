class CommentSummary:

    def __init__(self, filename):
        self.fileName = filename

    def run(self):
        self.comment_summary_docstrings(self.fileName)

        comments = self.inlineCommentCounter(self.fileName)
        print("Number of comments: {}".format(str(len(comments))))
        print("Comments: ")
        for comment in comments:
            print("\t {}".format(comment))

    def comment_summary_docstrings(self, path):
        ''' This method performs a comment summary for all docstring comments in a file.

        Parameters:
            path (str) : Relative path to the file being graded

        '''
        docStrings = self.comment_summary_get_docstrings(path)
        self.display_docstrings(docStrings)


    def comment_summary_get_docstrings(self, path):
        ''' This method returns a list of all docString style comments

        Parameters:
            path (str) : Relative path to the file being graded

        Returns:
            docStrings (list) : A list containing the content of each docString comment
        '''
        file = open(path)
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


    def display_docstrings(self, docStrings):
        ''' This method prints a list of docString style comments

        Parameters:
            docStrings (list) : A list of all docString style comments
        '''
        print("A total of *" + str(len(docStrings)) + "* docString style comments were found")

        for i in range(len(docStrings)):
            print("    -> " + docStrings[i])

    def inlineCommentCounter(self, fileName):
        comments = []
        commentCount = 0
        for line in open(fileName):
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
