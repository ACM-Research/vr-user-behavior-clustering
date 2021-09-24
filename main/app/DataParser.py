import app.env
import math, csv, os, glob
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
    def csvDictReader(path_to_dir, fileName,suffix=".csv"):
        path_to_dir = Path(f"{path_to_dir}/{fileName}{suffix}")
        with open(path_to_dir, "r") as f:
            reader = csv.DictReader(f)
            a = list(reader)
            print(a)

    @classmethod
    def convertUserTraces(self, frameNumber):
        # draw user trace points
        self.usertraces = []
        colwidth = self.frameImgWidth / self.numCols
        rowheight = self.frameImgHeigth / self.numRows
        
        for userid in self.allUserID:

            trace_row = frameNumber - 1
            arr = [trace_row[5], trace_row[6], trace_row[7]]
            yaw, pitch = self.convvec2angl(arr)
            """ 
            !! 
            How does the calculation work? 
            What is x, y here compared to x, y, z in the arr vector? 
            Why do we need this value? 
            !! 
            """
            x = ((yaw + 180) / 360) * self.imagesize[0]
            y = ((90 - pitch) / 180) * self.imagesize[1]

            # ?? Why might parsing the x, y values into indices here be useful ??
            x_index = int(x / colwidth)
            y_index = int(y / rowheight)
            self.usertraces.append((userid, frameNumber, (x_index, y_index)))