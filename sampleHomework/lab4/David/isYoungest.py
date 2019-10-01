def main():
    pres = input("Who was the youngest U.S. president? ")
    pres = pres.upper()
    isYoungest(pres)
def isYoungest(pres):
    if (pres == "THEODORE ROOSEVELT") or (pres == "TEDDY ROOSEVELT") or (pres =="TR"):
        print("Correct. He became president at the age of 42")
        print("when President McKinley was assasinated.")
    elif (pres == "JFK" )or (pres == "JOHN KENNEDY") or (pres == "JOHN F. KENNEDY"):
        print("Incorrect. He became president at age of 43. However,")
        print("he was the youngest person elected president.")
    else:
        print("Nope!")
main()
