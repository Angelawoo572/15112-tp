### citation (notes): not copying codes, just learning from the website: https://www.interviewcake.com/concept/java/bfs
def bfs(Adj,s):
    # initializing levels and parents
    level = {s:0} # level 0 starts with source node 's'
    parent = {s:None}

    i = 1
    frontier = [s] # Nodes to explore in the curr level
    
    while frontier:
        next_frontier = [] # nodes to explore in the next level
        for u in frontier:
            for v in Adj[u]:
                if v not in level: # not yet seen
                    level[v] = i # assign level i
                    parent[v] = u # track the parent v
                    next_frontier.append(v) # add node to next frontier
        frontier = next_frontier # move to next level
        i += 1 # increment level
    
    return level, parent

def find_shortest_path(parent, s, t):
    # If the target node t is not reachable
    if t not in parent:
        return None
    
    path = []
    current = t
    while current is not None:
        path.append(current)
        current = parent[current]
    
    path.reverse()
    return path