import app.env
import math, csv, os, glob
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List
from pathlib import PureWindowsPath
from pathlib import Path

env = app.env

class DataParser:
    def __init__(self, baseDir, videoID, numCols, numRows) -> None:
        self.csvPath = f"{baseDir}/resources/UserTracesByVideo/{videoID}/"
        self.videoID = videoID
        self.numCols = numCols
        self.numRows = numRows
        self.allUserID = DataParser.find_csv_filenames(self.csvPath)
        self.frameImgWidth = env.IMAGE_WIDTH
        self.frameImgHeigth = env.IMAGE_HEIGHT
        self.userTraces = []
        self.heatmapArray = None

        # print(self.frameImgHeigth)
        # print(self.frameImgWidth)
        # for id in self.allUserID:
        #     print(id) 

    @staticmethod
    def convvec2angl(vector):
        phi     = math.degrees(math.asin(vector[1]))
        theta   = math.degrees(math.atan2(vector[0], vector[2]))
        return (theta, phi)

    @staticmethod
    def find_csv_filenames(path_to_dir, suffix=".csv"):
        path_to_dir = Path(path_to_dir)
        
        os.chdir(path_to_dir)
        for file in glob.glob('*{}'.format(suffix)):
            yield file.replace(suffix, "")

    @staticmethod
    def csvRowReader(path_to_dir, rowIndex, fileName, suffix=".csv"):
        path_to_dir = Path(f"{path_to_dir}/{fileName}{suffix}")
        with open(path_to_dir, "r") as file:
            csv_reader = csv.reader(file)
            rows = list(csv_reader)
            return rows[rowIndex]

    def collectHeatDiagramLocations(self, frameNumber):
        # draw user trace points
        colwidth = self.frameImgWidth / self.numCols
        rowheight = self.frameImgHeigth / self.numRows
        
        for userid in self.allUserID:
            frameRow = DataParser.csvRowReader(self.csvPath, frameNumber - 1, userid)
            _3dVector = [float(frameRow[5]), float(frameRow[6]), float(frameRow[7])]
            
            # convert 3d vector to 2d vector
            (yaw, pitch) = self.convvec2angl(_3dVector)
            x = ((yaw + 180) / 360) * self.frameImgWidth
            y = ((90 - pitch) / 180) * self.frameImgHeigth

            x_index = int(x / colwidth)
            y_index = int(y / rowheight)
            self.userTraces.append((userid, frameNumber, (x_index, y_index)))

        print(self.userTraces)

    def loadHeatmapData(self):
        self.heatmapArray = np.empty(shape=(self.numRows, self.numCols))
        self.heatmapArray.fill(0)
        
        # # row 2 col 3
        # x[3-1][2-1] = x[3-1][2-1] + 1
        
        for user in self.userTraces:
            self.heatmapArray[user[2][1]][user[2][0]] = self.heatmapArray[user[2][1]][user[2][0]] + 1

        print(self.heatmapArray)

    def loadHeatmap(self):
        ax = sns.heatmap(self.heatmapArray)
        plt.show()
        