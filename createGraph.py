from matplotlib import pyplot as plt
import networkx as nx


def createUndirectedGraph(nodes, edges, weight=None):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    add_weighted_edges_if_exist(G, weight, edges)
    print(G.nodes())
    return G


def createDirectedGraph(nodes, edges, weight=None):
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    add_weighted_edges_if_exist(G, weight, edges)
    print(G.nodes())
    return G


def add_weighted_edges_if_exist(G, weight, edges=None):
    if weight:
        weighted_edges = [(edge[0], edge[1], w) for edge, w in zip(edges, weight)]
        G.add_weighted_edges_from(weighted_edges)
    else:
        G.add_edges_from(edges)


def drawGraph(edges, isDirected=False):
    edges = edges.split('\n')
    edges = [edge.split() for edge in edges]
    nodes, edges, weight = createList(edges)

    if isDirected:
        G = createDirectedGraph(nodes, edges, weight)
    else:
        G = createUndirectedGraph(nodes, edges, weight)
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_size=500)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='b', arrows=True)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()
    return


def createList(edges):
    edge_tuple = [(edge[0], edge[1]) for edge in edges]
    nodes = list(set([node for edge in edge_tuple for node in edge]))
    weight = [float(edge[2]) if len(edge) == 3 else 1.0 for edge in edges]
    return nodes, edge_tuple, weight

