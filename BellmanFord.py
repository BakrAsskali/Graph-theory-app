import networkx as nx
from collections import deque
from networkx.algorithms.shortest_paths.generic import _build_paths_from_predecessors

def _weight_function(G, weight):
    if callable(weight):
        return weight
    
    
    
    if G.is_multigraph():
        return lambda u, v, d: min(attr.get(weight, 1) for attr in d.values())
    return lambda u, v, data: data.get(weight, 1)

def bellman_ford_predecessor_and_distance(
    G, source, target=None, weight="weight", heuristic=False
):
    if source not in G:
        raise nx.NodeNotFound(f"Node {source} is not found in the graph")
    weight = _weight_function(G, weight)
    if any(weight(u, v, d) < 0 for u, v, d in nx.selfloop_edges(G, data=True)):
        raise nx.NetworkXUnbounded("Negative cycle detected.")

    dist = {source: 0}
    pred = {source: []}

    if len(G) == 1:
        return pred, dist

    weight = _weight_function(G, weight)

    dist = _bellman_ford(
        G, [source], weight, pred=pred, dist=dist, target=target, heuristic=heuristic
    )
    return (pred, dist)



def _bellman_ford(
    G,
    source,
    weight,
    pred=None,
    paths=None,
    dist=None,
    target=None,
    heuristic=True,
):
    if pred is None:
        pred = {v: [] for v in source}

    if dist is None:
        dist = {v: 0 for v in source}

    negative_cycle_found = _inner_bellman_ford(
        G,
        source,
        weight,
        pred,
        dist,
        heuristic,
    )
    if negative_cycle_found is not None:
        raise nx.NetworkXUnbounded("Negative cycle detected.")

    if paths is not None:
        sources = set(source)
        dsts = [target] if target is not None else pred
        for dst in dsts:
            gen = _build_paths_from_predecessors(sources, dst, pred)
            paths[dst] = next(gen)

    return dist


def _inner_bellman_ford(
    G,
    sources,
    weight,
    pred,
    dist=None,
    heuristic=True,
):
    for s in sources:
        if s not in G:
            raise nx.NodeNotFound(f"Source {s} not in G")

    if pred is None:
        pred = {v: [] for v in sources}

    if dist is None:
        dist = {v: 0 for v in sources}

    
    nonexistent_edge = (None, None)
    pred_edge = {v: None for v in sources}
    recent_update = {v: nonexistent_edge for v in sources}

    G_succ = G._adj  
    inf = float("inf")
    n = len(G)

    count = {}
    q = deque(sources)
    in_q = set(sources)
    while q:
        u = q.popleft()
        in_q.remove(u)

        
        if all(pred_u not in in_q for pred_u in pred[u]):
            dist_u = dist[u]
            for v, e in G_succ[u].items():
                dist_v = dist_u + weight(u, v, e)

                if dist_v < dist.get(v, inf):
                    
                    
                    
                    
                    
                    
                    if heuristic:
                        if v in recent_update[u]:
                            
                            pred[v].append(u)
                            return v

                        
                        
                        
                        
                        if v in pred_edge and pred_edge[v] == u:
                            recent_update[v] = recent_update[u]
                        else:
                            recent_update[v] = (u, v)

                    if v not in in_q:
                        q.append(v)
                        in_q.add(v)
                        count_v = count.get(v, 0) + 1
                        if count_v == n:
                            
                            return v

                        count[v] = count_v
                    dist[v] = dist_v
                    pred[v] = [u]
                    pred_edge[v] = u

                elif dist.get(v) is not None and dist_v == dist.get(v):
                    pred[v].append(u)

    
    return None

def bellman_ford_path(G, source, target, weight="weight"):
    length, path = single_source_bellman_ford(G, source, target=target, weight=weight)
    return path



def bellman_ford_path_length(G, source, target, weight="weight"):
    if source == target:
        if source not in G:
            raise nx.NodeNotFound(f"Node {source} not found in graph")
        return 0

    weight = _weight_function(G, weight)

    length = _bellman_ford(G, [source], weight, target=target)

    try:
        return length[target]
    except KeyError as err:
        raise nx.NetworkXNoPath(f"node {target} not reachable from {source}") from err


def single_source_bellman_ford_path(G, source, weight="weight"):
    (length, path) = single_source_bellman_ford(G, source, weight=weight)
    return path


def single_source_bellman_ford_path_length(G, source, weight="weight"):
    weight = _weight_function(G, weight)
    return _bellman_ford(G, [source], weight)


def single_source_bellman_ford(G, source, target=None, weight="weight"):
    if source == target:
        if source not in G:
            raise nx.NodeNotFound(f"Node {source} is not found in the graph")
        return (0, [source])

    weight = _weight_function(G, weight)

    paths = {source: [source]}  
    dist = _bellman_ford(G, [source], weight, paths=paths, target=target)
    if target is None:
        return (dist, paths)
    try:
        return (dist[target], paths[target])
    except KeyError as err:
        msg = f"Node {target} not reachable from {source}"
        raise nx.NetworkXNoPath(msg) from err


def all_pairs_bellman_ford_path_length(G, weight="weight"):
    length = single_source_bellman_ford_path_length
    for n in G:
        yield (n, dict(length(G, n, weight=weight)))


def all_pairs_bellman_ford_path(G, weight="weight"):
    path = single_source_bellman_ford_path
    
    for n in G:
        yield (n, path(G, n, weight=weight))
