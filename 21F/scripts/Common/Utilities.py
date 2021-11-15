from typing import List, Tuple
from math import acos, atan2, asin, degrees

Vector2 = Tuple[float, float]
Vector3 = Tuple[float, float, float]

# Given a cartesian coordinate (x, y, z) returns the equivalent spherical coordinate (yaw, pitch).
def cartesianToSpherical(xyz: Vector3) -> Vector2:
    yaw = degrees(atan2(xyz[0], xyz[2]))
    pitch = degrees(asin(xyz[1]))
    return (pitch, yaw)

def mapTo2D(xyz: Vector3, dimensions) -> Vector2:
    (pitch, yaw) = cartesianToSpherical(xyz)
    x = ((yaw + 180) / 360) * dimensions[0]
    y = ((90 - pitch) / 180) * dimensions[1]
    return (x, y)

def geoDistance(point1: Vector3, point2: Vector3):
    dotProduct = point1[0] * point2[0] + point1[1] * point2[1] + point1[2] * point2[2]
    
    # Sometimes, due to rounding errors, the dot product falls slightly outside of the
    # range [-1, 1], causing an domain error for acos. So we clamp it to [-1, 1].
    if dotProduct < -1:
        dotProduct = -1
    elif dotProduct > 1:
        dotProduct = 1
                    
    return acos(dotProduct)

# Upon completion, matrix[i][j] will contain the distance between positions[i] and positions[j]
def populateDistanceMatrix(positions: List[Vector3], matrix: List[List[float]]):
    positionsCount = len(positions)
    
    for i in range(positionsCount):
        for j in range(i + 1, positionsCount):
            matrix[i][j] = geoDistance(positions[i], positions[j])
    
# Returns the sum of the distances between the user specified by userIndex and all the users in cluster.
def getDistancesSum(userIndex: int, distanceMatrix: List[List[int]], cluster: List[int]):
    distancesSum = 0.0
    
    for otherUserIndex in cluster:
        if userIndex < otherUserIndex:
            distancesSum += float(distanceMatrix[userIndex][otherUserIndex])
        elif userIndex > otherUserIndex:
            distancesSum += float(distanceMatrix[otherUserIndex][userIndex])

    return distancesSum

# distances - distance matrix for users, where distrances[i][j] gives the distance between users i and j
# clusters  - a list of clusters
# scores    - array to output silhouette scores to

# This functions performs effectively performs:
# for i in range(scores):
#     scores[i] += silhouette score for user i

def getSilhouetteScores(distances: List[List[int]], clusters: List[List[int]], scores: List[float]):
    # Case in which there is only one cluster
    if len(clusters) < 2:
        return 1
    
    userCount = len(distances)

    for (clusterIndex, cluster) in enumerate(clusters):
        # If the cluster contains only one user, the silhouette score for that user is 0
        if len(cluster) == 1:
            continue

        for userIndex in cluster:
            # Compute the mean distance from user to other users in the same cluster
            a = getDistancesSum(userIndex, distances, cluster) / (len(cluster) - 1)
            
            # Compute the mean distance from user to other users in the next nearest cluster
            b = float('inf')

            for i in range(0, clusterIndex):
                otherCluster = clusters[i]
                meanDistance = getDistancesSum(userIndex, distances, otherCluster) / len(otherCluster)
                if b > meanDistance:
                    b = meanDistance

            for i in range(clusterIndex + 1, len(clusters)):
                otherCluster = clusters[i]
                meanDistance = getDistancesSum(userIndex, distances, otherCluster) / len(otherCluster)
                if b > meanDistance:
                    b = meanDistance

            # Compute silhouette score
            s = b - a
            s = s / a if a > b else s / b
            scores[userIndex] += s

class UserDataPoint:
    def __init__(self, idx, location: Vector3):
        self.idx = idx
        self.location = list(location)
    
    def __repr__(self):
        return "%s, [%f, %f, %f]" % (self.idx, self.location[0], self.location[1], self.location[2])
    def __str__(self):
        return "%s, [%f, %f, %f]" % (self.idx, self.location[0], self.location[1], self.location[2])
            
def standardize_data(data: List[Vector3]) -> List[UserDataPoint]:
    dataList = []
    for idx, value in enumerate(data):
        dataList.append(UserDataPoint(idx, value))
    return dataList
