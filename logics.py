import os

def organize(lst:list, num:int, index:int):
    length = len(lst)
    starting = num * index
    if (starting + num) <= len(lst):
        stopping = starting + num
    elif (starting + num) > len(lst):
        stopping = starting + length % num

    a = starting
    lst2 = list()
    for c in range(starting, stopping):
        item = os.path.basename(os.path.normpath(lst[c]))
        lst2.append(f"{a}. {item}")
        a += 1

    return lst2

    
