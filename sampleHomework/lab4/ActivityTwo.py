def main():
    word = input("Enter your word: ")
    word = word.lower()
    print(scrabble_score(word))

#This method calculates the scrabble score for a given word
def scrabble_score(word):
    score = 0
    letters = list(word)
    scores = {'e': 1, 'a': 1, 'i': 1, 'o': 1, 'n': 1, 'r': 1, 't': 1, 'l': 1, 's': 1, 'u': 1,
              'd': 2, 'g': 2,
              'b': 3, 'c': 3, 'm': 3, 'p': 3,
              'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
              'k': 5,
              'j': 8, 'x': 8,
              'q': 10, 'z': 10}

    for i in letters:
        score += scores[i]

    return score

main()