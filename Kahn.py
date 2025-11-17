def khan(graph):
    """Kahn's algorithm for topological sorting using an adjacency matrix."""

    # Data integrity check
    if (
         graph is None
        or not isinstance(graph, list)
        or len(graph) == 0
        or not all(isinstance(row, list) for row in graph)
        or not all(len(row) == len(graph) for row in graph)
    ):
        raise ValueError("Input must be a non-empty square adjacency matrix.")

    N = len(graph)
    NO_EDGE = graph[0][0]

    # Compute in-degrees
    in_degrees = [0] * N
    for u in range(N):
        for v in range(N):
            if graph[u][v] != NO_EDGE:
                in_degrees[v] += 1

    # Collect initial sources
    sources = []
    for i in range(N):
        if in_degrees[i] == 0:
            sources.append(i)

    topological_order = []

    # Repeatedly remove sources
    while len(sources) > 0:
        v = sources.pop(0)
        topological_order.append(v)

        # Reduce neighbors' in-degrees
        for w in range(N):
            if graph[v][w] != NO_EDGE:
                in_degrees[w] -= 1
                if in_degrees[w] == 0:
                    sources.append(w)

    return topological_order


def DFS(G, v, marked):
    """Simple recursive DFS from the notes."""
    marked.append(v)
    for w in range(len(G)):
        if G[v][w] != G[0][0] and w not in marked:
            DFS(G, w, marked)
    return marked


def DFS_helper(G, v):
    """DFS helper wrapper."""
    return DFS(G, v, [])


def topo_stack_duration(graph):
    """
    Topological sort using DFS and stack time duration method with an adjacency matrix.

    record, for each vertex v, the time when v finishes (its exit time)
    — that is, the moment it is popped from the recursion stack.
    In a DAG, for every edge u -> v we have exit_time[u] > exit_time[v],
    so sorting vertices by decreasing exit time yields a topological order
    """

    # Data integrity check
    if (
         graph is None
        or not isinstance(graph, list)
        or len(graph) == 0
        or not all(isinstance(row, list) for row in graph)
        or not all(len(row) == len(graph) for row in graph)
    ):
        raise ValueError("Input must be a non-empty square adjacency matrix.")

    N = len(graph)
    NO_EDGE = graph[0][0]

    visited   = [False] * N
    exit_time = [0] * N
    time      = 0

    def dfs(v):
        nonlocal time
        visited[v] = True
        for u in range(N):
            if graph[v][u] != NO_EDGE and not visited[u]:
                dfs(u)
        time += 1
        exit_time[v] = time

    for v in range(N):
        if not visited[v]:
            dfs(v)

    # Sort by decreasing exit time
    order = sorted(range(N), key=lambda v: exit_time[v], reverse=True)
    return order


def is_valid_topo(graph, order):
    """Check whether 'order' is a valid topological sort for adjacency matrix graph."""
    pos = {}
    for i in range(len(order)):
        pos[order[i]] = i

    N = len(graph)
    NO_EDGE = graph[0][0]

    for u in range(N):
        for v in range(N):
            if graph[u][v] != NO_EDGE:
                # Must have pos[u] < pos[v]
                if pos[u] >= pos[v]:
                    return False
    return True


def print_results(graph, name):
    """Run both algorithms and print results."""
    k = khan(graph)
    d = topo_stack_duration(graph)

    print("Graph:", name)
    print("  Kahn order          :", k, " valid:", is_valid_topo(graph, k))
    print("  Stack-duration order:", d, " valid:", is_valid_topo(graph, d))
    print()


# Example DAGs
G1 = [
    [0, 1, 1, 0, 0, 0],  # 0 -> 1,2
    [0, 0, 0, 1, 1, 0],  # 1 -> 3,4
    [0, 0, 0, 0, 1, 1],  # 2 -> 4,5
    [0, 0, 0, 0, 0, 1],  # 3 -> 5
    [0, 0, 0, 0, 0, 1],  # 4 -> 5
    [0, 0, 0, 0, 0, 0],  # 5
]

G2 = [
    [0, 0, 1, 0, 1, 1],  # 0 -> 2,4,5
    [0, 0, 1, 0, 0, 0],  # 1 -> 2
    [0, 0, 0, 0, 1, 1],  # 2 -> 4,5
    [0, 1, 2, 0, 0, 1],  # 3 -> 1,2,5
    [0, 0, 0, 0, 0, 1],  # 4 -> 5
    [0, 0, 0, 0, 0, 0],  # 5
]

#test case with a single linear path
G3 = [
    [0, 1, 0, 0, 0, 0],  # 0 -> 1
    [0, 0, 1, 0, 0, 0],  # 1 -> 2
    [0, 0, 0, 1, 0, 0],  # 2 -> 3
    [0, 0, 0, 0, 1, 0],  # 3 -> 4
    [0, 0, 0, 0, 0, 1],  # 4 -> 5
    [0, 0, 0, 0, 0, 0],  # 5
]

if __name__ == "__main__":
    print_results(G1, "G1")
    print_results(G2, "G2")
    print_results(G3, "G3")
