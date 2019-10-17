def main():
    comment_summary_docstrings("../sampleHomework/lab7/correctCommented/Card.py")

    numOfComments = inlineCommentCounter("../sampleHomework/lab7/correctCommented/Card.py")
    print("Number of comments: {}".format(str(numOfComments)) )

def comment_summary_docstrings(path):
    ''' This method performs a comment summary for all docstring comments in a file.

    Parameters:
        path (str) : Relative path to the file being graded

    '''
    docStrings = comment_summary_get_docstrings(path)
    display_docstrings(docStrings)


def comment_summary_get_docstrings(path):
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


def display_docstrings(docStrings):
    ''' This method prints a list of docString style comments

    Parameters:
        docStrings (list) : A list of all docString style comments
    '''
    print("A total of *" + str(len(docStrings)) + "* docString style comments were found")

    for i in range(len(docStrings)):
        print("    -> " + docStrings[i])

def inlineCommentCounter(fileName):
    commentCount = 0
    for line in open(fileName):
        li = line.strip()
        if li.startswith("#"):
            commentCount += 1
        else:
            isComment = False
            for letter in li:
                if letter == '\"' and isComment == False:
                    isComment = True
                elif letter == '\"' and isComment == True:
                    isComment = False
                if letter == '#' and isComment == False:
                    commentCount += 1
    return commentCount

main()
