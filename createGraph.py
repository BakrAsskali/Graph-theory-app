from matplotlib import pyplot as plt
import networkx as nx


def createUndirectedGraph(nodes, edges):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    add_weighted_edges_if_exist(G, edges)
    print(G.nodes())
    return G


def createDirectedGraph(nodes, edges):
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    add_weighted_edges_if_exist(G, edges)
    print(G.nodes())
    return G


def add_weighted_edges_if_exist(G, edges):
    isWeighted = False
    for edge in edges:
        if len(edge) >= 2:
            if len(edge) == 2:
                G.add_edge(edge[0], edge[1])
            else:
                G.add_edge(edge[0], edge[1], weight=edge[2])
                isWeighted = True
    if isWeighted:
        G.graph['edge_weight_attr'] = 'weight'
    return G

def drawGraph(edges, isDirected=False):
    edges = edges.split('\n')
    edges = [edge.split() for edge in edges]
    nodes, edges, weight = createList(edges)
    if isDirected:
        G = createDirectedGraph(nodes, edges)
    else:
        G = createUndirectedGraph(nodes, edges)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()
    return

def createList(edges):
    edge_tuple =[(edge[0], edge[1]) for edge in edges]
    nodes = list(set([node for edge in edge_tuple for node in edge]))
    weight = [edge[2] for edge in edges if len(edge) == 3]
    return nodes, edge_tuple, weight


    
