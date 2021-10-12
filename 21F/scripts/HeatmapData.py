import array
import math

# Wrapper around a frequency array used to generate a heatmap.
class HeatmapData:
    def __init__(self, width, height, rows, cols):
        self.width = width
        self.height = height
        
        self.row = rows
        self.cols = cols
        
        self.colWidth = width / cols
        self.rowHeight = height / rows
        
        # Creates a 2d array of unsigned longs with row rows and cols columns.
        self.grid = [array.array('L', [0 for j in range(cols)]) for i in range(rows)]

    # Transforms a 3d direction vector into a corresponding 2d point on the map,
    # and increments the frequency value of the grid square containing that point.
    def addPoint(self, x, y, z):
        pitch = math.asin(y)
        yaw = math.atan2(x, z)

        x = ((yaw + math.pi) / (math.pi * 2)) * self.width
        y = ((math.pi / 2 - pitch) / math.pi) * self.height

        xIndex = int(x / self.colWidth)
        yIndex = int(y / self.rowHeight)

        self.grid[yIndex][xIndex] += 1
