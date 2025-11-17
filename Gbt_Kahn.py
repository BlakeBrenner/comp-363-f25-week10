"""
kahn.py

Kahn's algorithm vs. DFS "stack duration" topological sort
using only plain Python (no imports).

For this assignment:
- We show how to obtain the topological sorting of a DAG using recursive DFS
  by timing how long each vertex "stays" in the stack.
"""


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


def topo_stack_duration_with_details(graph):
    """
    Core DFS-based topological sort.

    Uses recursive DFS and records:
    - enter_time[v]: when v is pushed on the recursion stack
    - exit_time[v]:  when v is popped off the recursion stack
    - duration[v] = exit_time[v] - enter_time[v]

    Returns:
        order      : list of vertices in topological order
        durations  : list of durations per vertex
        enter_time : list of enter times per vertex
        exit_time  : list of exit times per vertex
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

    visited    = [False] * N
    enter_time = [0] * N
    exit_time  = [0] * N
    time       = 0  # logical timer

    # Recursive DFS with timestamps
    def dfs(v):
        nonlocal time
        visited[v] = True

        # v is "pushed" on the recursion stack here
        time += 1
        enter_time[v] = time

        # Explore all neighbors
        for u in range(N):
            if graph[v][u] != NO_EDGE and not visited[u]:
                dfs(u)

        # v is about to be "popped" from the recursion stack here
        time += 1
        exit_time[v] = time

    # Run DFS from all vertices (in case graph has multiple components)
    for v in range(N):
        if not visited[v]:
            dfs(v)

    # Compute "time spent on recursion stack"
    durations = [exit_time[v] - enter_time[v] for v in range(N)]

    # Sort vertices by decreasing duration
    order = sorted(range(N), key=lambda v: durations[v], reverse=True)

    return order, durations, enter_time, exit_time


def topo_stack_duration(graph):
    """
    Simple wrapper that only returns the topological order
    (used where we don't care about the detailed timing).
    """
    order, durations, enter_time, exit_time = topo_stack_duration_with_details(graph)
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
                # Must have pos[u] < pos[v] for edge u -> v
                if pos[u] >= pos[v]:
                    return False
    return True


def print_results(graph, name):
    """
    Run both algorithms on 'graph' and print:

    - topological order from Kahn's algorithm
    - topological order from DFS stack-duration method
    - enter_time, exit_time, and duration for each vertex
    """

    print("========================================")
    print("Graph:", name)
    print("----------------------------------------")

    # Kahn's algorithm
    kahn_order = khan(graph)
    print("Kahn's algorithm topological order:")
    print("  ", kahn_order)
    print("  Valid topological sort:", is_valid_topo(graph, kahn_order))
    print()

    # DFS stack-duration algorithm (with details)
    order, durations, enter_time, exit_time = topo_stack_duration_with_details(graph)
    print("DFS stack-duration topological order:")
    print("  ", order)
    print("  Valid topological sort:", is_valid_topo(graph, order))
    print()

    # Detailed timing information
    print("Vertex timing details (per vertex index):")
    print("  v | enter_time | exit_time | duration (exit - enter)")
    print(" ---+------------+-----------+------------------------")
    for v in range(len(graph)):
        et = enter_time[v]
        xt = exit_time[v]
        dur = durations[v]
        print(f"  {v:1d} | {et:10d} | {xt:9d} | {dur:6d}")

    print()

    # Also show the same table but in topological order
    print("Vertex timing details in DFS topo order:")
    print("  v | enter_time | exit_time | duration (exit - enter)")
    print(" ---+------------+-----------+------------------------")
    for v in order:
        et = enter_time[v]
        xt = exit_time[v]
        dur = durations[v]
        print(f"  {v:1d} | {et:10d} | {xt:9d} | {dur:6d}")

    print("========================================")
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
    [0, 1, 2, 0, 0, 1],  # 3 -> 1,2 (2 just means "has edge"),5
    [0, 0, 0, 0, 0, 1],  # 4 -> 5
    [0, 0, 0, 0, 0, 0],  # 5
]


if __name__ == "__main__":
    # Main "driver" code: run on the example DAGs
    print_results(G1, "G1")
    print_results(G2, "G2")
