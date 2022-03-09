# Name: Holden Chen
# OSU Email: chenhol@oregonstate.edu
# Course: CS261 - Data Structures ; section 400
# Assignment: 6
# Due Date: 03/12/2022
# Description: This file contains an implementation of a HashMap using Separate Chaining.
# solution methods are: put(), get(), remove(), contains_key(), clear(), empty_pockets(),
# empty_buckets(), resize_tables(), table_load(), and get_keys()


from a6_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A6 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A6 HashMap implementation
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
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
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
            self.buckets.append(LinkedList())

    def get(self, key: str) -> object:
        """
        Takes a key parameter and returns the value associated
        with the given key. This method returns None if the given
        key is not in the hash map.
        """
        target_index = self.hash_function(key) % self.buckets.length()
        target_bucket = self.buckets[target_index]  # this is a LinkedList

        if self.size == 0 or target_bucket.length() == 0:
            return

        for node in target_bucket:

            if node.key == key:
                return node.value
            else:
                continue

        # no match found
        return

    def put(self, key: str, value: object) -> None:
        """
        Takes a key parameter and value parameter and updates
        the key/value pair in the hash map. If the given key
        exists, then the given value will replace the current
        value at that key. If the given key is not in the hash
        map, a new key/value pair will be added. This method
        returns None.
        """
        target_index = self.hash_function(key) % self.buckets.length()
        target_bucket = self.buckets[target_index]  # this is a LinkedList

        if target_bucket.length() == 0:
            target_bucket.insert(key, value)
            self.size += 1
            return

        for node in target_bucket:

            # overwrite the value if the key already exists
            if node.key == key:
                node.value = value
                return

            continue

        target_bucket.insert(key, value)
        self.size += 1

    def remove(self, key: str) -> None:
        """
        Takes a key parameter and removes the given key
        and its associated value from the hash map. If
        the key does not match any of the keys in the hash
        map, then this method makes no changes.
        """
        target_index = self.hash_function(key) % self.buckets.length()
        target_bucket = self.buckets[target_index]  # this is a LinkedList

        if self.size == 0 or target_bucket.length() == 0:
            return

        if target_bucket.remove(key) is True:
            self.size -= 1
            return

    def contains_key(self, key: str) -> bool:
        """
        Takes a key parameter and returns a boolean value
        that represents whether the given key is in the hash
        map or not. It returns True if the given key is in the
        hash map and returns false otherwise.
        """
        target_index = self.hash_function(key) % self.buckets.length()
        target_bucket = self.buckets[target_index]  # this is a LinkedList

        if self.size == 0 or target_bucket.length() == 0:
            return False

        for node in target_bucket:

            if node.key == key:
                return True
            else:
                continue

        # no match found
        return False

    def empty_buckets(self) -> int:
        """
        Takes no parameters and returns an integer that
        represents the number of empty buckets in the
        hash table.
        """
        number_of_empty_buckets = 0

        # count no. of empty buckets in the DA
        for index in range(self.buckets.length()):
            bucket = self.buckets[index]

            if bucket.length() == 0:
                number_of_empty_buckets += 1
            else:
                continue

        return number_of_empty_buckets

    def table_load(self) -> float:
        """
        Takes no parameters and returns a float value that
        represents the current hash table load factor.
        """
        number_of_elements_in_table = 0
        number_of_buckets = self.buckets.length()

        # accumulate number of elements in table
        for index in range(number_of_buckets):
            bucket = self.buckets[index]
            number_of_elements_in_table += bucket.length()

        # calculate and return the load factor
        load_factor = number_of_elements_in_table / number_of_buckets
        return load_factor

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes an integer parameter that represents the new
        capacity and changes the capacity of the internal
        hash table. This method returns None.
        """
        if new_capacity < 1:
            return

        new_da = DynamicArray()

        for index in range(new_capacity):
            new_da.append(LinkedList())

        for index in range(self.buckets.length()):
            bucket = self.buckets[index]  # this is a LinkedList

            for node in bucket:
                new_hash = self.hash_function(node.key)
                new_index = new_hash % new_capacity
                new_da[new_index].insert(node.key, node.value)

        self.capacity = new_capacity
        self.buckets = new_da

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
            bucket = self.buckets[index]

            for node in bucket:
                output_da.append(node.key)

        return output_da


# BASIC TESTING
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
