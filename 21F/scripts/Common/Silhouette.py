from math import pi
import sys

from Clustering import affinityGeodesic, affinity, getClusters, printMatrix
from KMeans import KMeans
from DBScan import DBScan
from Utilities import populateDistanceMatrix, getSilhouetteScores, standardize_data
from VideoUtil import VideoDataManager

manager = VideoDataManager('../../..')
userCount = 30

affinityMatrix = [[0 for _ in range(userCount)] for _ in range(userCount)]
distanceMatrix = [[0.0 for _ in range(userCount)] for _ in range(userCount)]
scoresGeodesic = [0] * userCount
scoresKMeans = [0] * userCount
scoresDBScan = [0] * userCount

kmeans = KMeans(k = 3, random_state = 30, max_iter = 300)
dbscan = DBScan(0.9, 3)

print('Left to right: geodesic, k-means, DB scan')

calculateGeodesic = True if sys.argv[1] == 'true' else False
calculateKMeans = True if sys.argv[2] == 'true' else False
calculateDBScan = True if sys.argv[3] == 'true' else False

for videoIndex in range(1, 31):
    if videoIndex == 15 or videoIndex == 16:
        continue
    
    videoData = manager.getVideoData(videoIndex)
    videoScoreGeodesic = 0.0
    videoScoreKMeans = 0.0
    videoScoreDBScan = 0.0
    chunkCount = 0

    for chunk in videoData.getChunks(60):
        chunkCount += 1

        if calculateGeodesic:
            affinityGeodesic(chunk, affinityMatrix, pi/5)
            clustersGeodesic = getClusters(affinityMatrix, 40)

        if calculateKMeans or calculateDBScan:
            normalizedTracePositions = [standardize_data(userPositions) for userPositions in chunk.tracePositions]

        if calculateDBScan:
            affinity(normalizedTracePositions, dbscan, affinityMatrix)
            clustersDBScan = getClusters(affinityMatrix, 40)

        if calculateKMeans:
            affinity(normalizedTracePositions, kmeans, affinityMatrix)
            clustersKMeans = getClusters(affinityMatrix, 40)
            
        for userPositions in chunk.tracePositions:
            populateDistanceMatrix(userPositions, distanceMatrix)

            if calculateGeodesic:
                getSilhouetteScores(distanceMatrix, clustersGeodesic, scoresGeodesic)

            if calculateDBScan:
                getSilhouetteScores(distanceMatrix, clustersDBScan, scoresDBScan)

            if calculateKMeans:
                getSilhouetteScores(distanceMatrix, clustersKMeans, scoresKMeans)

        chunkScoreGeodesic = 0.0
        chunkScoreDBScan = 0.0
        chunkScoreKMeans = 0.0
        
        for i in range(userCount):
            chunkScoreGeodesic += scoresGeodesic[i] / len(chunk.tracePositions)
            chunkScoreKMeans += scoresKMeans[i] / len(chunk.tracePositions)
            chunkScoreDBScan += scoresDBScan[i] / len(chunk.tracePositions)

        chunkScoreGeodesic /= userCount
        chunkScoreKMeans /= userCount
        chunkScoreDBScan /= userCount
        
        videoScoreGeodesic += chunkScoreGeodesic
        videoScoreKMeans += chunkScoreKMeans
        videoScoreDBScan += chunkScoreDBScan

        for i in range(userCount):
            scoresGeodesic[i] = 0.0
            scoresKMeans[i] = 0.0
            scoresDBScan[i] = 0.0

    print(f'{videoScoreGeodesic / chunkCount} {videoScoreKMeans / chunkCount} {videoScoreDBScan / chunkCount}')
