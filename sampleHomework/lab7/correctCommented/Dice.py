import random

'''This class represents a set of dice'''
class PairOfDice:
    def __init__(self):
        '''Create the dice'''
        self._dice1 = 0;
        self._dice2 = 0;

    def getDice1(self):
        '''returns value of die 1'''
        return self._dice1

    def getDice2(self):
        '''returns value of die 2'''
        return self._dice2

    def roll(self):
        '''simulates rolling both dice'''
        self._dice1 = random.choice(range(1, 7))
        self._dice2 = random.choice(range(1, 7))

    def sum(self):
        '''returns the sum of the dice'''
        return self._dice1 + self._dice2



