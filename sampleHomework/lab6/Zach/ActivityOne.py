'''Straight forward code I think'''
def countup(n):
    # yes
    if n >= 0:
        # no
        countup(n - 1)
        # maybe
        print(n)
# so
countup(5)