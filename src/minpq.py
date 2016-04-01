# Class for the indexed priority queue. It uses the binary heap structure and a
# directory to keep the index information for given key value. Each datapoint
# will be (key, value), and the priority will be determined by the value.

import numpy as np

class indexedMinPQ:
    """
    Class for the indexed priority queue.
    (1) It uses the binary heap structure.
    (2) Two directories to keep the relations between indices and keys value. 
    (3) Each datapoint will be (key, value) pair, and the priority will be 
        determined by the value.
    """
    def __init__(self, dtype='float'):
        """
        Constructor
        Input:
            dtype (str): datatype for values (ex: 'int', 'float') 
                         (default: 'float')
        """
        self.array = np.zeros(2, dtype=dtype)  
                    # numpy array to store values for heap structure
                    # (initially two elements are needed)
        self.heap_size = 0 # Number of data points stored.
        self.index_to_key = {}  # dict (key: index, value: key of the datapoint)
        self.key_to_index = {}  # dict (key: key of the datapoint, value: index)

    def add(self, key, value):
        """ 
        Add a new (key, value) pair.
        Input:
            key: key of the datapoint
            value: value of the datapoint.
        """
        self.array[self.heap_size + 1] = value
        self.heap_size += 1
        self.index_to_key[self.heap_size] = key
        self.key_to_index[key] = self.heap_size
        self.bubble_up(self.heap_size)
        if self.heap_size + 1 == len(self.array):
            self.array = np.resize(self.array, len(self.array) * 2)

    def remove(self, key):
        """
        Remove information about (key, value) pair based on key
        Input:
            key: key of the datapoint.
        """
        if key not in self.key_to_index:
            return
        index = self.key_to_index[key]
        self.swap(self.heap_size, index) # Swap to the last spot.
        del self.key_to_index[self.index_to_key[self.heap_size]]
        del self.index_to_key[self.heap_size]
        self.heap_size -= 1
        self.bubble_down(index)
        if self.heap_size <= len(self.array) and self.heap_size > 3:
            self.array = np.resize(self.arrya, len(self.array)/2)

    def update(self, key, value):
        """
        Update the value of the given key with the given value
        Input:
            key: key of the dataporint
            value: value of the datapoint
        """
        if key not in self.key_to_index:
            return
        index = self.key_to_index[key]
        self.array[index] = value
        if value < self.array[self.parent(index)]:
            self.bubble_up(index)
        else:
            self.bubble_down(index)


    def value(self, key):
        """
        Return the value associated the given key
        Input:
            key: key of the datapoint
        """
        if key in self.key_to_index:
            return self.array[self.key_to_index[key]]
        else:
            return None

    def peek_min(self):
        """
        Peek the minimum value.
        """
        if self.heapsize == 0:
            return -1   # No value to return
        else:
            return self.array[1]


    def pop_min(self):
        """
        Get the minimum value and its associated key, and remove the datapoint.
        """
        if self.heap_size == 0:
            return None
        minimum = self.array[1]
        self.swap(self.heap_size, 1)
        del self.key_to_index[self.index_to_key[self.heap_size]]
        key = self.index_to_key[self.heap_size]
        del self.index_to_key[self.heap_size]
        self.heap_size -= 1
        self.bubble_down(1)
        if self.heap_size <= len(self.array)/4 and self.heap_size > 3:
            self.array = np.resize(self.array, len(self.array)/2)
        return key, minimum


    def swap(self, index1, index2):
        """
        Swapping two (key, value) pairs.
        Input:
            index1 (int): index of self.array for the first pair
            index2 (int): index of self.array for the second pair
        """
        # swapping values
        temp = self.array[index1]
        self.array[index1] = self.array[index2]
        self.array[index2] = temp
        # swapping keys
        key1 = self.index_to_key[index1]
        self.index_to_key[index1] = self.index_to_key[index2]
        self.index_to_key[index2] = key1
        self.key_to_index[key1] = index2
        self.key_to_index[key2] = index1

    def bubble_up(self, index):
        """
        If the value of the datapoint is not valid, goes up until valid.
        Input:
            index (int): index of the datapoint
        """
        while self.parent(index) >= 1 and \
                self.array[self.parent[index]] > self.array[index]:
            self.swap(index, self.parent(index)
            index = self.parent(index)


    def bubble_down(self, index):
        """
        If the value of the datapoint is not valid, goes down until valid.
        Input:
            index (int): index of the datapoint
        """
        while self.left(index) <= self.heap_size:
            temp = self.left(index)
            if temp < self.heap_size and \
                self.array[temp] > self.array[self.right(index)]:
                temp += 1
            if self.array[temp] > self.array[index]:
                break
            self.swap(index, temp)
            index = temp


    def parent(self, index):
        """
        Get the parent index for the given (key, value) pair.
        Input:
            index (int): index of self.array for the given (key, value) pair
        """
            return index / 2

    def left(self, index):
        """
        Get the left-child index for the given (key, value) pair.
        Input:
            index (int): index of self.array for the given (key, value) pair
        """
            return index * 2

    def right(self, index):
        """
        Get the right-child index for the given (key, value) pair.
        Input:
            index (int): index of self.array for the given (key, value) pair
        """
            return index * 2 + 1

    def write(self):
        """
        Write the stored data to that standard output.
        """
        for i in range(1, self.heap_size + 1):
            print i, self.array[i], self.index_to_key[i]

def main():
    a='a'
    b='b'
    c='c'
    d='d'

    t={(a,b): 1, (c,d):2}
    print t

if __name__ == "__main__":
    main()
