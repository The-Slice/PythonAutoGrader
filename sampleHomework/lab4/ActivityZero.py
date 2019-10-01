def main():
    l1 = [1,1,2,3,4,4,5,5,]
    l2 = [1,3,5, 6]
    print(removeDuplicates(l1))
    print(findItemsInBoth(l1,l2))
    print(findItemsInEither(l1,l2))

#This method removes duplicates
def removeDuplicates(list1):
    uniques  = set(list1)
    list2 = list(uniques)
    return list2

#This method finds numbers that are in both lists
def findItemsInBoth(list1, list2):
    list3 = list(set(list1).intersection(list2))
    return list3

#This method finds numbers that are in either list
def findItemsInEither(list1, list2):
    list3 = list(set(list1) | set(list2))
    return list3
main()