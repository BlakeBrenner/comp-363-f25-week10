def khan(graph: list[list[int]]) -> list[int]:

    """Comprehensive implementation of Kahn's algorithm for topological sorting."""

    # Data integrity check - a bit much but I was having fun with it.
    if (
         graph is None
        or not isinstance(graph, list)
        or len(graph) == 0
        or not all(isinstance(row, list) for row in graph)
        or not all(len(row) == len(graph) for row in graph)
    ):
        raise ValueError("Input must be a non-empty square adjacency matrix.")

    # Ease of reference
    N = len(graph)
    NO_EDGE = graph[0][0]

    # Calculate in-degrees of all vertices.
    in_degrees = [0] * N
    for u in range(N):
        for v in range(N):
            if graph[u][v] != NO_EDGE:
                # In edge u --> v we compute the in-degree of v
                in_degrees[v] += 1

    # Initialize list of source vertices
    sources = []
    for i in range(N):
        if in_degrees[i] == 0:
            sources.append(i)

    # List to store the topological order
    topological_order = []

    # Progressively remove sources and update in-degrees
    while len(sources) > 0:
        # Remove a source vertex
        vertex = sources.pop(0)
        # Add it to the topological order
        topological_order.append(vertex)
        # Decrease in-degrees of its neighbors
        for neighbor in range(N):
            if graph[vertex][neighbor] != NO_EDGE:
                in_degrees[neighbor] -= 1
                # If in-degree becomes zero, add it to sources
                if in_degrees[neighbor] == 0:
                    sources.append(neighbor)

    # Done
    return topological_order

def DFS(G, v, marked):
    # Mark the current vertex as visited
    marked.append(v)
    # Consider all the neighbors of v
    for w in range(len(G)):
        # For any edg v --> w, if w is unmarked,
        # plan to visit it.
        if G[v][w] != G[0][0] and w not in marked:
            # Plan to visit w
            DFS(G, w, marked)
    return marked

def DFS_helper(G, v):
    """Helper method to launch a DFS from vertex v."""
    # Launch DFS from v with empty marked list
    return DFS(G, v, [])

def topo_stack_duration(graph: list[list[int]]) -> list[int]:
    """
    Topological sort using recursive DFS and how long each vertex
    stays on the recursion stack (exit_time - enter_time).
    """

    # Same data integrity check as in khan()
    if (
         graph is None
        or not isinstance(graph, list)
        or len(graph) == 0
        or not all(isinstance(row, list) for row in graph)
        or not all(len(row) == len(graph) for row in graph)
    ):
        raise ValueError("Input must be a non-empty square adjacency matrix.")

    # Ease of reference
    N = len(graph)
    NO_EDGE = graph[0][0]

    # DFS bookkeeping
    visited     = [False] * N
    enter_time  = [0] * N
    exit_time   = [0] * N
    time        = 0  # logical clock

    # Recursive DFS that tracks how long a vertex stays "on the stack"
    def dfs(v: int):
        nonlocal time

        visited[v] = True
        time += 1
        enter_time[v] = time  # v is "pushed" on recursion stack

        # Explore all neighbors
        for u in range(N):
            if graph[v][u] != NO_EDGE and not visited[u]:
                dfs(u)

        time += 1
        exit_time[v] = time  # v is about to be "popped" from recursion stack

    # Run DFS from every unvisited vertex (in case the DAG is not connected)
    for v in range(N):
        if not visited[v]:
            dfs(v)

    # Compute how long each vertex stayed on the recursion stack
    durations = [exit_time[v] - enter_time[v] for v in range(N)]

    # Sort vertices by decreasing duration
    topo_order = sorted(range(N), key=lambda v: durations[v], reverse=True)

    return topo_order

G1 = [
    [0, 1, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 1, 1],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0],
]

G2 = [
    [0,0,1,0,1,1],
    [0,0,1,0,0,0],
    [0,0,0,0,1,1],
    [0,1,2,0,0,1],
    [0,0,0,0,0,1],
    [0,0,0,0,0,0]
]

def print_results(G, name):
    print_results(G1, "G1")
    print_results(G2, "G2")