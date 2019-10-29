import random

class PairOfDice:
    def __init__(self):
        self._dice1 = 0;
        self._dice2 = 0;

    def getDice1(self):
        return self._dice1

    def getDice2(self):
        return self._dice2

    def roll(self):
        self._dice1 = random.choice(range(1, 7))
        self._dice2 = random.choice(range(1, 7))

    def sum(self):
        return self._dice1 + self._dice2



