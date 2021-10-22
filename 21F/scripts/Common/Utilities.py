from geopy import distance
from typing import Tuple

Vector2 = Tuple[float, float]
Vector3 = Tuple[float, float, float]

distance.EARTH_RADIUS = 1

# Given a cartesian coordinate (x, y, z) returns the equivalent spherical coordinate (yaw, pitch).
def cartesianToSpherical(xyz: Tuple[float, float, float]) -> Tuple[float, float]:
    yaw = math.degrees(math.atan2(xyz[0], xyz[2]))
    pitch = math.degrees(math.asin(xyz[1]))
    return (yaw, pitch)

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
