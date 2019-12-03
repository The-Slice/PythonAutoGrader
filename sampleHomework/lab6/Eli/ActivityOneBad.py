def countup(n):
    if n == 8:
        # why the hell would I print 8? Ridiculous
        countup(n - 2)
    if n >= 0:
        countup(n - 2)
        print(n)

countup(5)