from tkinter import *
from tkinter import ttk

from createGraph import drawGraph
from graphAlgorithmes import algoSelector


def toggleDirected():
    if isDirected.get():
        isUndirected.set(False)
    return


def toggleUndirected():
    if isUndirected.get():
        isDirected.set(False)
    return


root = Tk()
root.title("Graph GUI")

Listlabel = Label(root, text="List of Edges (node1 node2 weight)")
Listlabel.grid(row=0, column=0, padx=5, pady=5)

algoLabel = Label(root, text="Choose Algorithm")
algoLabel.grid(row=1, column=0, padx=5, pady=5)

edges = StringVar()
algoSelection = StringVar()
isDirected = BooleanVar()
isUndirected = BooleanVar()

edges_entry = Text(root, width=30, height=10)
edges_entry.grid(row=0, column=1, padx=5, pady=5)

algoSelection = ttk.Combobox(root, width=27, textvariable=algoSelection)
algoSelection['state'] = 'readonly'
algoSelection['values'] = ('BFS', 'DFS', 'Dijkstra', 'Kruskal', 'Prim', 'Kosaraju')
algoSelection.grid(row=1, column=1, padx=5, pady=5)

start_node = StringVar()
start_node_label = Label(root, text="Start Node")
start_node_label.grid(row=2, column=0, padx=5, pady=5)
start_node_entry = Entry(root, width=30, textvariable=start_node)
start_node_entry.grid(row=2, column=1, padx=5, pady=5)

directedLabel = Label(root, text="Directed")
directedLabel.grid(row=3, column=0, padx=5, pady=5)

undirectedLabel = Label(root, text="Undirected")
undirectedLabel.grid(row=4, column=0, padx=5, pady=5)

directedCheck = Checkbutton(root, variable=isDirected, command=toggleDirected)
directedCheck.grid(row=3, column=1, padx=5, pady=5)

undirectedCheck = Checkbutton(root, variable=isUndirected, command=toggleUndirected)
undirectedCheck.grid(row=4, column=1, padx=5, pady=5)


def draw():
    edges_value = edges_entry.get("1.0", "end-1c")
    if edges_value == '' or (not isDirected.get() and not isUndirected.get()):
        print("Please enter edges and select a graph type")
        return
    else:
        drawGraph(edges_value, isDirected.get())
        return


def runAlgo():
    endNode = StringVar()
    algo = algoSelection.get()
    if algo not in ["BFS", "DFS", "Kruskal", "Prim", "Floyd-Warshall", "Kosaraju", "Dijkstra", "Bellman-Ford"]:
        print("Please select an algorithm")
        return

    if algo in ["Kosaraju"]:
        if not isDirected.get():
            print("Please select a directed graph")
            return
        else:
            algoSelector(algo, edges_entry.get("1.0", "end-1c"), start_node_entry.get(), isDirected.get())
            return

    if algo in ["Dijkstra", "Bellman-Ford"]:
        top = Toplevel()
        top.title(algo)

        Label(top, text="End Node").grid(row=0)
        e1 = Entry(top, textvariable=endNode)
        e1.grid(row=0, column=1)

        Button(top, text='Quit', command=top.destroy).grid(row=3, column=0, sticky=W, pady=4)
        Button(top, text='Run', command=lambda: algoSelector(algo, edges_entry.get("1.0", "end-1c"),
                                                             start_node_entry.get(), isDirected.get(),
                                                             endNode.get())).grid(row=3, column=1, sticky=W, pady=4)

    else:
        algoSelector(algo, edges_entry.get("1.0", "end-1c"), start_node_entry.get(), isDirected.get())


drawButton = Button(root, text="Draw", command=draw)
drawButton.grid(row=5, column=0, padx=5, pady=5)

algoButton = Button(root, text="Run", command=runAlgo)
algoButton.grid(row=5, column=1, padx=5, pady=5)

root.mainloop()
