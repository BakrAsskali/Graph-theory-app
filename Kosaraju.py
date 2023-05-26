import networkx as nx
from networkx.utils import not_implemented_for

def strongly_connected_components(G):
    
    preorder = {}
    lowlink = {}
    scc_found = set()
    scc_queue = []
    i = 0  # Preorder counter
    neighbors = {v: iter(G[v]) for v in G}
    for source in G:
        if source not in scc_found:
            queue = [source]
            while queue:
                v = queue[-1]
                if v not in preorder:
                    i = i + 1
                    preorder[v] = i
                done = True
                for w in neighbors[v]:
                    if w not in preorder:
                        queue.append(w)
                        done = False
                        break
                if done:
                    lowlink[v] = preorder[v]
                    for w in G[v]:
                        if w not in scc_found:
                            if preorder[w] > preorder[v]:
                                lowlink[v] = min([lowlink[v], lowlink[w]])
                            else:
                                lowlink[v] = min([lowlink[v], preorder[w]])
                    queue.pop()
                    if lowlink[v] == preorder[v]:
                        scc = {v}
                        while scc_queue and preorder[scc_queue[-1]] > preorder[v]:
                            k = scc_queue.pop()
                            scc.add(k)
                        scc_found.update(scc)
                        yield scc
                    else:
                        scc_queue.append(v)



def kosaraju_strongly_connected_components(G, source=None):
    
    post = list(nx.dfs_postorder_nodes(G.reverse(copy=False), source=source))

    seen = set()
    while post:
        r = post.pop()
        if r in seen:
            continue
        c = nx.dfs_preorder_nodes(G, r)
        new = {v for v in c if v not in seen}
        seen.update(new)
        yield new



def strongly_connected_components_recursive(G):
    
    def visit(v, cnt):
        root[v] = cnt
        visited[v] = cnt
        cnt += 1
        stack.append(v)
        for w in G[v]:
            if w not in visited:
                yield from visit(w, cnt)
            if w not in component:
                root[v] = min(root[v], root[w])
        if root[v] == visited[v]:
            component[v] = root[v]
            tmpc = {v}  # hold nodes in this component
            while stack[-1] != v:
                w = stack.pop()
                component[w] = root[v]
                tmpc.add(w)
            stack.remove(v)
            yield tmpc

    visited = {}
    component = {}
    root = {}
    cnt = 0
    stack = []
    for source in G:
        if source not in visited:
            yield from visit(source, cnt)


@not_implemented_for("undirected")
def number_strongly_connected_components(G):
    
    return sum(1 for scc in strongly_connected_components(G))


@not_implemented_for("undirected")
def is_strongly_connected(G):
    
    if len(G) == 0:
        raise nx.NetworkXPointlessConcept(
            """Connectivity is undefined for the null graph."""
        )

    return len(next(strongly_connected_components(G))) == len(G)


@not_implemented_for("undirected")
def condensation(G, scc=None):
    
    if scc is None:
        scc = nx.strongly_connected_components(G)
    mapping = {}
    members = {}
    C = nx.DiGraph()
    # Add mapping dict as graph attribute
    C.graph["mapping"] = mapping
    if len(G) == 0:
        return C
    for i, component in enumerate(scc):
        members[i] = component
        mapping.update((n, i) for n in component)
    number_of_components = i + 1
    C.add_nodes_from(range(number_of_components))
    C.add_edges_from(
        (mapping[u], mapping[v]) for u, v in G.edges() if mapping[u] != mapping[v]
    )
    # Add a list of members (ie original nodes) to each node (ie scc) in C.
    nx.set_node_attributes(C, members, "members")
    return C