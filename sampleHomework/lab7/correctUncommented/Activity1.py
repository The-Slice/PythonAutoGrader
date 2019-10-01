from sampleHomework.lab7.correctUncommented.Card import PlayingCard

spadesList = []
heartsList = []
diamondsList = []
clubsList = []

for i in range(0,13):
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


list = spadesList + heartsList + diamondsList + clubsList

for card in list:
    print(str(card))
