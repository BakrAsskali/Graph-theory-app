from heapq import heappop, heappush
from itertools import count
from math import isnan

def Prim_minimum_spanning_edges(
    G, algorithm="prim", weight="weight", keys=True, data=True, ignore_nan=False
):

    return prim_mst_edges(
        G, minimum=True, weight=weight, keys=keys, data=data, ignore_nan=ignore_nan
    )


def prim_mst_edges(G, minimum, weight="weight", keys=True, data=True, ignore_nan=False):
    is_multigraph = G.is_multigraph()
    push = heappush
    pop = heappop

    nodes = set(G)
    c = count()

    sign = 1 if minimum else -1

    while nodes:
        u = nodes.pop()
        frontier = []
        visited = {u}
        if is_multigraph:
            for v, keydict in G.adj[u].items():
                for k, d in keydict.items():
                    wt = d.get(weight, 1) * sign
                    if isnan(wt):
                        if ignore_nan:
                            continue
                        msg = f"NaN found as an edge weight. Edge {(u, v, k, d)}"
                        raise ValueError(msg)
                    push(frontier, (wt, next(c), u, v, k, d))
        else:
            for v, d in G.adj[u].items():
                wt = d.get(weight, 1) * sign
                if isnan(wt):
                    if ignore_nan:
                        continue
                    msg = f"NaN found as an edge weight. Edge {(u, v, d)}"
                    raise ValueError(msg)
                push(frontier, (wt, next(c), u, v, d))
        while nodes and frontier:
            if is_multigraph:
                W, _, u, v, k, d = pop(frontier)
            else:
                W, _, u, v, d = pop(frontier)
            if v in visited or v not in nodes:
                continue
            # Multigraphs need to handle edge keys in addition to edge data.
            if is_multigraph and keys:
                if data:
                    yield u, v, k, d
                else:
                    yield u, v, k
            else:
                if data:
                    yield u, v, d
                else:
                    yield u, v
            # update frontier
            visited.add(v)
            nodes.discard(v)
            if is_multigraph:
                for w, keydict in G.adj[v].items():
                    if w in visited:
                        continue
                    for k2, d2 in keydict.items():
                        new_weight = d2.get(weight, 1) * sign
                        if isnan(new_weight):
                            if ignore_nan:
                                continue
                            msg = f"NaN found as an edge weight. Edge {(v, w, k2, d2)}"
                            raise ValueError(msg)
                        push(frontier, (new_weight, next(c), v, w, k2, d2))
            else:
                for w, d2 in G.adj[v].items():
                    if w in visited:
                        continue
                    new_weight = d2.get(weight, 1) * sign
                    if isnan(new_weight):
                        if ignore_nan:
                            continue
                        msg = f"NaN found as an edge weight. Edge {(v, w, d2)}"
                        raise ValueError(msg)
                    push(frontier, (new_weight, next(c), v, w, d2))