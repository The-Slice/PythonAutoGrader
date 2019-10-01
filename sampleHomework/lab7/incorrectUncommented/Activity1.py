from sampleHomework.lab7.incorrectUncommented.Card import PlayingCard

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
