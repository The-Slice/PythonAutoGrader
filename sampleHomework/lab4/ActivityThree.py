def main():
    topHitters = {"Gehrig": {"atBats": 8061, "hits": 2721},
                  "Ruth": {"atBats": 8399, "hits": 2873},
                  "Williams": {"atBats": 7706, "hits": 2654}}

    calculateAverage(topHitters)

#This method calculates the batting average for given players in a dictionary
def calculateAverage(topHitters):
    for key in topHitters:
        avg = str(round(topHitters[key]['hits'] / topHitters[key]['atBats'], 3))
        print(key + ": " + avg)

main()