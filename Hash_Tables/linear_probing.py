# MolarFox 2018
# Linear Probing Hash Function


from referential_array import build_array


class hashTable:

    def __init__(self, table_size=11):
        self.array = build_array(table_size)
        self.table_max_size = table_size
        self.count = 0

    # -----------------------------------------------------------------------

    def __str__(self):
        string = ""
        for index in range(self.table_max_size):
            if self.array[index] is None:
                pass
            else:
                string += str((index, str(self.array[index])))
                string += ", "
        return string

    # -----------------------------------------------------------------------

    def __getitem__(self, val):
        item = self.probe(val)

        if item is None:
            raise KeyError(str(val)+" not found")
        return item

    # -----------------------------------------------------------------------

    def __contains__(self, key):
        item = self.probe(key)
        if item is None:
            return False
        return True

    # -----------------------------------------------------------------------

    def insert(self, val):
        pos = self.probe(val, False)
        if pos is not None:
            self.array[pos] = val
            return True
        return False

    # -----------------------------------------------------------------------

    def __len__(self):
        return self.count

    # -----------------------------------------------------------------------

    def hash_value(self, input_string):
        return ord(input_string[0]) % self.table_max_size

    # -----------------------------------------------------------------------

    def probe(self, val, find=True):
        key = self.hash_value(val)
        keyInitial = key
        count = 0
        if find:
            while (self.array[key] is not None) and (self.array[key] != val):
                count += 1
                if count == self.table_max_size:
                    return None
                key = (key + 1) % self.table_max_size
            return key
        else:
            while self.array[key] is not None:
                count += 1
                if count == self.table_max_size:
                    return None
                key = (key + 1) % self.table_max_size
            return key

    # -----------------------------------------------------------------------


input_strings = ["Eva", "Amy", "Tim", "Ron", "Jan", "Kim", "Dot", "Ann", "Jim", "Jon"]

muh_table = hashTable()

for string in input_strings:
    muh_table.insert(string)

print(muh_table)
print()
print(muh_table['Jim'])
print(muh_table['Jon'])
print(muh_table['Joe'])
