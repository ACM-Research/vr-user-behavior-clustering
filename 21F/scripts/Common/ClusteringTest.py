import cv2
from VideoUtil import VideoData, VideoDataManager
import VideoUtil as vutil
from Clustering import getClusters
from math import pi
from Utilities import mapTo2D

colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255,126,0), (187,51,255)] * 6
manager = VideoDataManager('../../..')

videoId = 23
videoData = manager.getVideoData(videoId)
print(f'Opening video at {videoData.videoPath}')
videoCapture = cv2.VideoCapture(videoData.videoPath)

if not videoCapture.isOpened():
    print(f'Failed to open video #{videoId}')
    exit()

fps = videoCapture.get(5)
frameSize = (960, 480)
writer = cv2.VideoWriter(f'{manager.visPath}/{videoId}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, frameSize)

#for chunk in videoData.getChunks(60):
chunks = videoData.getChunks(60)
for i in range(0, 1):
    chunk = next(chunks)
    # Get clusters for current chunk, using distance threshold of pi/10 and affinity of 40 frames.
    clusters = getClusters(chunk, pi/10, 40)    
    startFrame = chunk.frameRange[0] + 1
    
    for i in range(len(chunk.tracePositions)):
        ret, frame = videoCapture.read()
            
        if not ret:
            print('Error reading frame')
            exit()
        
        userPositions = chunk.tracePositions[i]
        frame = cv2.resize(frame, frameSize)
        
        # Plot all users in all clusters
        for cluster in clusters:
            for user in cluster:
                point = mapTo2D(userPositions[user], frameSize)
                cv2.circle(frame, (int(point[0]), int(point[1])), 5, colors[user], -1)

        # Write new video frame
        writer.write(frame)

cv2.destroyAllWindows()
videoCapture.release()
writer.release()
