from .Dice import PairOfDice

#Incorrect. Spacing is all wrong

pairOfDice1 = PairOfDice()

    numDoubleSixes = 0

for x in range(0, 10000):

    found = False

    for i in range(0,24):
         pairOfDice1.roll()
                if pairOfDice1.sum() == 12:
              found = True

    if found:
              numDoubleSixes += 1

print(numDoubleSixes/10000)