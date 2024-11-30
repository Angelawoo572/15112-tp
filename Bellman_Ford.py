# do not need priority queue
# it need repeated relaxation
def initialize_single_source(V,s):
    # the distance initially to all nodes unknown -- infinity
    distances = {vertex: float('inf') for vertex in V} 
    # predescessors are None
    predecessors = {vertex: None for vertex in V}
    # Set the distance to the start node as 0, the starting point.
    distances[s] = 0
    return distances, predecessors

# relax do not need priority queue
def relax(u, v, w, distance, predecessor):
    if distance[u] != float('inf') and distance[v] > distance[u] + w:
        distance[v] = distance[u] + w
        predecessor[v] = u
    # update the shortest path from a source to very other vertex
    # i = 1 to |Vertices| -1 iterates all edges

def bellman_ford(V,edges,s):
    distance, predecessor = initialize_single_source(V, s)

    for _ in range(len(V) - 1): # vertices - 1; V is a list
        for u, v, w in edges:
            relax(u, v, w, distance, predecessor)

    # Check for negative-weight cycles
    for u, v, w in edges:
        if distance[u] != float('inf') and distance[v] > distance[u] + w:
            print("Graph contains a negative-weight cycle")
            return None, None

    return distance, predecessor

def find_shortest_path(V, edges, start, end):
    distance, predecessor = bellman_ford(V, edges, start)
    if distance is None:
        return None, float('inf')

    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = predecessor[current]
    if path[0] == start:
        return path, distance[end]
    else:
        return None, float('inf')
    
def find_all_shortest_paths(V, edges, src):
    distance, p = bellman_ford(V, edges, src)
    if distance is None:
        return None
    return distance