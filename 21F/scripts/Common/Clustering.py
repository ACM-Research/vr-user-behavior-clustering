import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from geopy import distance
from Utilities import cartesianToSpherical

distance.EARTH_RADIUS = 1

# Returns a list of clusters of the given graph,
# where each cluster is a list of nodes belonging to that graph.
#
# graph - a networkx Graph

def getMaxCliques(graph):
    if graph == None:
        return None
    
    clusters = []
    currentGraph = graph.copy()
    
    while currentGraph.number_of_nodes() > 0:
        cliqueIterator = nx.find_cliques(currentGraph)
        maxClique = next(cliqueIterator)

        # Find the clique with the most nodes.
        for clique in cliqueIterator:
            if len(clique) > len(maxClique):
                maxClique = clique

        # Append the clique with the most nodes to the cluster list.
        clusters.append(maxClique)
        
        # Remove nodes in the clique from the graph.
        currentGraph.remove_nodes_from(maxClique)
        
    return clusters

def getClusters(chunk, distanceThreshold, affinityThreshold):
    userCount = len(chunk.tracePositions[0])
    affinityMatrix = [[0 for _ in range(userCount)] for _ in range(userCount)]

    # Construct affinity matrix
    for userList in chunk.tracePositions:
        for i in range(userCount):
            for j in range(i + 1, userCount):
                geoDistance = distance.great_circle(cartesianToSpherical(userList[i]), cartesianToSpherical(userList[j]))
                if (geoDistance > distanceThreshold):
                    affinityMatrix[i][j] += 1

    # Construct graph from affinity matrix
    graph = nx.Graph()
    for i in range(userCount):
        row = affinityMatrix[i]
        for j in range(userCount):
            if row[j] > affinityThreshold:
                graph.add_edge(i, j)

    return getMaxCliques(graph)

# Iterates that iterates over clusters in a given graph.
class ClusterIterator:
    
    def __init__(self, graph) -> None:
        self.graph = graph.copy

    def __iter__(self) -> None:
        return self
    
    def __next__(self):
        if graph.number_of_nodes() == 0:
            raise StopIteration

        cliqueIterator = nx.find_cliques(graph)
        maxClique = next(cliqueIterator)

        # Find the clique with the most nodes.
        for clique in cliqueIterator:
            if len(clique) > len(maxClique):
                maxClique = clique

        # Remove nodes in the clique from the graph.
        currentGraph.remove_nodes_from(maxClique)
        
        # Return the clique with the most nodes.
        return maxClique

# Returns an affinity matrix for a list of adjacency matrices and a given threshold.
# The affinity matrix returned is a 2d matrix where each entry is an int that is either
# 1 or 0, and has the same size as the adjacency matrices. The affinity matrix is upper
# triangular.
#
# matrices - an iterable object of 2d adjacency matrices, where each entry is an int
# that is either 1 or 0. Each matrix must have the same dimensions. Note that each
# matrix is assumed to be upper triangular. Works with standard Python or numpy arrays.
#
# threshold - the minimum number of times that two nodes must be neighbours in
# the adjacency matrices in order to be considered neighbours in the affinity matrix.
#
# For example, suppose the input matrices are
# |0 1| |0 1| |1 1|
# |0 1| |1 0| |1 0|
# and the threshold is two. The resulting affinity matrix would be
# |0 1|
# |0 0|
# since the sum of the matrices is
# |1 3|
# |2 1|
# and only the top right and bottom left entries sum to two or more,
# while the bottom left entry is disregarded (not part of the upper triangle).

def getAffinityMatrix(matrices, threshold):
    matrixIterator = iter(matrices)
    
    # Get the first adjacency matrix in the matrix iterator.
    firstMatrix = next(matrixIterator)

    # Copy the contents of the first adjacency matrix as a starting point for the affinity matrix.
    affinityMatrix = [row for row in firstMatrix]

    # For each adjacency matrix, add the value in each cell to the corresponding cell of the affinity matrix.
    for matrix in matrixIterator:
        for i in range(len(matrix)):
            row = matrix[i]
            for j in range(i + 1, len(row)):
                affinityMatrix[i][j] += row[j]

    # Set all cells with values that exceed the threshold to one, and all others to zero.
    for i in range(len(affinityMatrix)):
        row = affinityMatrix[i]
        for j in range(i + 1, len(row)):
            if row[j] >= threshold:
                row[j] = 1
            else:
                row[j] = 0

    return affinityMatrix

# Constructs a networkx Graph from an upper triangular adjacency matrix.
def matrixToGraph(matrix):
    graph = nx.Graph()

    for i in range(len(matrix)):
        row = matrix[i]
        for j in range(i + 1, len(row)):
            if row[j] == 1:
                graph.add_edge(i, j)

    return graph
    
def getAffinityMatrix(matrices, affinityThreshold: int):
    matrixIterator = iter(matrices)
    
    # Get the first adjacency matrix in the matrix iterator.
    firstMatrix = next(matrixIterator)

    # Copy the contents of the first adjacency matrix as a starting point for the affinity matrix.
    affinityMatrix = [row for row in firstMatrix]

    # For each adjacency matrix, add the value in each cell to the corresponding cell of the affinity matrix.
    for matrix in matrixIterator:
        for i in range(len(matrix)):
            row = matrix[i]
            for j in range(i + 1, len(row)):
                affinityMatrix[i][j] += row[j]

    # Set all cells with values that exceed the threshold to one, and all others to zero.
    for i in range(len(affinityMatrix)):
        row = affinityMatrix[i]
        for j in range(i + 1, len(row)):
            if row[j] >= affinityThreshold:
                row[j] = 1
            else:
                row[j] = 0

    return affinityMatrix