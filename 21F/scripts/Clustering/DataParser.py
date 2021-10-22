import geopy
#import app.env
import math, csv, os, glob
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sympy

from typing import List
from pathlib import PureWindowsPath
from pathlib import Path
from geopy.distance import great_circle
from geopy.distance import EARTH_RADIUS



class DataParser:
    def __init__(self, baseDir, videoID, numCols, numRows) -> None:
        self.csvPath = f"{baseDir}/Data/UserTracesByVideo/{videoID}/"
        self.videoID = videoID
        self.numCols = numCols
        self.numRows = numRows
        self.allUserID = DataParser.find_csv_filenames(self.csvPath)
        self.frameImgWidth = 3840
        self.frameImgHeigth = 1920
        self.userTraces = []
        self.heatmapArray = None
        self.adjacencyArray = None

        # print(self.frameImgHeigth)
        # print(self.frameImgWidth)
        # for id in self.allUserID:
        #     print(id) 

    def getUserID(self):
        return self.allUserID
    @staticmethod
    def find_csv_filenames(path_to_dir, suffix=".csv"):
        path_to_dir = Path(path_to_dir)
        fileNames = []
        os.chdir(path_to_dir)
        for file in glob.glob('*{}'.format(suffix)):
            fileNames.append(file.replace(suffix, ""))

        return fileNames 

    @staticmethod
    def csvRowReader(path_to_dir, rowIndex, fileName, suffix=".csv"):
        path_to_dir = Path(f"{path_to_dir}/{fileName}{suffix}")
        with open(path_to_dir, "r") as file:
            csv_reader = csv.reader(file)
            rows = list(csv_reader)
            return rows[rowIndex]

    @staticmethod
    def asCartesian3d(rthetaphi):
        #takes list rthetaphi (single coord)
        r       = rthetaphi[0]
        theta   = rthetaphi[1] * sympy.pi/180 # to radian
        phi     = rthetaphi[2] * sympy.pi/180
        x       = r * sympy.sin(theta) * sympy.cos(phi)
        y       = r * sympy.sin(theta) * sympy.sin(phi)
        z       = r * sympy.cos(theta)
        return [x, y, z]

    @staticmethod
    def asSpherical(xyz):
        #takes list xyz (single coord)
        x       = xyz[0]
        y       = xyz[1]
        z       = xyz[2]
        r       = sympy.sqrt(x*x + y*y + z*z)
        theta   = sympy.acos(z/r)  * 180 / sympy.pi #to degrees
        phi     = sympy.atan2(y,x) * 180 / sympy.pi
        return [r, theta, phi]

    @staticmethod
    def asGeographic(xyz):
        #takes list xyz (single coord)
        x           = xyz[0]
        y           = xyz[1]
        z           = xyz[2]
        r           = sympy.sqrt(x*x + y*y + z*z)
        latitude    = sympy.asin(z/r)  * 180 / sympy.pi #to degrees
        longitude   = sympy.atan2(y,x) * 180 / sympy.pi
        return [r, latitude, longitude]

    @staticmethod
    def convvec2angl(xyz):
        phi     = math.degrees(math.asin(xyz[1]))
        theta   = math.degrees(math.atan2(xyz[0], xyz[2]))
        return (theta, phi)

    @staticmethod
    def calculateGeodesic(rlatlong_1, rlatlong_2):
        pointA = (rlatlong_1[1], rlatlong_1[2])
        pointB = (rlatlong_2[1], rlatlong_2[2])
        return great_circle(pointA, pointB).km / EARTH_RADIUS # convert to radian

    def collectAdjacencyMatrix(self, frameNumber, threshold = sympy.pi/10):
        numberOfUser = len(self.allUserID)
        self.adjacencyArray = np.empty(shape=(numberOfUser,numberOfUser))
        self.adjacencyArray.fill(0)
        
        rowIndex = 0
        colIndex = 0

        for useridRow in self.allUserID:
            frameRow_useridRow = DataParser.csvRowReader(self.csvPath, frameNumber - 1, useridRow)
            xyz_useridRow = [float(frameRow_useridRow[5]), float(frameRow_useridRow[6]), float(frameRow_useridRow[7])]
            rlatlong_useridRow = DataParser.asGeographic(xyz_useridRow)

            colIndex = 0
            for useridCol in self.allUserID:
                frameRow_useridCol = DataParser.csvRowReader(self.csvPath, frameNumber - 1, useridCol)
                xyz_useridCol = [float(frameRow_useridCol[5]), float(frameRow_useridCol[6]), float(frameRow_useridCol[7])]
                rlatlong_useridCol = DataParser.asGeographic(xyz_useridCol)

                # print(DataParser.calculateGeodesic(rlatlong_useridRow, rlatlong_useridCol))
                if float(DataParser.calculateGeodesic(rlatlong_useridRow, rlatlong_useridCol)) <= float(threshold):
                    self.adjacencyArray[rowIndex, colIndex] = 1

                colIndex = colIndex + 1

            rowIndex = rowIndex + 1

        return (self.adjacencyArray)

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
dataP = DataParser("C:/Users/salma/vr-user-behavior-clustering",1,40,80)
print(dataP.collectAdjacencyMatrix(60))