import math
import array
from geopy import distance
from DataManager import DataManager

# This program uses DataManager to get an array of vectors for a given frame. Then, these vectors are converted to
# geographic coordinates. The geographic coordinates are used to calculate geodesic length and return an adjacency Matrix


# for the video specified by videoId. frameList is assumed to be sorted and to have no duplicates.
class AdjacencyData:
    def __init__(self, dataManager, videoId, frameList):

        # Constant that determines how close variables must be to be considered adjacent
        self.adjacencyThreshold = math.pi / 10
        self.vectorArray = dataManager.getVectors(videoId, frameList)

    def vectorsToGeographic(self) -> object:

        geographicArray = [[] for i in range(len(self.vectorArray))]

        for i in range(len(self.vectorArray)):
            x = self.vectorArray[i][0]
            y = self.vectorArray[i][1]
            z = self.vectorArray[i][2]

            latitude = math.asin(z)
            longitude = math.atan2(y, x)

            geographicArray[i].append((latitude, longitude))

        return geographicArray

    def adjacencyMatrix(self):

        distance.EARTH_RADIUS = 1

        geographicArray = self.vectorsToGeographic()
        adjacencyMatrix = [array.array('L', [0 for i in range(len(geographicArray))]) for j in
                           range(len(geographicArray))]

        for i in range(len(geographicArray)):
            dist1 = distance.great_circle(geographicArray[i][0], geographicArray[i][1])
            for j in range(len(geographicArray)):
                dist2 = distance.great_circle(geographicArray[j][0], geographicArray[j][1])
                if 0 < abs(dist1 - dist2) < self.adjacencyThreshold:
                    adjacencyMatrix[i][j] = 1
                else:
                    adjacencyMatrix[i][j] = 0

        return adjacencyMatrix
