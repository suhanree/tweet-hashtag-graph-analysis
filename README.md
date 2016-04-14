# Tweet Hashtag Graph Analyzer

This is a part of a coding challenge. In this challenge, we generate average
degrees of hashtag graph for the last 60 seconds every time a new tweet
appears. A hashtag graph can be constructed by adding a link whenever a
pair of hashtags appears together in a tweet, and we only keep links for tweets
in the last 60 seconds.

The algorithms we need for this problem can be borrowed from Dijkstra's
shortest-path algorithm, because we need to find the oldest link(s) 
and remove them if necessary,
whenever the 60-second time window changes by updating the current time.
When we implement Dijkstra's algorithm,
we have to find the node with the shortest distance from a group of nodes.
To get the `log N` time for these lookups, the indexed minimum priority queue using 
the heap data structure is used. In the indexed priority queue, `(key, value)` pairs
are stored where the minimum `value` is kept and `key` can be used to update
the associated `value`.
In this problem, `key` is the link (represented by two hashtags), 
and `value` is the timestamp of the given link. 

Now we have to determine how to represent the graph. Since the graph
structure we are
dealing with here changes constantly, I decided to use the dictionary of sets
(implemented using hash maps and hash sets) instead of using existing graph
libraries.
Each node becomes a `key` of the dictionary, and a set of nodes representing 
links from the given node is the associated `value`.
Then we can add, look up, and remove nodes and links in `O(1)` time (if we only
consider the graph structure, since the priority queue is used additionally to 
store time information for links, adding/removing links will take `O(logN)`
time where `N` is the number of links).

## Tools
Python 2.7 is used for this problem, and imported libraries are `sys`, `time`,
`json` and `numpy`.

## Classes
I implemented two classes: `TimeWindowGraph` and `indexedMinPQ`.

### TimeWindowGraph class
This class represents graphs that have links with time information, it has
the window size (default: 60) and the current time should be kept
to maintain the moving window and nodes and links in the window.

1. Time is represented by a non-negative integer (e,g,, epoch time),
and the window size can be set (default: 60).
2. It has to keep the current time to maintain the window.
3. Given the current time, it only keeps links within the given time
window.
4. Links are undirected
5. Self-loops (same node as endpoints) and multiple links (more than one
links connecting the same pair of nodes) are not allowed.
6. Nodes are named uniquely (e.g., integer, string), and it is assumed that
they are immutable and operator < can be used with them.

Public methods for this class are:

`check_node(node)`: check if a node exists in the graph.

`add_node(node)`: add a node.

`remove_node(node)`: remove a node and its associated links if exist.

`check_link(node1, node2)`: check if a link exists between node1 and node2.

`add_link(node1, node2, time=0)`: add a link when there is no link
between node1 and node2.

`update_link(node1, node2, time=0)`: update a given link with new time value.

`remove_link(node1, node2)`: remove a given link.

`remove_min_link()`: remove a link with the minimum value 
(if there are more than one with
the same minimum value, one is chosen without any order).

`average_degree()`: returns the average degree of the graph, and computed by 
`2 * (number of links) / (number of nodes)`.

`set_current_time(time)`: set the current time if time is non negative (old
links will be removed here if necessary).

### indexedMinPQ class
This class represents the indexed priority queue, and it will be used by
`TimeWindowGraph` class.

1. It uses the binary heap structure (represented by a numpy array).
2. Two dictionaries to keep the relations between indices and keys value are
used additionally. 
3. Each datapoint will be (key, value) pair, and the priority will be 
determined by the value.

Public methods for this class are:

`add(key, value)`: add a new (key, value) pair. Do nothing, if key exists already.

`remove(key)`: remove information about (key, value) pair based on key.

`update(key, value)`: update the value of the given key with the given value.

`value(key)`: return the value associated the given key.

`peek_min()`: peek the minimum value and return (key, value) pair.

`pop_min()`: get the minimum value and its associated key, and remove the datapoint.

`size()`: returns the size of the priority queue.


## Error handlings

1. Missing fields: To find the time information for a tweet in json format, 
    `created_at` field is used, and to find hashtags, `entities` field is used.
    If those fields don't exist somehow, timestamp is set to 0, and
    no hashtag is assumed.

2. Control data: There are some control data in the stream of tweets. To skip
   those, the number of fields are checked, and if that is less than a certain
   number, that data point will be ignored.

3. Duplicate hashtags: If there are duplicate hashtags in a tweet, a link
   betweeen the same node (self-loop) will not be added.

4. Multiple links: Only one link can exist between two nodes, but the time
   information for that link will be updated if the time is more recent.

## Complexities
Time and space complexities are briefly discussed here.

Adding/removing/looking up a node: `O(1)`

Adding/removing/looking up a link: `O(logN)` where `N` is the number of links.

Getting the information of the oldest link: `O(1)`

Removing the oldest link: `O(logN)` where `N` is the number of links.

Computing the average degree: `O(1)` because it is simply 
`2 * (number of links) / (number of nodes)`, and getting 
the numbers of nodes and links are `O(1)`.

Space-wise it has some redundancies when storing node and link information.
Nodes are directly represented by hashtag strings (in unicode) and links are 
represented by a tuple of two hashtag strings. If we assume the average 
size of a hashtag is `H` (byte), and the numbers of nodes and links are `V` and
`E` respectively, the graph structure uses at least `H(V + 2E)` (bytes)
for the dictionary of sets, and
the priority queue uses at least `2E(2H + 4) + 4E` (bytes), where the size
of an integer is assumed to be 4 (byte), 
`2E(2H + 4)` is for two dictionaries that stores relations
between indices and links, and `4E` is for an array of time information for all
links, representing the binary heap structure.
Here `2EH` is the size of the memory we need to store a list of all links, and
it appears three times overall, once for the graph structure, and twice for the
priority queue. These can be easily reduced by combining two classes, if the
memory is limited.

## Final remarks
I have past experience on building graph classes, and I have
implemented indexed priority queues before, even though they were all
written in C++.
Hence, for the classes I implemented in this problem, I mostly rewrote C++ codes 
into python codes. Then I had to write functions for reading the text file
with tweet streams, and for extracting information about the time and hashtags
out of a tweet in json format. It is straightforward afterward, if we use methods
from the graph class.

