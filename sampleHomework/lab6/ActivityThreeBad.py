def indexOf(text,string):
    L = len(text)
    if string:
        print('elif ' + text + ' == ' + string[0])
    if len(string) == 0:
        return -1
    elif text == string[:L]:
        return 0
    else:
        return 1 + indexOf(text, string[1:])

text1 = 'no'
string1 = 'noodle'

print(indexOf(text1,string1))
