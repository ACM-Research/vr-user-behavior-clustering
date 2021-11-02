from geopy import distance
from typing import Tuple
from math import atan2, asin, degrees

Vector2 = Tuple[float, float]
Vector3 = Tuple[float, float, float]

distance.EARTH_RADIUS = 1

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

def getGeodesicDistance(point1: Vector3, point2: Vector3):
    spherical1 = cartesianToSpherical(point1)
    spherical2 = cartesianToSpherical(point2)
    return distance.great_circle((spherical1[1], spherical1[0]), (spherical2[1], spherical2[0]))

#print(getGeodesicDistance((-0.16352, 0.10097, 0.98136)
# Parameters:
# positionMatrix - outer List
#def getAffinityMatrix(positionMatrix: List[List[Vector3]], adjacencyThreshold: float):
    
    # Each row is the positions for all users in a single frame.
#    for row in positionMatrix:
#        geographic = cartesianToGeographic(row)

#        for i in range(len(geographic)):
#            dist1 = distance.great_circle(geographic[i][0], geographic[i][1])
#            for j in range(i + 1, len(geographic)):
#                dist2 = distance.great_circle(geographic[j][0], geographic[j][1])
#                if 0 < abs(dist1 - dist2) < adjacencyThreshold:
#                    affinityMatrix[i][j] += 1
                    

 #   userCount = len(positionMatrix)
 #   self.affinityMatrix = np.empty(shape=(userCount, userCount))
 #   self.affinityMatrix.fill(0)
                
  #  return affinityMatrix
