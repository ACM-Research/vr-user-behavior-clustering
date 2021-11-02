from networkx import Graph, find_cliques
from math import acos

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
        cliqueIterator = find_cliques(currentGraph)
        maxClique = next(cliqueIterator)

        # Find the clique with the most nodes.
        for clique in cliqueIterator:
            if len(clique) > len(maxClique):
                maxClique = clique
            # Optimization: if a clique includes more than half of the nodes in the entire
            # graph, it must have the most nodes.
            if len(clique) > currentGraph.number_of_nodes() / 2 + 1:
                break

        # Append the clique with the most nodes to the cluster list.
        clusters.append(maxClique)
        
        # Remove nodes in the clique from the graph.
        currentGraph.remove_nodes_from(maxClique)
        
    return clusters

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

def getClusters(chunk, distanceThreshold, affinityThreshold):
    userCount = len(chunk.tracePositions[0])
    affinityMatrix = [[0 for _ in range(userCount)] for _ in range(userCount)]

    # Construct affinity matrix
    for userList in chunk.tracePositions:
        for i in range(userCount):
            for j in range(i + 1, userCount):
                point1 = userList[i]
                point2 = userList[j]
                # arccos  of dot product of the two points
                geoDistance = acos(point1[0] * point2[0] + point1[1] * point2[1] + point1[2] * point2[2])
                if geoDistance <= distanceThreshold:
                    affinityMatrix[i][j] += 1

    #printMatrix(affinityMatrix)
    # Construct graph from affinity matrix
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

        cliqueIterator = find_cliques(graph)
        maxClique = next(cliqueIterator)

        # Find the clique with the most nodes.
        for clique in cliqueIterator:
            if len(clique) > len(maxClique):
                maxClique = clique

        # Remove nodes in the clique from the graph.
        currentGraph.remove_nodes_from(maxClique)
        
        # Return the clique with the most nodes.
        return maxClique
