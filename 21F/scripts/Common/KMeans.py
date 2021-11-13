import sys, random
import numpy as np
from typing import Tuple, List

from numpy.ma.core import default_fill_value

from VideoUtil import VideoData, VideoDataManager
from Utilities import mapTo2D, getGeodesicDistance

class UserDataPoint:
    def __init__(self, idx, location: Tuple[float, float, float]):
        self.idx = idx
        self.location = list(location)
    
    def __repr__(self):
        return "%s, [%f, %f, %f]" % (self.idx, self.location[0], self.location[1], self.location[2])
    def __str__(self):
        return "%s, [%f, %f, %f]" % (self.idx, self.location[0], self.location[1], self.location[2])

def standardize_data(data: List[Tuple[float, float, float]]) -> List[UserDataPoint]:
    dataList = []

    for idx, value in enumerate(data): dataList.append(UserDataPoint(idx, value))
    return dataList

class KMeans:
    def __init__(self, k=2, tol=0.01, random_state = None, max_iter=300):
        if random_state is not None: random.seed(random_state)
        self.k = k
        self.tol = tol
        self.max_iter = max_iter

    def fit(self, userPointList : list):
        self.centroids = random.sample(userPointList, self.k)
        
        for i in range(self.max_iter):
            self.classifications = {}

            for i in range(self.k):
                self.classifications[i] = []

            for userPoint in userPointList:
                geodesicDistances = [getGeodesicDistance(userPoint.location, centroid.location) for centroid in self.centroids]
                classification = geodesicDistances.index(min(geodesicDistances))
                self.classifications[classification].append(userPoint)

            prev_centroids = self.centroids

            for classification in self.classifications:
                locationsList = [pos.location for pos in self.classifications[classification]]
                self.centroids[classification] = UserDataPoint(classification, np.average(locationsList,axis=0))

            optimized = True

            for idx, value in enumerate(self.centroids):
                original_centroid = np.array(prev_centroids[idx].location)
                current_centroid = np.array(value.location)
                
                # mape = np.mean(np.abs(original_centroid - original_centroid) / original_centroid) * 100
                mape = np.sum((current_centroid - original_centroid) / original_centroid * 100.0)
                if mape > self.tol: optimized = False

            if optimized:
                break


videoId         = int(sys.argv[1])
frameIndex      = int(sys.argv[2])

manager = VideoDataManager('../../..')
videoData = manager.getVideoData(videoId)
frameListUser3dPosition             = []

for chunkIndex, chunk in enumerate(videoData.getChunks(1)):
    for i in range(len(chunk.tracePositions)):
        frameListUser3dPosition.append(chunk.tracePositions[i])


# print(len(frameListUser3dPosition[frameIndex]))
normalizedData = standardize_data(frameListUser3dPosition[frameIndex])
# print(normalizedData)

# print()
# print()
# print()

kmeans = KMeans(k = 3, random_state = 30, max_iter = 300)
kmeans.fit(normalizedData)

cluster = []

for classification in kmeans.classifications:
    cluster.append([user.idx for  user in kmeans.classifications[classification]])

print(cluster)