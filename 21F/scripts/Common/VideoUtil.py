import csv
import os

from PIL import Image
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

class Video:

    def __init__(self, videoId: int, framesPath: str, tracesPath: str) -> None:
        self.videoId = videoId
        self.framesPath = framesPath     # path to directory containing source frames
        self.tracesPath = tracesPath     # path to directory containing user traces
        
        self._dimensions: Tuple[int, int] = None  # (width, height)
        self._userIds: List[str]          = None  # users associated with traces

    # Get (width, height) of the video.
    def getDimensions(self) -> Tuple[int, int]:
        if self._dimensions == None:
            framePath = f'{self.framesPath}/frame1.jpg'
            with Image.open(framePath) as frame:
                self._dimensions = frame.size

        return self._dimensions

    # Get a list of all users for the video.
    def getUserIds(self) -> List[str]:
        if self._userIds == None:
            self._userIds = [trace[:trace.find('.csv')] for trace in os.listdir(self.tracesPath)]

        return self._userIds

    def getChunks(self, length: int) -> ChunkIterator:
        traceIterators = [TraceIterator(f'{self.tracesPath}/{userId}.csv') for userId in self.getUserIds()]
        return ChunkIterator(traceIterators, length)

class VideoManager:
    
    def __init__(self, baseDir):
        self.baseDir = baseDir
        self.framesPath = f'{baseDir}/Data/VideosData/Videos/SourceFrames'
        self.tracesPath = f'{baseDir}/Data/UserTracesByVideo'

    def getVideo(self, videoId: int):
        return Video(int, f'{self.framesPath}/{videoId}', f'{self.tracesPath}/{videoId}')
