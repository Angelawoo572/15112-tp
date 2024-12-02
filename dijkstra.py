### citation (notes): not copying codes, just learning from the website: 
# https://medium.com/basecs/finding-the-shortest-path-with-a-little-help-from-dijkstra-613149fbdc8e

def initialize_single_source(graph,start):
    # the distance initially to all nodes unknown -- infinity
    distances = {vertex: float('inf') for vertex in graph} 
    # predescessors are None
    predecessors = {vertex: None for vertex in graph}
    # Set the distance to the start node as 0, the starting point.
    distances[start] = 0
    return distances, predecessors

def relax(u, v, weight, distances, predecessors, q):
    # update the distance to a neighbor node if a shorter path is found
    if distances[v] > distances[u] + weight: # u current node, v neighbor node
        distances[v] = distances[u] + weight
        predecessors[v] = u
        # Add the updated node back to the q for further exploration.
        q.append((distances[v], v))

def dijkstra(graph,start):
    # initialize
    distances, predecessors = initialize_single_source(graph, start)
    q = [(0,start)] #(distance,node) a list of tuples
    visited = set()

    while q:
        # Sort the q to get the node with the smallest distance.
        # citation: learned how to use key = lambda x: from https://docs.python.org/3/howto/sorting.html
        # also can write :
        # def get_first_element(x):
        #     return x[0]
        # q.sort(key=get_first_element)
        q.sort(key=lambda x: x[0])
        current_distance, u = q.pop(0)
        
        # If the node has already been visited, skip it.
        if u in visited:
            continue
        visited.add(u)
        
        # Iterate over all adjacent nodes and relax the edges.
        for v, weight in graph[u].items(): # already cited in huffman_tree_game: 
            # I learned from https://www.w3schools.com/python/ref_dictionary_items.asp
            if v not in visited:
                relax(u, v, weight, distances, predecessors, q)
                
    return distances, predecessors

def find_shortest_path(predecessors, target):
    # Backtrack from the target node to find the shortest path.
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = predecessors[current]
    # Reverse the path to get the correct order from start to target.
    path.reverse()
    return path

# code
# def hint_node_to_node(graph, start, end):
#     """Provides the shortest path between two nodes."""
#     d, preds = dijkstra(graph, start)
#     path = find_shortest_path(preds, end)
#     return path

# def hint_whole_graph(graph, start_node, end_node):
#     """Provides the shortest path from start to the end node."""
#     distances, predecessors = dijkstra(graph, start_node)
#     return find_shortest_path(predecessors, end_node)