from .Dice import PairOfDice

pairOfDicee1 = PairOfDice() #Incorrect. Spelling mistake
pairOfDice2 = PairOfDice()

pairOfDice1.roll()
pairOfDice2.roll()

print("Player 1: " + str(pairOfDice1.sum()))
print("Player 2: " + str(pairOfDice2.sum()))

if pairOfDice1.sum() > pairOfDice2.sum():
    print("Player 1 wins.")
elif pairOfDice2.sum() > pairOfDice1.sum():
    print("Player 2 wins.")
else:
    print("Tie")
