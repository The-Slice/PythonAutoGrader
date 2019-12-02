def countup(n):
    if n >= 0:
        countup(n - 2)
        print(n)

countup(5)