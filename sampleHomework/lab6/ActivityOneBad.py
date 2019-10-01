def countup(n):
    if n >= 0:
        countup(n - 1)
        print(n)

countup(5)