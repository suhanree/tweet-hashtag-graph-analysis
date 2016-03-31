# Class for the indexed priority queue. It uses the binary heap structure and a
# directory to keep the index information for given key value. Each datapoint
# will be (key, value), and the priority will be determined by the value.
class indexedMinPQ:
    def __init__(self):
        pass

    def add(self, key, value):
        return True

    def remove(self, key):
        return True

    def update(self, key, value):
        return True

    def value(self, key):
        return 1

    def peek_min(self):
        return 1

    def pop_min(self):
        return 1

def main():
    a='a'
    b='b'
    c='c'
    d='d'

    t={(a,b): 1, (c,d):2}
    print t

if __name__ == "__main__":
    main()
