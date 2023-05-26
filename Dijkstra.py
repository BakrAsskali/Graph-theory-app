from collections import deque
from heapq import heappop, heappush
from itertools import count
import networkx as nx



def _weight_function(G, weight):
    
    if callable(weight):
        return weight
    if G.is_multigraph():
        return lambda u, v, d: min(attr.get(weight, 1) for attr in d.values())
    return lambda u, v, data: data.get(weight, 1)


def dijkstra_path(G, source, target, weight="weight"):
    
    (length, path) = single_source_dijkstra(G, source, target=target, weight=weight)
    return path


def dijkstra_path_length(G, source, target, weight="weight"):
    
    if source not in G:
        raise nx.NodeNotFound(f"Node {source} not found in graph")
    if source == target:
        return 0
    weight = _weight_function(G, weight)
    length = _dijkstra(G, source, weight, target=target)
    try:
        return length[target]
    except KeyError as err:
        raise nx.NetworkXNoPath(f"Node {target} not reachable from {source}") from err


def single_source_dijkstra_path(G, source, cutoff=None, weight="weight"):
    
    return multi_source_dijkstra_path(G, {source}, cutoff=cutoff, weight=weight)


def single_source_dijkstra_path_length(G, source, cutoff=None, weight="weight"):
    
    return multi_source_dijkstra_path_length(G, {source}, cutoff=cutoff, weight=weight)


def single_source_dijkstra(G, source, target=None, cutoff=None, weight="weight"):
    
    return multi_source_dijkstra(
        G, {source}, cutoff=cutoff, target=target, weight=weight
    )


def multi_source_dijkstra_path(G, sources, cutoff=None, weight="weight"):
   
    length, path = multi_source_dijkstra(G, sources, cutoff=cutoff, weight=weight)
    return path


def multi_source_dijkstra_path_length(G, sources, cutoff=None, weight="weight"):
   
    if not sources:
        raise ValueError("sources must not be empty")
    for s in sources:
        if s not in G:
            raise nx.NodeNotFound(f"Node {s} not found in graph")
    weight = _weight_function(G, weight)
    return _dijkstra_multisource(G, sources, weight, cutoff=cutoff)


def multi_source_dijkstra(G, sources, target=None, cutoff=None, weight="weight"):
    
    if not sources:
        raise ValueError("sources must not be empty")
    for s in sources:
        if s not in G:
            raise nx.NodeNotFound(f"Node {s} not found in graph")
    if target in sources:
        return (0, [target])
    weight = _weight_function(G, weight)
    paths = {source: [source] for source in sources}  # dictionary of paths
    dist = _dijkstra_multisource(
        G, sources, weight, paths=paths, cutoff=cutoff, target=target
    )
    if target is None:
        return (dist, paths)
    try:
        return (dist[target], paths[target])
    except KeyError as err:
        raise nx.NetworkXNoPath(f"No path to {target}.") from err


def _dijkstra(G, source, weight, pred=None, paths=None, cutoff=None, target=None):
    
    return _dijkstra_multisource(
        G, [source], weight, pred=pred, paths=paths, cutoff=cutoff, target=target
    )


def _dijkstra_multisource(
    G, sources, weight, pred=None, paths=None, cutoff=None, target=None
):
    
    G_succ = G._adj  

    push = heappush
    pop = heappop
    dist = {} 
    seen = {}
    c = count()
    fringe = []
    for source in sources:
        seen[source] = 0
        push(fringe, (0, next(c), source))
    while fringe:
        (d, _, v) = pop(fringe)
        if v in dist:
            continue 
        dist[v] = d
        if v == target:
            break
        for u, e in G_succ[v].items():
            cost = weight(v, u, e)
            if cost is None:
                continue
            vu_dist = dist[v] + cost
            if cutoff is not None:
                if vu_dist > cutoff:
                    continue
            if u in dist:
                u_dist = dist[u]
                if vu_dist < u_dist:
                    raise ValueError("Contradictory paths found:", "negative weights?")
                elif pred is not None and vu_dist == u_dist:
                    pred[u].append(v)
            elif u not in seen or vu_dist < seen[u]:
                seen[u] = vu_dist
                push(fringe, (vu_dist, next(c), u))
                if paths is not None:
                    paths[u] = paths[v] + [u]
                if pred is not None:
                    pred[u] = [v]
            elif vu_dist == seen[u]:
                if pred is not None:
                    pred[u].append(v)

    # The optional predecessor and path dictionaries can be accessed
    # by the caller via the pred and paths objects passed as arguments.
    return dist


def dijkstra_predecessor_and_distance(G, source, cutoff=None, weight="weight"):
    
    if source not in G:
        raise nx.NodeNotFound(f"Node {source} is not found in the graph")
    weight = _weight_function(G, weight)
    pred = {source: []}  # dictionary of predecessors
    return (pred, _dijkstra(G, source, weight, pred=pred, cutoff=cutoff))


def all_pairs_dijkstra(G, cutoff=None, weight="weight"):
    
    for n in G:
        dist, path = single_source_dijkstra(G, n, cutoff=cutoff, weight=weight)
        yield (n, (dist, path))


def all_pairs_dijkstra_path_length(G, cutoff=None, weight="weight"):
    
    length = single_source_dijkstra_path_length
    for n in G:
        yield (n, length(G, n, cutoff=cutoff, weight=weight))


def all_pairs_dijkstra_path(G, cutoff=None, weight="weight"):
    
    path = single_source_dijkstra_path
    for n in G:
        yield (n, path(G, n, cutoff=cutoff, weight=weight))


def bidirectional_dijkstra(G, source, target, weight="weight"):
    if source not in G or target not in G:
        msg = f"Either source {source} or target {target} is not in G"
        raise nx.NodeNotFound(msg)

    if source == target:
        return (0, [source])

    weight = _weight_function(G, weight)
    push = heappush
    pop = heappop
    dists = [{}, {}] 
    paths = [{source: [source]}, {target: [target]}]
    fringe = [[], []] 
    seen = [{source: 0}, {target: 0}] 
    c = count()
    push(fringe[0], (0, next(c), source))
    push(fringe[1], (0, next(c), target))
    if G.is_directed():
        neighs = [G._succ, G._pred]
    else:
        neighs = [G._adj, G._adj]
    finalpath = []
    dir = 1
    while fringe[0] and fringe[1]:
        dir = 1 - dir
        (dist, _, v) = pop(fringe[dir])
        if v in dists[dir]:
            continue
        dists[dir][v] = dist 
        if v in dists[1 - dir]:
            return (finaldist, finalpath)

        for w, d in neighs[dir][v].items():
            cost = weight(v, w, d) if dir == 0 else weight(w, v, d)
            if cost is None:
                continue
            vwLength = dists[dir][v] + cost
            if w in dists[dir]:
                if vwLength < dists[dir][w]:
                    raise ValueError("Contradictory paths found: negative weights?")
            elif w not in seen[dir] or vwLength < seen[dir][w]:

                seen[dir][w] = vwLength
                push(fringe[dir], (vwLength, next(c), w))
                paths[dir][w] = paths[dir][v] + [w]
                if w in seen[0] and w in seen[1]:
                    totaldist = seen[0][w] + seen[1][w]
                    if finalpath == [] or finaldist > totaldist:
                        finaldist = totaldist
                        revpath = paths[1][w][:]
                        revpath.reverse()
                        finalpath = paths[0][w] + revpath[1:]
    raise nx.NetworkXNoPath(f"No path between {source} and {target}.")