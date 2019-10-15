def main():
    numOfComments = inlineCommentCounter("activityOne.py")
    print("Number of comments: {}".format(str(numOfComments)) )

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