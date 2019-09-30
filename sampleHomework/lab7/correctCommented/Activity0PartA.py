from sampleHomework.lab7.correctCommented.Dice import PairOfDice

#Create dice
pairOfDice1 = PairOfDice()
pairOfDice2 = PairOfDice()

#Roll dice
pairOfDice1.roll()
pairOfDice2.roll()

#Print totals
print("Player 1: " + str(pairOfDice1.sum()))
print("Player 2: " + str(pairOfDice2.sum()))

#Print winner
if pairOfDice1.sum() > pairOfDice2.sum():
    print("Player 1 wins.")
elif pairOfDice2.sum() > pairOfDice1.sum():
    print("Player 2 wins.")
else:
    print("Tie")