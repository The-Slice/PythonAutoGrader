
def main():
    print(battingAverges(topHitters))


topHitters = {"Gehrig": {"atBats": 8061, "hits": 2721},
              "Ruth": {"atBats": 8399, "hits": 2873},
              "Williams": {"atBats": 7706, "hits": 2654}}


def battingAverges(dict):
    for a in topHitters:
        print(a)
        for b in topHitters[a]:
             print (b, topHitters[a][b])
main()