def main():
    l1 = [1,1,2,3,4,4,5,5,]
    l2 = [1,3,5, 6]
    print(removeDuplicates(l1))
    print(findItemsInBoth(l1,l2))
    print(findItemsInEither(l1,l2))

def removeDuplicates(list1):
    set1 = set([])
    set2 = set([])
    for item in list1:
        if item not in set2:
            set1.add(item)
    return set1

def findItemsInBoth(list1, list2):
    set3=[]
    for item in list1:
        if (item in list2) and (item not in set3):
            set3.append(item)
    return set3

def findItemsInEither(list1, list2):
    set3=[]
    for item in list1:
        if (item not in set3):
            set3.append(item)
    for item in list2:
        if (item not in set3):
            set3.append(item)
    return set3
main()