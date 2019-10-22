import random
'''This class represents a Playing card'''
class PlayingCard:
    def __init__(self, rank="queen", suit="hearts"):
        """Creates a representation of a card - rank and suit"""
        self._rank = rank
        self._suit = suit   #This is an inline comment

    def setRank(self, rank):
        '''sets the rank of the card'''
        self._rank = rank

    def setSuit(self, suit):
        '''sets the suit of the card'''
        self._suit = suit

    def getRank(self):
        '''retuns the rank of the card'''
        return self._rank

    def getSuit(self):
        '''retuns the suit of the card'''
        return self._suit

    def selectAtRandom(self):
        '''sets the rank and suit to a random card'''
        # Randomly select a rank and a suit.
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9',
                 "10", "jack", "queen", "king", "ace"]
        self._rank = random.choice(ranks)
        self._suit = random.choice(["spades", "hearts", "clubs", "diamonds"])

    def __str__(self):
        '''returns string representation of card'''
        return self._rank + " of " + self._suit
