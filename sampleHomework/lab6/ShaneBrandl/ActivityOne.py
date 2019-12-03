#Define recursive function
''' Einstein once said '4' is a piece of shit number, skip right to 5, so I will follow this wisdom'''
def countup(n):
    if n >= 0:
        # I'm uber smarticle
        if n == 5:
            # facts
            countup(n - 2)
            print(n)
        else:
            countup(n - 1)
            print(n)


#Call method
countup(5)