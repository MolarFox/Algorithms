# Rithesh Jayaram 2019

import random
import math

val_in = int(input("Value to determine: "))
coinArray = [1, 5, 9]

memo = [None] * (val_in+1)
memo[0] = 0

#------------------------------------------------------------------

# Bottom-up implementation
def bottomup_coinchange(value):
    for v in range(1, value+1):
        minCoins = math.inf
        for i in range(0, len(coinArray)):
            if coinArray[i] <= v:
                c = 1 + memo[v - coinArray[i]]
                if c < minCoins:
                    minCoins = c
        memo[v] = minCoins
    print(memo)
    return memo[value]

#------------------------------------------------------------------

# Top-down implementation
def topdown_coinchange(value):
    if memo[value-1] is not None:
        return memo[value-1]
    
    minCoins = math.inf
    for i in range(1, len(coinArray)):
        if coinArray[i] <= value:
            c = 1 + topdown_coinchange(value - coinArray[i])
            if c < minCoins:
                minCoins = c
    memo[value-1] = minCoins
    return memo[value-1]

#------------------------------------------------------------------

print(bottomup_coinchange(val_in))
#print(topdown_coinchange(val_in))