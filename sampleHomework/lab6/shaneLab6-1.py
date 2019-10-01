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
        finalString = string + finalString
        x = x + 1
        return repeatRecur(string, finalString, numberOfRepeats, x)

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
        counter = counter + 1
        y = y + 2
        product = product * y
        return multiplyEvensRecur(x,y,counter,product)

print(multiplyEvens(1))
print(multiplyEvens(2))
print(multiplyEvens(4))