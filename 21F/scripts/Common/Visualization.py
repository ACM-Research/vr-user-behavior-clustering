import cv2
import sys
from VideoUtil import VideoData, VideoDataManager
import VideoUtil as vutil
from Clustering import getClusters, affinityGeodesic, affinity
from math import pi
from time import perf_counter
from Utilities import mapTo2D, cartesianToSpherical, standardize_data
from KMeans import KMeans
from DBScan import DBScan

argc = len(sys.argv)

if argc < 2:
    print('Insufficient args; at least one arg for video ID required.')
    exit()

videoId = int(sys.argv[1])

if argc < 3:
    print('No argument for number of chunks; all chunks will be processed.')
    chunkCount = -1
else:
    chunkCount = int(sys.argv[2])

# Colors are in BGR for some reason
colors = [(0, 0, 255),    # red
          (0, 128, 0),    # green
          (255, 0, 0),    # blue
          (32, 165, 218), # goldenrod
          (0, 0, 139),    # dark red
          (127, 255, 0),  # spring green
          (255, 191, 0),  # deep sky blue
          (0, 140, 255),  # dark orange
          (0, 128, 0),    # olive green
          (128, 128, 0),  # teal
          (255, 0, 255),  # fuchsia
          (130, 0, 75),   # indigo
          (122, 150, 233) # dark salmon
          ] * 3


dotSize = 7
textOffset = dotSize / 2
manager = VideoDataManager('../../..')

videoData = manager.getVideoData(videoId)
print(f'Opening video at {videoData.videoPath}')
videoCapture = cv2.VideoCapture(videoData.videoPath)

if not videoCapture.isOpened():
    print(f'Failed to open video #{videoId}')
    exit()

fps = videoCapture.get(5)
frameSize = (960, 480)
writerGeo = cv2.VideoWriter(f'{manager.visPath}/Geodesic/{videoId}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, frameSize)
writerKmeans = cv2.VideoWriter(f'{manager.visPath}/KMeans/{videoId}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, frameSize)
writerDBSCAN = cv2.VideoWriter(f'{manager.visPath}/DBSCAN/{videoId}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, frameSize)

clustersSet = [[], [], []]
kmeans = KMeans(k = 3, random_state = 30, max_iter = 300)
dbscan = DBScan(pi/10, 3)
userCount = 30
affinityMatrix = [[0 for _ in range(userCount)] for _ in range(userCount)]

for chunkIndex, chunk in enumerate(videoData.getChunks(60)):
    if chunkIndex == chunkCount:
        break

    start = perf_counter()
    affinityGeodesic(chunk, affinityMatrix, pi/10)
    clustersSet[0] = getClusters(affinityMatrix, 40)

    normalizedTracePositions = [standardize_data(userPositions) for userPositions in chunk.tracePositions]

    affinity(normalizedTracePositions, dbscan, affinityMatrix)
    clustersSet[1] = getClusters(affinityMatrix, 40)

    affinity(normalizedTracePositions, kmeans, affinityMatrix)
    clustersSet[2] = getClusters(affinityMatrix, 40)
    print(clustersSet[1])
    
    startFrame = chunk.frameRange[0] + 1

    for i in range(len(chunk.tracePositions)):
        ret, frame = videoCapture.read()
            
        if not ret:
            print('Error reading frame')
            exit()
        
        userPositions = chunk.tracePositions[i]
        frame = cv2.resize(frame, frameSize)
        frames = [frame, frame.copy(), frame.copy()]

        singularClusters = 0
        # Plot all users in all clusters
        for i in range(len(clustersSet)):
            for clusterIndex, cluster in enumerate(clustersSet[i]):
                if len(cluster) < 2:
                    color = (0, 0, 0)
                    singularClusters += 1
                else:
                    color = colors[clusterIndex]
                    
                for userIndex in cluster:
                    positionFloat = mapTo2D(userPositions[userIndex], frameSize)
                    positionInt = (int(positionFloat[0]), int(positionFloat[1]))
                    
                    if userIndex > 9:
                        textLeft = positionInt[0] - 4
                    else:
                        textLeft = positionInt[0] - 2
                            
                    cv2.circle(frames[i], positionInt, 6, color, -1)
                    cv2.putText(frame[i], str(userIndex), (textLeft, positionInt[1] + 2), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (255, 255, 255), 1)

        # Write new video frame
        writerGeo.write(frames[0])
        writerDBSCAN.write(frames[1])
        writerKmeans.write(frames[2])
        
       # cv2.putText(frame, f'{len(clusters) - singularClusters} ({singularClusters})', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        
    end = perf_counter()
    print(f'Processed chunk {chunkIndex} in {end - start}')

cv2.destroyAllWindows()
videoCapture.release()
writer.release()
