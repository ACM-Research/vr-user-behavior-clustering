from app.DataParser import DataParser
import os
from pathlib import Path
from pathlib import PureWindowsPath

parser = DataParser(os.getcwd(), 23, 80, 40)

# path = r"C:\Users\Thinh Nguyen\OneDrive\_1_Fall2021\ACM\Research\vr-user-behavior\main\resources\UserTracesByVideo\1"
# DataParser.csvRowReader(path, 0, "0Z4VWJ")

# parser.collectHeatDiagramLocations(1)
# parser.loadHeatmapData()
# parser.loadHeatmap()

print(parser.collectAdjacencyMatrix(30))