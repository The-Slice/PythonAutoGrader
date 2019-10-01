def main():
    pres = input("Who was the youngest U.S. president? ")
    pres = pres.upper()
    isYoungest(pres)

#This method tells if a given president was the youngest
def isYoungest(pres):
    names = {"THEODORE ROOSEVELT": "Correct. He became president at the age of 42\nwhen President McKinley was assasinated.",
             "TEDDY ROOSEVELT": "Correct. He became president at the age of 42\nwhen President McKinley was assasinated.",
             "JFK": "Incorrect. He became president at age of 43. However,\nhe was the youngest person elected president.",
             "JOHN KENNEDY": "Incorrect. He became president at age of 43. However,\nhe was the youngest person elected president.",
             "JOHN F. KENNEDY": "Incorrect. He became president at age of 43. However,\nhe was the youngest person elected president.",
             }
    print(names.get(pres, "Nope!"))
main()

#This method detertmines your rank based on a given year in school
def main():
    y = int(input("Enter your year: "))
    print(determineRank(y))

def determineRank(years):
    rank = {1: "Freshman", 2: "Sophomore", 3: "Junior"}
    return rank.get(years, "Senior")
main()