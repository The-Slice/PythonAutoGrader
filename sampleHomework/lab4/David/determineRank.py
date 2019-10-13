
def main():
    y = int(input("Enter your year: "))
    print(determineRank(y))
def determineRank(years):
    if years == 1:
        return "Freshman"
    elif years == 2:
        return "Sophomore"
    elif years == 3:
        return "Junior"
    else:
        return "Senior"
main()