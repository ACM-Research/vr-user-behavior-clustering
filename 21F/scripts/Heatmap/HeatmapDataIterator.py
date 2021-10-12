from DataManager import DataManager
from HeatmapData import HeatmapData

# Iterating over a HeatmapDataIterator returns a HeatmapData instance for each frame in frameList
# for the video specified by videoId. frameList is assumed to be sorted and to have no duplicates.
class HeatmapDataIterator:
    def __init__(self, dataManager, videoId, frameList, rows, cols):
        self.rows = rows
        self.cols = cols

        self.dimensions = dataManager.getVideoDimensions(videoId)
        self.vectors = dataManager.getVectors(videoId, frameList)
        self.frameIndex = 0
        
    def __iter__(self):
        return self;

    def __next__(self):
        if self.frameIndex >= len(self.vectors):
            raise StopIteration
        
        heatmapData = HeatmapData(self.dimensions[0], self.dimensions[1], self.rows, self.cols)
        
        for vector in self.vectors[self.frameIndex]:
            heatmapData.addPoint(vector[0], vector[1], vector[2])

        self.frameIndex += 1
        return heatmapData
