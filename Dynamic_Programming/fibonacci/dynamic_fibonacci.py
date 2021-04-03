# MolarFox 2018

def dynamic_fibonacci(num, memoized_results={}):
    """
    Dynamic implentation of fibonacci sequence, memoizes past results in an associative array and returns the number at
        position `num` in the sequence
        NB: Since Python dicts are mutable, any memoized results from previous runs will be kept for future calls
    :param num: Position in fibonacci sequence that is desired to be found
    :param memoized_results: Defaults to blank assosciative array - holds memoized results, needed for dynamic calling
    :return: Value in fibonacci sequence at the requested position
    :precondition: num is a valid positive integer, memoized_results is not passed if this is the root call of function
    :postcondition: Fibonacci value at requested position is passed, used mem is cleared by garbage collection C inbuilt
    :complexity: O(n) best case - effectively has to progressively add values in finding target value, linear complexity
                        actual number of calls made is higher, but roughly linearin growth
    """

    # Try to access and return memoized value, or move on if non-existent
    try:
        saved_num = memoized_results[num]
        return saved_num
    except KeyError:
        pass

    # Return 1 for 0th / 1st element (base case)
    if num <= 1:
        memoized_results[num] = 1
    # Else, recursive call to determine element (utilising memoization)
    else:
        memoized_results[num] = dynamic_fibonacci(num - 1, memoized_results) +\
                                dynamic_fibonacci(num - 2, memoized_results)

    # Target value should be memoized by this point - simply fetch and return it
    return memoized_results[num]


# ------------------------------------------------------------

print(dynamic_fibonacci(10))
