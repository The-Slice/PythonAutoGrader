from sampleHomework.lab7.correctCommented.Dice import PairOfDice

pairOfDice1 = PairOfDice()

numDoubleSixes = 0

#Repeat 10,000 times
for x in range(0, 10000):

    found = False   #boolean whether sum=12 has been found

    for i in range(0,24):
        pairOfDice1.roll()
        if pairOfDice1.sum() == 12:
            found = True    #set found to true

    if found:
        numDoubleSixes += 1

#Print stats
print(numDoubleSixes/10000)