# Class that represents graphs (undirected, with no self-loop, with no multiple
# links). Each link will have time value associated with it, and we have to keep
# only the latest links based on time. We only keep links for the last 60
# seconds, which means we have to keep the current time, and links should be
# also stored in some type of priority queue structures. Basic graph structure
# will be stored as a dictionary of dictionaries.

from minpq import indexedMinPQ

class TimeWindowGraph:
    """
    TimeWindowGraph class
    This class represents graphs that have links with time information.
    (1) Time is represented by a non-negative integer (e,g,, epoch time),
        and the window size can be set (default: 60).
    (2) It has to keep the current time to maintain the window.
    (3) Given the current time, it only keeps links within the given time
        window.
    (4) Links are undirected
    (5) Self-loops (same node as endpoints) and multiple links (more than one
        links connecting the same pair of nodes) are not allowed.
    (6) Nodes are named uniquely (e.g., integer, string), and it is assumed that
        they are immutable and operator < can be used with them.
    """
    def __init__(self, window_size=60):
        """
        Constructor
        Input:
            window_size (int): size of the window (default: 60)
        """
        # Attributes of this class
        self.window_size = window_size   # size of the window
        self.num_links = 0  # Total number of links.
        self.num_nodes = 0  # Total number of nodes.
        self.current_time = 0   # Current time in int.
        self._graph_structure = {}   # dict to represent graph structure
                                    # (key: node, value: set of nodes).
        self._linkheap = indexedMinPQ(dtype='int')  
                                    # Indexed minimum priority queue to
                                    # remove old links efficiently
                                    # (log(N) time where N: number of links)
                                    # (key: (node1, node2), value: time)

    def check_node(self, node):
        """
        Check if a node exists in the graph
        Input:
            node: ID of a node
        Output:
            (bool): True if exists, False if not
        """
        if node in self._graph_structure:
            return True
        else:
            return False

    def add_node(self, node):
        """
        Add a node
        Input:
            node: ID of a node
        Output:
            (bool): True if successful, False if not
        """
        if node not in self._graph_structure:
            self._graph_structure[node] = set()
            self.num_nodes += 1
            return True
        else:
            return False

    def remove_node(self, node):
        """
        Remove a node and its associated links if exist.
        Input:
            node: ID of a node
        Output:
            (bool): True if successful, False if not
        """
        if node in self._graph_structure:
            links_info = self._graph_structure[node].copy()
            if len(links_info) > 0: # If there are links associated with node,
                                    # we have to remove them first.
                for node2 in links_info:
                    self.remove_link(node, node2)
            del self._graph_structure[node]
            self.num_nodes -= 1
            return True
        else:
            return False

    def check_link(self, node1, node2):
        """
        Check if a link exists between node1 and node2.
        Input:
            node1: ID of a node
            node2: ID of a node
        Output:
            time (int): -1 if none exists, time value if already exists.
        """
        if not self.check_node(node1) or not self.check_node(node2) \
            or node1 == node2:
            return -1
        else:
            if node1 in self._graph_structure and \
                node2 in self._graph_structure[node1]:
                node_pair = (node1, node2) if node1 < node2 else (node2, node1)
                return self._linkheap.value(node_pair)
            else:
                return -1

    def add_link(self, node1, node2, time=0):
        """
        Add a link when there is no link between node1 and node2.
        Input:
            node1: ID of a node
            node2: ID of a node
            time (int): time value of the link (non-negative)(default: 0)
        Output:
            (bool): True if successful, False if not.
        """
        if not self.check_node(node1) or not self.check_node(node2) or \
            node1 == node2 or self.check_link(node1, node2) >= 0:
            return False
        else:
            node_pair = (node1, node2) if node1 < node2 else (node2, node1)
            self._linkheap.add(node_pair, time)
            self._graph_structure[node1].add(node2)
            self._graph_structure[node2].add(node1)
            self.num_links += 1
            # If the time is greater than the current time, update it
            if time > self.current_time:
                self.set_current_time(time)
            return True

    def update_link(self, node1, node2, time=0):
        """
        Update a given link with new time value
        Input:
            node1: ID of a node
            node2: ID of a node
            time (int): time value of the link (non-negative)(default: 0)
        Output:
            (bool): True if successful, False if not.
        """
        if self.check_link(node1, node2) < 0:
            return False
        else:
            node_pair = (node1, node2) if node1 < node2 else (node2, node1)
            if self._linkheap.update(node_pair, time):
                # If the time is greater than the current time, update it
                if time > self.current_time:
                    self.set_current_time(time)
                return True
            else:
                return False


    def remove_link(self, node1, node2):
        """
        Remove a given link
        Input:
            node1: ID of a node
            node2: ID of a node
        Output:
            (bool): True if successful, False if not.
        """
        if self.check_link(node1, node2) < 0:
            return False
        else:
            node_pair = (node1, node2) if node1 < node2 else (node2, node1)
            if self._linkheap.remove(node_pair):
                self._graph_structure[node1].remove(node2)
                self._graph_structure[node2].remove(node1)
                self.num_links -= 1
                return True
            else:
                return False


    def remove_min_link(self):
        """
        Remove a link with the minimum value (if there are more than one with
        the same minimum value, one is chosen without any order).
        Output:
            node_pair: (origin, destination) for the minimum link
            time (int): minimum value
        """
        if self.num_links == 0:
            return None, None
        else:
            (node1, node2), time = self._linkheap.pop_min()
            if time is not None:
                self._graph_structure[node1].remove(node2)
                self._graph_structure[node2].remove(node1)
                self.num_links -= 1
            return (node1, node2), time


    def write(self):
        """
        Print graph information to the standard output
        """
        print "Nodes (total:", self.num_nodes, "):"
        print self._graph_structure.keys()
        print "Links (total:", self.num_links, "):"
        for node1 in self._graph_structure:
            for node2 in self._graph_structure[node1]:
                if node1 < node2:
                    print repr(node1), "->", repr(node2), ":", \
                        self._linkheap.value((node1,node2))
        print "average degree: %.2f" % self.average_degree()


    def average_degree(self):
        if self.num_nodes == 0:
            return 0
        else:
            return 2 * self.num_links/float(self.num_nodes)


    def set_current_time(self, time):
        """
        Set the current time if time is non negative.
        """
        if time >= 0:
            self.current_time = int(time)
            if self.num_links >  0:
                self._remove_old_links()


    def _remove_old_links(self):
        """
        Remove old links if the current time advances and some links are
        out of the window. If a node has no link (degree 0) as a result
        of this operatoin, remove that node, too.
        This method will be called from 'self.set_current_time'.
        """
        # If there is no link, no need.
        if self.num_links == 0:
            return
        threshold = self.current_time - self.window_size
        (node1, node2), time  = self._linkheap.peek_min()
        while time <= threshold: # threshold (=current_time - window_size)
                                 # is not included in the window.
            (node1, node2), time  = self.remove_min_link()
            if len(self._graph_structure[node1]) == 0:
                self.remove_node(node1)
            if len(self._graph_structure[node2]) == 0:
                self.remove_node(node2)
            if self.num_links == 0:
                break
            (node1, node2), time  = self._linkheap.peek_min()
        return


def main():
    """
    Testing the class
    """
    gr = TimeWindowGraph(window_size=5)
    gr.write()
    print gr.add_node("a")
    print gr.add_node("b")
    gr.write()
    print gr.add_node("a")
    gr.write()
    print gr.add_node("c")
    gr.write()
    print gr.add_link("a", "b", 2)
    print gr.add_link("a", "c", 4)
    print gr.add_link("b", "c", 8)
    gr.write()
    print gr.update_link("b", "c", 8)
    gr.write()
    print gr.update_link("b", "c", 9)
    gr.write()
    #print gr.remove_node("a")
    #gr.write()

if __name__ == "__main__":
    main()
