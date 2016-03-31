# Class that represents graphs (undirected, with no self-loop, with no multiple
# links). Each link will have timestamp associated with it, and we have to keep
# only the latest links based on time. We only keep links for the last 60
# seconds, which means we have to keep the current time, and links should be
# also stored in some type of priority queue structures. Basic graph structure
# will be stored as a dictionary of dictionaries.

from minpq import indexedMinPQ

class HashtagGraph:
    """
    HashtagGraph class
    """
    def __init__(self):
        self.num_links = 0
        self.num_nodes = 0
        self.current_time = 0
        self.graph_structure = {}
        self.nodemap = {}
        self.linkheap = indexedMinPQ()

    def check_link(self, node1, node2):
        return 0

    def add_link(self, node1, node2, timestamp):
        pass

    def update_link(self, node1, node2, timestamp):
        pass

    def remove_old_links(self, timestamp):
        pass

    def add_nodes(self, node1, node2):
        pass

    def average_degree(self):
        if self.num_nodes == 0:
            return 0
        else:
            return 2 * self.num_links/float(self.num_nodes)

    def get_current_time(self):
        return self.current_time

    def set_current_time(self, timestamp):
        self.current_time = timestamp

    def remove_link(self, node1, node2):
        pass

def main():
    pass

if __name__ == "__main__":
    main()
