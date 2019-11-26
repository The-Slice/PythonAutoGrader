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

spadesList = []
heartsList = []
diamondsList = []
clubsList = []

for i in range(0,9): #Incorrect. Should be 13, not 9
    playingCard = PlayingCard()
    playingCard.selectAtRandom()

    if playingCard.getSuit() == "spades":
        spadesList.append(playingCard)
    elif playingCard.getSuit() == "hearts":
        heartsList.append(playingCard)
    elif playingCard.getSuit() == "diamonds":
        diamondsList.append(playingCard)
    elif playingCard.getSuit() == "clubs":
        clubsList.append(playingCard)
    else:
        print("there has been a mistake")


list = spadesList + heartsList + diamondsList + diamondsList #Incorrect. Should add each clubsList instead of the 2nd diamondsList

for card in list:
    print(str(card))
