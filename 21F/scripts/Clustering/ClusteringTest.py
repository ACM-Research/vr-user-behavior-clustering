# BROKEN - DOES NOT WORK

import networkx as nx
import numpy as np
import Clustering.Clustering

# AFFINITY MATRIX TEST

matrices = [np.array([[1, 0, 1, 1, 0], [1, 0, 1, 0, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [1, 0, 1, 1, 0]]), 
            np.array([[1, 1, 1, 0, 1], [0, 1, 0, 1, 0], [1, 0, 0, 0, 1], [1, 1, 1, 0, 1], [0, 1, 1, 1, 0]]),
            np.array([[1, 1, 1, 0, 1], [0, 1, 0, 1, 0], [1, 0, 0, 0, 1], [1, 1, 1, 0, 1], [0, 1, 1, 1, 0]]),
            np.array([[1, 1, 1, 0, 1], [0, 1, 0, 1, 0], [1, 0, 0, 0, 1], [1, 1, 1, 0, 1], [0, 1, 1, 1, 0]])]

affinityMatrix = getAffinityMatrix(matrices, 2)
for row in affinityMatrix:
    print(row)

# GRAPH CONSTRUCTION TEST

graph = matrixToGraph(affinityMatrix)

# CLUSTERING TEST

#graph = nx.Graph()
#graph.add_edges_from([(2, 4), (1, 3), (2, 3), (3, 6), (4, 5), (5, 6), (1, 7), (1, 2), (3, 4), (4, 6)])
pos = nx.shell_layout(graph)
nx.draw_networkx(graph, pos=pos)
plt.show()

clusters = getClusters(graph)
for cluster in clusters:
    clusterGraph = graph.subgraph(cluster)
    nx.draw_networkx(clusterGraph, pos=pos)
    
plt.show()
