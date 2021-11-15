from networkx import Graph, find_cliques
from math import acos
from typing import List
from Utilities import geoDistance

def printMatrix(matrix):
    print('', end='   ')
    for i in range(len(matrix)):
        if i > 9:
            print(i, end=' ')
        else:
            print(i, end='  ')
    print()
    
    for r, row in enumerate(matrix):
        if r > 9:
            print(r, end=' ')
        else:
            print(r, end='  ')
            
        for c, item in enumerate(row):
            if item > 9:
                print(item, end=' ')
            else:
                print(item, end='  ')
        print()

# Given a particular affinity matrix and threshold, returns a list of clusters
# using BK max clique.
def getClusters(affinityMatrix: List[List[int]], affinityThreshold: int):
    userCount = len(affinityMatrix)
    graph = Graph()

    # Add all users to the graph
    for i in range(userCount):
        graph.add_node(i)

    # Add edges
    for i in range(userCount):
        row = affinityMatrix[i]
        for j in range(i + 1, userCount):
            if row[j] > affinityThreshold:
                graph.add_edge(i, j)
    
    clusters = []
    currentGraph = graph.copy()
    
    while currentGraph.number_of_nodes() > 0:
        cliqueIterator = find_cliques(currentGraph)
        maxClique = next(cliqueIterator)

        # Find the clique with the most nodes.
        for clique in cliqueIterator:
            if len(clique) > len(maxClique):
                maxClique = clique
            # Optimization: if a clique includes more than half of the nodes in the entire
            # graph, it must be the maximum clique.
            if len(clique) > currentGraph.number_of_nodes() / 2 + 1:
                break

        # Append the clique with the most nodes to the cluster list.
        clusters.append(maxClique)
        
        # Remove nodes in the clique from the graph.
        currentGraph.remove_nodes_from(maxClique)
        
    return clusters

# Populates an affinity matrix for a given chunk using geodesic distance
# to determine whether users are adjacent for a given frame.
# The matrix is assumed to be initialized to all 0 values.
def affinityGeodesic(chunk, affinityMatrix: List[List[int]], distanceThreshold: int):
    for userPositions in chunk.tracePositions:
        for i in range(chunk.userCount):
            row = affinityMatrix[i]
            for j in range(i + 1, chunk.userCount):
                if geoDistance(userPositions[i], userPositions[j]) <= distanceThreshold:
                    row[j] += 1
                            
def affinity(normalizedTracePositions, algorithm, affinityMatrix: List[List[int]]):
    for i in range(len(affinityMatrix)):
        row = affinityMatrix[i]
        for j in range(i + 1, len(row)):
            row[j] = 0

    for userPositions in normalizedTracePositions:
        algorithm.fit(userPositions)
        clusters = algorithm.getCluster()

        for cluster in clusters:
            cluster.sort()
            for i in range(len(cluster)):
                for j in range(i + 1, len(cluster)):
                    user1 = cluster[i]
                    user2 = cluster[j]
                    affinityMatrix[user1][user2] += 1
