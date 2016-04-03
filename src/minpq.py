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
        self._array = np.zeros(2, dtype=dtype)  
                    # numpy array to store values for heap structure
                    # (initially two elements are needed)
        self._heap_size = 0 # Number of data points stored.
        self._index_to_key = {}  # dict (key: index, value: key of the datapoint)
                                # where 'index' is the index of self._array.
        self._key_to_index = {}  # dict (key: key of the datapoint, value: index)

    def add(self, key, value):
        """ 
        Add a new (key, value) pair. Do nothing, if key exists already.
        Input:
            key: key of the datapoint
            value: value of the datapoint.
        Output:
            (bool): True if successful, False if not
        """
        # Do nothing, if key already exists.
        if key in self._key_to_index:
            return False
        # Put the new value at the end of the heap.
        self._array[self._heap_size + 1] = value
        self._heap_size += 1
        # Update dicts.
        self._index_to_key[self._heap_size] = key
        self._key_to_index[key] = self._heap_size
        # Heapify (it has to go up)
        self._bubble_up(self._heap_size)
        # Resize self._array to double the size if heap_size reaches 
        # the size of self._array.
        if self._heap_size + 1 == len(self._array):
            self._array = np.resize(self._array, len(self._array) * 2)
        return True


    def remove(self, key):
        """
        Remove information about (key, value) pair based on key
        Input:
            key: key of the datapoint.
        Output:
            (bool): True if successful, False if not
        """
        # Do nothing, if key does not exist.
        if key not in self._key_to_index:
            return False
        # Find the index for the key.
        index = self._key_to_index[key]
        # Then swap this value with the last value in the heap.
        self._swap(self._heap_size, index)
        # Update dicts.
        del self._key_to_index[self._index_to_key[self._heap_size]]
        del self._index_to_key[self._heap_size]
        self._heap_size -= 1
        # Heapify.
        self._bubble_down(index)
        # Resize self._array to half the size if heap_size reaches
        # a quarter of self._array (Note: it is a quarter, not a half.)
        if self._heap_size <= len(self._array) / 4 and self._heap_size > 3:
            self._array = np.resize(self._array, len(self._array)/2)
        return True


    def update(self, key, value):
        """
        Update the value of the given key with the given value
        Input:
            key: key of the dataporint
            value: value of the datapoint
        Output:
            (bool): True if successful, False if not
        """
        # Do nothing, if key does not exist.
        if key not in self._key_to_index:
            return False
        # Update the value in self._array.
        index = self._key_to_index[key]
        self._array[index] = value
        # Heapify based on the new value.
        if value < self._array[self._parent(index)]:
            self._bubble_up(index)
        else:
            self._bubble_down(index)
        return True


    def value(self, key):
        """
        Return the value associated the given key
        Input:
            key: key of the datapoint
        """
        if key in self._key_to_index:
            return self._array[self._key_to_index[key]]
        else:
            return None # If key doesn't exist.


    def peek_min(self):
        """
        Peek the minimum value and return (key, value) pair.
        """
        if self._heap_size == 0:
            return None, None   # No value to return
        else:
            # Value at the root of heap (minimum).
            return self._index_to_key[1], self._array[1]   


    def pop_min(self):
        """
        Get the minimum value and its associated key, and remove the datapoint.
        """
        if self._heap_size == 0:
            return None, None   # No value to return
        # (key, value) pair to return.
        key = self._index_to_key[1]
        value = self._array[1]
        # Remove (key, value) pair.
        self.remove(key)
        return key, value


    def size(self):
        """
        Returns the size of the priority queue
        Output:
            size (int): number of (key, value) pairs.
        """
        return self._heap_size


    def write(self):
        """
        Write the stored data to that standard output.
        """
        for i in range(1, self._heap_size + 1):
            print i, self._array[i], self._index_to_key[i]

    # ==== private methods from here on =====================
    def _swap(self, index1, index2):
        """
        Swapping two (key, value) pairs.
        Input:
            index1 (int): index of self._array for the first pair
            index2 (int): index of self._array for the second pair
        """
        # swapping values
        temp = self._array[index1]
        self._array[index1] = self._array[index2]
        self._array[index2] = temp
        # swapping keys
        key1 = self._index_to_key[index1]
        key2 = self._index_to_key[index2]
        self._index_to_key[index1] = key2
        self._index_to_key[index2] = key1
        self._key_to_index[key1] = index2
        self._key_to_index[key2] = index1

    def _bubble_up(self, index):
        """
        If the value of the datapoint is not valid, goes up until valid.
        Input:
            index (int): index of the datapoint
        """
        while self._parent(index) >= 1 and \
                self._array[self._parent(index)] > self._array[index]:
            self._swap(index, self._parent(index))
            index = self._parent(index)


    def _bubble_down(self, index):
        """
        If the value of the datapoint is not valid, goes down until valid.
        Input:
            index (int): index of the datapoint
        """
        while self._left(index) <= self._heap_size:
            temp = self._left(index)
            if temp < self._heap_size and \
                self._array[temp] > self._array[self._right(index)]:
                temp += 1
            if self._array[temp] > self._array[index]:
                break
            self._swap(index, temp)
            index = temp


    def _parent(self, index):
        """
        Get the parent index for the given (key, value) pair.
        Input:
            index (int): index of self._array for the given (key, value) pair
        """
        return index / 2

    def _left(self, index):
        """
        Get the left-child index for the given (key, value) pair.
        Input:
            index (int): index of self._array for the given (key, value) pair
        """
        return index * 2

    def _right(self, index):
        """
        Get the right-child index for the given (key, value) pair.
        Input:
            index (int): index of self._array for the given (key, value) pair
        """
        return index * 2 + 1

def main():
    pq = indexedMinPQ(dtype='int')
    pq.add('a', 5)
    pq.write()
    pq.add('b', 4)
    pq.write()
    pq.add('c', 3)
    pq.write()
    pq.add('d', 2)
    pq.write()
    pq.add('e', 1)
    pq.write()
    print pq.value('a')
    print pq.value('b')
    print pq.value('c')
    print pq.value('d')
    print pq.value('e')
    pq.remove('b')
    pq.write()
    pq.remove('a')
    pq.write()
    pq.remove('c')
    pq.write()
    pq.remove('e')
    pq.write()
    print pq.pop_min()
    pq.write()
    print pq.pop_min()
    pq.write()
    pq.remove('b')
    pq.write()

if __name__ == "__main__":
    main()
