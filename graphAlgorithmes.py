import networkx as nx
import matplotlib.pyplot as plt
from BFS import bfs_edges
from DFS import dfs_edges
from Dijkstra import dijkstra_path
from BellmanFord import single_source_bellman_ford
from Prim import Prim_minimum_spanning_edges
from Kruskal import minimum_spanning_edges
from Kosaraju import kosaraju_strongly_connected_components
from FloydWarshall import floyd_warshall
from createGraph import createDirectedGraph, createUndirectedGraph, createList
import tkinter as tk


def algoSelector(algo, edges, startNode, isDirected=False, endNode=None):
    edges = edges.split('\n')
    edges = [edge.split() for edge in edges]
    nodes, edges, weight = createList(edges)
    if isDirected:
        G = createDirectedGraph(nodes, edges, weight)
    else:
        G = createUndirectedGraph(nodes, edges, weight)
    match algo:
        case 'BFS':
            output = list(bfs_edges(G, startNode))
            master = tk.Tk()
            master.title("BFS")
            master.geometry("500x500")
            master.configure(bg='white')
            outputLabel = tk.Label(master, text=output)
            outputLabel.grid(row=0, column=0, padx=5, pady=5)
            for i in range(len(output)):
                outputLabel = tk.Label(master, text=output[i], bg='white')
                outputLabel.grid(row=i + 1, column=0, padx=5, pady=5)
            print(output)
        case 'DFS':
            output = list(dfs_edges(G, startNode))
            master = tk.Tk()
            master.title("DFS")
            master.geometry("500x500")
            master.configure(bg='white')
            outputLabel = tk.Label(master, text=output)
            outputLabel.grid(row=0, column=0, padx=5, pady=5)
            for i in range(len(output)):
                outputLabel = tk.Label(master, text=output[i], bg='white')
                outputLabel.grid(row=i + 1, column=0, padx=5, pady=5)
            print(output)
        case 'Kosaraju':
            output = list(kosaraju_strongly_connected_components(G))
            master = tk.Tk()
            master.title("Kosaraju")
            master.geometry("500x500")
            master.configure(bg='white')
            outputLabel = tk.Label(master, text=output)
            outputLabel.grid(row=0, column=0, padx=5, pady=5)
            for i in range(len(output)):
                outputLabel = tk.Label(master, text=output[i], bg='white')
                outputLabel.grid(row=i + 1, column=0, padx=5, pady=5)
            print(output)
        case 'Dijkstra':
            chain = dijkstra_path(G, startNode, endNode)
            output = list(zip(chain, chain[1:]))
            master = tk.Tk()
            master.title("Dijkstra")
            master.geometry("500x500")
            master.configure(bg='white')
            outputLabel = tk.Label(master, text=output)
            outputLabel.grid(row=0, column=0, padx=5, pady=5)
            for i in range(len(output)):
                outputLabel = tk.Label(master, text=output[i], bg='white')
                outputLabel.grid(row=i + 1, column=0, padx=5, pady=5)
            print(output)
        case "Kruskal":
            output = list(minimum_spanning_edges(G))
            master = tk.Tk()
            master.title("Kruskal")
            master.geometry("500x500")
            master.configure(bg='white')
            outputLabel = tk.Label(master, text=output)
            outputLabel.grid(row=0, column=0, padx=5, pady=5)
            for i in range(len(output)):
                outputLabel = tk.Label(master, text=output[i], bg='white')
                outputLabel.grid(row=i + 1, column=0, padx=5, pady=5)
            print(output)
        case "Prim":
            output = list(Prim_minimum_spanning_edges(G))
            master = tk.Tk()
            master.title("Prim")
            master.geometry("500x500")
            master.configure(bg='white')
            outputLabel = tk.Label(master, text=output)
            outputLabel.grid(row=0, column=0, padx=5, pady=5)
            for i in range(len(output)):
                outputLabel = tk.Label(master, text=output[i], bg='white')
                outputLabel.grid(row=i + 1, column=0, padx=5, pady=5)
            print(output)
        case "floydWarshall":
            output = list(floyd_warshall(G, weight="weight"))
            master = tk.Tk()
            master.title("Floyd-Warshall")
            master.geometry("500x500")
            master.configure(bg='white')
            outputLabel = tk.Label(master, text=output)
            outputLabel.grid(row=0, column=0, padx=5, pady=5)
            for i in range(len(output)):
                outputLabel = tk.Label(master, text=output[i], bg='white')
                outputLabel.grid(row=i + 1, column=0, padx=5, pady=5)
            print(output)

    G.clear()
    if isDirected:
        G = createDirectedGraph(nodes, output, weight)
    else:
        G = createUndirectedGraph(nodes, output, weight)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()

