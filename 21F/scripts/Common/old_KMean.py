import sys

from sklearn import cluster
from VideoUtil import VideoData, VideoDataManager
from Utilities import mapTo2D, cartesianToSpherical

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

NUMBER_OF_CLUSTER = 0

def create_clusters(numberOfUser, points):
    cluster = []
    bestSilhouetteScore = -1.0
    optimizedNumberOfCluster = -1
    silhouette_coefficients = []

    kmeans_kwargs = {
        "init" : "random",
        "n_init" : 10,
        "max_iter" : 300,
        "random_state" : 42
    }
    
    # calculate optimized number of clusters
    for k in range(2, numberOfUser):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(points)
        score = silhouette_score(points, kmeans.labels_)
        silhouette_coefficients.append(score)
        
        if (score > bestSilhouetteScore):
            bestSilhouetteScore = score
            optimizedNumberOfCluster = k
            optimizedClusterLabels = kmeans.labels_
    
    # print(optimizedNumberOfCluster)

    # kmeans = KMeans(**kmeans_kwargs).fit(points)

    for label in optimizedClusterLabels : cluster.append(label)
    return (optimizedNumberOfCluster, cluster)

videoId         = int(sys.argv[1])
frameIndex      = int(sys.argv[2])

frameSize = (720, 360)

manager = VideoDataManager('../../..')
videoData = manager.getVideoData(videoId)
frameListUserPosition = []
frameListUser2DPosition = []

for chunkIndex, chunk in enumerate(videoData.getChunks(1)):
    for i in range(len(chunk.tracePositions)):
        frameListUserPosition.append(chunk.tracePositions[i])

for frame in frameListUserPosition:
    list2Dcoords = []
    for userPos in frame:
        positionFloat = mapTo2D(userPos, frameSize)
        positionFloatArray = [positionFloat[0], positionFloat[1]]
        list2Dcoords.append(positionFloatArray)

    frameListUser2DPosition.append(list2Dcoords)

# standardize data before cluster
scaled_2dposition = StandardScaler().fit_transform(frameListUser2DPosition[frameIndex])

# clusterData = create_clusters(len(videoData.getUserIds()), frameListUser2DPosition[frameIndex])
clusterData = create_clusters(len(videoData.getUserIds()), scaled_2dposition)

clusterArray = [[] for i in range(clusterData[0])]

for userIndex in range(0, len(videoData.getUserIds())):
    clusterArray[clusterData[1][userIndex]].append(userIndex)

print(clusterArray)

# plt.style.use("fivethirtyeight")
# plt.plot(range(2, len(videoData.getUserIds())), silhouette_coefficients)
# plt.xticks(range(2, len(videoData.getUserIds())))
# plt.xlabel("Number of Clusters")
# plt.ylabel("Silhouette Coefficient")
# plt.show()