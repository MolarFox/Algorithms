# MolarFox 2018
# Dynamic Knapsack


def knapsack_dp(values, weights, max_cap):
    """
    uses Dynamic Programming to solve the knapsack problem for params given
    :param values: the values of items available
    :param weights: the weights of items available
    :param max_cap: the maximum capacity (integer, pls not too huge)
    :return: returns the matrix holding items used
    """
    # for c and k, dp is better of c,k-1 and c-weight(k),k-1 + value(k)

    # Initialise blank 2D matrix to hold final results
    item_count = len(weights)
    sol_matrix = [None]*(item_count+1)     # Initialise rows (as none)
    for row in range(item_count+1):         # Initialise columns, zero fill all
        sol_matrix[row] = [0]*(max_cap + 1)

    for curritem in range(1,item_count+1):
        for currcap in range(1,max_cap+1):
            no_use_it = sol_matrix[curritem-1][currcap]  # Weight before using item

            how_heavy = weights[curritem-1]
            cost = values[curritem-1]
            reduced_cap = currcap - how_heavy

            if reduced_cap >= 0:  # Can fit item in
                use_it = sol_matrix[curritem-1][reduced_cap] + cost
            else:
                use_it = 0  # Not enough space left for item

            best = max(no_use_it, use_it)   # Determine if using or not using item is optimal
            sol_matrix[curritem][currcap] = best

            '''
            # Is the item being used in final cycle / max ks size?
            if currcap == max_cap:
                if best != no_use_it:
                    sol_matrix[curritem][max_cap+1] += 1
            '''

    # Substract weight to determine how many of each item were used
    items_used = [0]*len(values)
    i = len(sol_matrix) - 2
    while i >= 0:
        change = sol_matrix[i + 1][max_cap] - sol_matrix[i][max_cap]
        if change != 0:
            items_used[i] = change // weights[i]
        i -= 1
    '''    
    print()
    print(items_used)
    print()
    '''

    return items_used


# ------------------------------------------------------------


weights =   [3, 4, 7,  8,  9]
vals =      [4, 5, 10, 11, 13]

# NB: function outputs array of items used
out = knapsack_dp(vals, weights, 17)

# Add total weight and value based on items used
total_value = 0
total_weight = 0
for item in range(len(out)):
    if out[item] == 1:
        total_value += vals[item]
        total_weight += weights[item]

print("Items used were" + str(out))
print()
print("Total value: " + str(total_value))
print("Total weight: " + str(total_weight))
