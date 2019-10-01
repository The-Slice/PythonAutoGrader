#Define recursive function
def countup(n):
    if n >= 0:
        countup(n - 1)
        print(n)

#Call method
countup(5)