# Shane Brandl
# Lab 6 - Recursion
# Problems 2 & 4

#Excercise 2
def repeat(string, numberOfRepeats):
    x = 0
    finalString = ""
    if x == numberOfRepeats:
        return "'" + finalString + "'"
    else:
        return repeatRecur(string, finalString, numberOfRepeats, x)

def repeatRecur(string, finalString, numberOfRepeats, x):
    if x == numberOfRepeats:
        return "'" + finalString + "'"
    else:
        finalString = finalString + string
        return repeatRecur(string, finalString, numberOfRepeats, x+1)

print(repeat("hi", 3))
print(repeat("don't print me ", 0))

#Excercise 4
def multiplyEvens(x):
    counter = 1
    product = 2
    y = 2
    if counter == x:
        return product
    else:
        return multiplyEvensRecur(x,y,counter,product)

def multiplyEvensRecur(x,y,counter,product):
    if counter == x:
        return product
    else:
        y = y + 2
        return multiplyEvensRecur(x,y,counter+1,product*y)

print(multiplyEvens(1))
print(multiplyEvens(2))
print(multiplyEvens(4))