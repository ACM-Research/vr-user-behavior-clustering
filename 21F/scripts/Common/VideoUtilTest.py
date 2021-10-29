import VideoUtil as vutil
from Clustering import getClusters
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
print(getClusters(chunk, 0.45, 10))

# Iterate over first five chunks only, and print the position of the first user in the first frame of each chunk.
#for i in range(0, 5):
#    chunk = next(chunks)
#    print(chunk.tracePositions[0][0])    