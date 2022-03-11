# Name: Holden Chen
# OSU Email: chenhol@oregonstate.edu
# Course: CS261 - Data Structures ; section 400
# Assignment: 6
# Due Date: 03/12/2022
# Description: This file contains an implementation of a HashMap using Open Addressing.
# solution methods are: put(), get(), remove(), contains_key(), clear(), empty_pockets(),
# empty_buckets(), resize_tables(), table_load(), and get_keys()


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """
        Takes no parameters and removes all the key/value
        pairs from the hash map. This method returns None
        and DOES NOT change the underlying capacity
        of the hash table.
        """
        # just reinitialize the buckets DA and size; don't change capacity
        self.buckets = DynamicArray()
        self.size = 0

        # populate new DA with buckets (Linked Lists)
        for _ in range(self.capacity):
            self.buckets.append(None)

    def get(self, key: str) -> object:
        """
        Takes a key parameter and returns the value associated
        with the given key. This method returns None if the given
        key is not in the hash map.
        """
        initial_index = self.hash_function(key) % self.buckets.length()

        if self.buckets[initial_index] is not None:

            if self.buckets[initial_index].is_tombstone is False and self.buckets[initial_index].key == key:
                return self.buckets[initial_index].value

            # quadratic probing required
            probe_val = 1
            target_index = (initial_index + probe_val * probe_val) % self.buckets.length()

            while probe_val < self.buckets.length():

                if self.buckets[target_index] is not None and self.buckets[target_index].is_tombstone is False:

                    if self.buckets[target_index].key == key:
                        return self.buckets[target_index].value
                    else:
                        probe_val += 1
                        target_index = (initial_index + probe_val * probe_val) % self.buckets.length()
                else:
                    probe_val += 1
                    target_index = (initial_index + probe_val * probe_val) % self.buckets.length()

            # no match found
            return

        # quadratic probing required
        probe_val = 1
        target_index = (initial_index + probe_val * probe_val) % self.buckets.length()

        while probe_val < self.buckets.length():

            if self.buckets[target_index] is not None and self.buckets[target_index].is_tombstone is False:

                if self.buckets[target_index].key == key:
                    return self.buckets[target_index].value
                else:
                    probe_val += 1
                    target_index = (initial_index + probe_val * probe_val) % self.buckets.length()
            else:
                probe_val += 1
                target_index = (initial_index + probe_val * probe_val) % self.buckets.length()
        # no match found
        return

    def put(self, key: str, value: object) -> None:
        """
        Takes a key parameter and value parameter and updates
        the key/value pair in the hash map. If the given key
        exists, then the given value will replace the current
        value at that key. If the given key is not in the hash
        map, a new key/value pair will be added. This method
        returns None
        """
        # if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        if self.table_load() >= 0.5:
            self.resize_table(self.capacity*2)

        initial_index = self.hash_function(key) % self.buckets.length()

        if self.buckets[initial_index] is None:
            self.buckets[initial_index] = HashEntry(key, value)
            self.size += 1
            return

        if self.buckets[initial_index].is_tombstone:
            self.buckets[initial_index].key = key
            self.buckets[initial_index].value = value
            self.buckets[initial_index].is_tombstone = False
            self.size += 1
            return

        if self.buckets[initial_index].key == key:
            self.buckets[initial_index].value = value
            return

        # quadratic probing required
        probe_val = 1
        target_index = (initial_index + probe_val * probe_val) % self.buckets.length()

        while probe_val < self.buckets.length():

            if self.buckets[target_index] is None:
                self.buckets[target_index] = HashEntry(key, value)
                self.size += 1
                return

            if self.buckets[target_index].is_tombstone:
                self.buckets[target_index].key = key
                self.buckets[target_index].value = value
                self.buckets[target_index].is_tombstone = False
                self.size += 1
                return

            if self.buckets[target_index].key == key:
                self.buckets[target_index].value = value
                return

            probe_val += 1
            target_index = (initial_index + probe_val * probe_val) % self.buckets.length()

    def remove(self, key: str) -> None:
        """
        Takes a key parameter and removes the given key
        and its associated value from the hash map. If
        the key does not match any of the keys in the hash
        map, then this method makes no changes.
        """
        initial_index = self.hash_function(key) % self.buckets.length()

        if self.buckets[initial_index] is not None:

            if self.buckets[initial_index].is_tombstone is False and self.buckets[initial_index].key == key:
                self.buckets[initial_index].is_tombstone = True
                self.size -= 1
                return

            # quadratic probing required
            probe_val = 1
            target_index = (initial_index + probe_val * probe_val) % self.buckets.length()

            while probe_val < self.buckets.length():

                if self.buckets[target_index] is not None and self.buckets[target_index].is_tombstone is False:

                    if self.buckets[target_index].key == key:
                        self.buckets[target_index].is_tombstone = True
                        self.size -= 1
                        return
                    else:
                        probe_val += 1
                        target_index = (initial_index + probe_val * probe_val) % self.buckets.length()
                else:
                    probe_val += 1
                    target_index = (initial_index + probe_val * probe_val) % self.buckets.length()
            # not match found
            return

        # quadratic probing required
        probe_val = 1
        target_index = (initial_index + probe_val * probe_val) % self.buckets.length()

        while probe_val < self.buckets.length():

            if self.buckets[target_index] is not None and self.buckets[target_index].is_tombstone is False:

                if self.buckets[target_index].key == key:
                    self.buckets[target_index].is_tombstone = True

                    return
                else:
                    probe_val += 1
                    target_index = (initial_index + probe_val * probe_val) % self.buckets.length()
            else:
                probe_val += 1
                target_index = (initial_index + probe_val * probe_val) % self.buckets.length()
        # no match found
        return

    def contains_key(self, key: str) -> bool:
        """
        Takes a key parameter and returns a boolean value
        that represents whether the given key is in the hash
        map or not. It returns True if the given key is in the
        hash map and returns False otherwise.
        """
        initial_index = self.hash_function(key) % self.buckets.length()

        if self.size == 0:
            return False

        if self.buckets[initial_index] is not None and self.buckets[initial_index].is_tombstone is False:

            if self.buckets[initial_index].key == key:
                return True

            probe_val = 1
            target_index = (initial_index + probe_val * probe_val) % self.buckets.length()

            while probe_val < self.buckets.length():

                if self.buckets[target_index] is not None and self.buckets[target_index].is_tombstone is False:

                    if self.buckets[target_index].key == key:
                        return True
                    else:
                        probe_val += 1
                        target_index = (initial_index + probe_val * probe_val) % self.buckets.length()
                else:
                    probe_val += 1
                    target_index = (initial_index + probe_val * probe_val) % self.buckets.length()
            return False

        probe_val = 1
        target_index = (initial_index + probe_val * probe_val) % self.buckets.length()

        while probe_val < self.buckets.length():
            if self.buckets[target_index] is not None and self.buckets[target_index].is_tombstone is False:

                if self.buckets[target_index].key == key:
                    return True
                else:
                    probe_val += 1
                    target_index = (initial_index + probe_val * probe_val) % self.buckets.length()
            else:
                probe_val += 1
                target_index = (initial_index + probe_val * probe_val) % self.buckets.length()
        return False

    def empty_buckets(self) -> int:
        """
        Takes no parameters and returns an integer that
        represents the number of empty buckets in the
        hash table.
        """
        return self.capacity - self.size

    def table_load(self) -> float:
        """
        Takes no parameters and returns a float value that
        represents the current hash table load factor.
        """
        return self.size / self.buckets.length()

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes an integer parameter that represents the new
        capacity and changes the capacity of the internal
        hash table. This method returns None. If the new_capacity
        less than 1 or less than the number of elements in the hash
        map, then no modifications are made.
        """
        # if new_capacity not valid, then return
        if new_capacity < 1 or new_capacity < self.size:
            return

        temp_hash_map = HashMap(new_capacity, self.hash_function)

        # rehash non-deleted entries into new table
        for index in range(self.buckets.length()):

            if self.buckets[index] is not None and self.buckets[index].is_tombstone is False:
                temp_hash_map.put(self.buckets[index].key, self.buckets[index].value)

        self.buckets = temp_hash_map.buckets
        self.capacity = temp_hash_map.capacity

    def get_keys(self) -> DynamicArray:
        """
        Takes no parameters and returns a DynamicArray object
        that contains all the keys that exist in the hash
        map.
        """
        output_da = DynamicArray()

        if self.size == 0:
            return output_da

        for index in range(self.buckets.length()):

            if self.buckets[index] is not None and self.buckets[index].is_tombstone is False:
                output_da.append(self.buckets[index].key)

        return output_da


if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    # this test assumes that put() has already been correctly implemented
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
