# MolarFox 2019

import random

def countingSort(in_list):
    
    min_num = in_list[0]
    max_num = in_list[0]
    
    for num in in_list:
        if num > max_num:
            max_num = num
        if num < min_num:
            min_num = num

    countlist = [0 for i in range(max_num-min_num+1)]
    for num in in_list:
        countlist[num - min_num] += 1
    
    for i in range(1, len(countlist)):
        countlist[i] += countlist[i-1]
    
    outlist = [None for i in range(len(in_list))]
    for num in in_list:
        outlist[countlist[num - min_num]-1] = num
        countlist[num - min_num] -= 1
    
    return outlist

if __name__ == "__main__":
    list_size = int(input("Number of elements to generate: "))
    max_val =   int(input("Maximum value of any element: "))
    min_val =   int(input("Minimum value of any element: "))

    # Generate das elementes
    unsorted_list = []
    random.seed()
    for j in range(list_size):
        unsorted_list.append(random.randint(min_val, max_val))

    print(unsorted_list)
    print()
    print(countingSort(unsorted_list))
