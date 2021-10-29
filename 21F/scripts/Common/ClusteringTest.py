import VideoUtil as vutil
from Clustering import getClusters
from math import pi
# Test file demonstrating getting video data.

videoManager = vutil.VideoManager('../../..')
print('Video #23')
video = videoManager.getVideo(23)

print('Frames path: \'{video.framesPath}\'')

print('Traces path: \'{video.tracesPath}\'')

print('User ids:')
print(video.getUserIds())

#print("Dimensions:")
#print(video.getDimensions())

chunks = video.getChunks(30)
chunk = next(chunks)

print('Clusters for first chunk:')

# Get cluseters for current chunk, using distance threshold of pi/10 and affinity of 10 frames.
print(getClusters(chunk, pi/10, 10))

# Iterate over first five chunks only, and print the position of the first user in the first frame of each chunk.
#for i in range(0, 5):
#    chunk = next(chunks)
#    print(chunk.tracePositions[0][0])    
