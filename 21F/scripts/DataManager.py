import csv
import os
from PIL import Image

# Utility class for reading, caching, and parsing various video data.
class DataManager:
    # Dictionary of video dimensions.
    # Keys are video IDs, values are (width, height) tuples.
    videoDimensions = {}
    
    def __init__(self, baseDir):
        self.baseDir = baseDir
        self.sourceFramesPath = f'{baseDir}/Data/VideosData/Videos/SourceFrames/'
        self.tracesPath = f'{baseDir}/Data/UserTracesByVideo/'

    # Get a (width, height) tuple for a particular video.
    def getVideoDimensions(self, videoId):
        if videoId in self.videoDimensions:
            return self.videoDimensions[videoId]
        else:
            frame = f'{self.sourceFramesPath}/{videoId}/frame1.jpg'
            with Image.open(frame) as im:
                self.videoDimensions[videoId] = im.size
                return im.size

    # Get a list of the file paths of traces for a particular video.
    def getTraces(self, videoId):
        tracesDir = f'{self.tracesPath}/{videoId}/'
        return [tracesDir + name for name in os.listdir(tracesDir)]

    # Get a list of direction vectors for each frame in frameList for a
    # all the traces for a particular video. Returns a 2d list of
    # (x, y, z) tuples, where each row is a list of direction vectors
    # from every trace for one frame. The ith row corresponds to the
    # ith frame in frameList. frameList is assumed to be sorted and
    # to have no duplicates.
    def getVectors(self, videoId, frameList):
        vectors = [[] for i in range(len(frameList))]
        lastFrame = frameList[len(frameList) - 1]
        
        for trace in self.getTraces(videoId):
            with open(trace) as traceCSV:
                reader = csv.reader(traceCSV, quoting=csv.QUOTE_NONNUMERIC)
                i = 0
                for j in range(lastFrame + 1):
                    row = next(reader)
                    if j == frameList[i]:
                        vectors[i].append((row[5], row[6], row[7]))
                        i += 1
                        
        return vectors
