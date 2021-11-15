import csv
import cv2
import os

from typing import List, Tuple
from Utilities import Vector2, Vector3

# Classes for working with video data.
# TraceIterator - iterates over the positions, frame-by-frame, in a particular trace file.
# Chunk - user trace positions for a contigious set of frames in a video.
# ChunkIterator - iterates over chunks in a video.
# Video - represents a video and its corresponding user trace data.
# VideoManager - gets Video object for a particular video id.

class TraceIterator:
    
    def __init__(self, tracePath) -> None:
        self.traceFile = open(tracePath, 'r')
        self.reader = csv.reader(self.traceFile, quoting=csv.QUOTE_NONNUMERIC)

    def __iter__(self):
        return self
    
    # Returns the position (x, y, z) in the next frame.
    def __next__(self) -> Vector3:
        if self.reader == None:
            raise StopIteration

        # Try to get the next row in the CSV file.
        try:
            row = next(self.reader)
            return (row[5], row[6], row[7])
        except StopIteration:
            self.traceFile.close()
            self.reader = None
            raise StopIteration

class Chunk:

    def __init__(self, tracePositions: List[List[Vector3]], frameRange: range):
        self.tracePositions = tracePositions    # tracePositions[i][j] corresponds to the position of user j during the ith frame
        self.frameRange = frameRange
        self.userCount = len(tracePositions[0])
        
    # Returns a list of silhouette scores for each user, where the nth element
    # in the list is the average silhouette score over the chunk for user n.
    def getSilhouetteScores(clusters):
        scores: List[float] = [0.0 for _ in range(self.userCount)]
        getS

        frameCount = len(tracePositions)
        for i in range(len(scores)):
            scores[i] = scores[i] / frameCount

        return scores

class ChunkIterator:

    def __init__(self, traceIterators: List[TraceIterator], chunkLength: int) -> None:
        self.traceIterators = traceIterators     # trace iterators for each user
        self.chunkLength = chunkLength           # number of frames per chunk
        self.currentFrame = 0

    def __iter__(self):
        return self
    
    def __next__(self) -> Chunk:
        frameRange = range(self.currentFrame, self.currentFrame + self.chunkLength)
        tracePositions: List[List[Vector3]] = []
        
        for i in frameRange:
            tracePositions.append([next(traceIterator) for traceIterator in self.traceIterators])

        chunk = Chunk(tracePositions, frameRange)
        self.currentFrame += self.chunkLength
        return chunk

class VideoData:

    def __init__(self, videoId: int, videosPath: str, tracesPath: str):
        self.videoId = videoId
        self.videoPath = f'{videosPath}/Source/{videoId}.mp4'
        self.tracesPath = f'{tracesPath}/{videoId}'
        self.framesPath = f'{videosPath}/SourceFrames/{videoId}'
        
        self._dimensions: Tuple[int, int] = None  # (width, height)
        self._userIds: List[str]          = None  # users associated with traces

    # Get a list of all users for the video.
    def getUserIds(self) -> List[str]:
        if self._userIds == None:
            self._userIds = [trace[:trace.find('.csv')] for trace in os.listdir(self.tracesPath)]

        return self._userIds

    def getChunks(self, length: int) -> ChunkIterator:
        traceIterators = [TraceIterator(f'{self.tracesPath}/{userId}.csv') for userId in self.getUserIds()]
        return ChunkIterator(traceIterators, length)

    def getFrameImage(self, frameNumber: int):
        return cv2.imread(f'{self.framesPath}/frame{frameNumber}.jpg', cv2.IMREAD_COLOR)

class VideoDataManager:
    
    def __init__(self, baseDir):
        self.baseDir = baseDir
        self.videosPath = f'{baseDir}/Data/VideosData/Videos'
        self.tracesPath = f'{baseDir}/Data/UserTracesByVideo'
        self.visPath = f'{baseDir}/21F/Visualizations'

    def getVideoData(self, videoId: int):
        return VideoData(videoId, self.videosPath, self.tracesPath)
