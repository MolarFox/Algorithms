# MolarFox 2018
# Building a Rehash Method

from referential_array import build_array

class HashTableLinear:

    prime_list = [25717, 102877, 205759, 411527,
                 823117, 1646237, 3292489, 6584983,
                 13169977]

    def __init__(self):
        self.count = 0
        size = 0
        self.a = 31
        self.table_max_size = HashTableLinear.prime_list[size]
        self.array = build_array(self.table_max_size)

    # -----------------------------------------------------------------------

    def __setitem__(self, key, value):
        position = self.hash_value(key)
        for _ in range(self.table_max_size):
            if self.array[position] is None:
                self.array[position] = (key, value)
                self.count += 1
                return
            elif self.array[position][0] == key:
                self.array[position] = (key, value)
                return
            else:
                position = (position+1) % self.table_max_size

        self.__rehash__()
        self.__setitem__(key, value)

    # -----------------------------------------------------------------------

    def hash_value(self, input_string):
        return ord(input_string[0]) % self.table_max_size

    # -----------------------------------------------------------------------

    def __rehash__(self):
        temp = self.array
        self.table_max_size = self.table_max_size * 2
        self.array = build_array(self.table_max_size)
        for item in temp:
            if item is not None:
                self.insert(item)
