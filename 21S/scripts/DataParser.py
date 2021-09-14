import math
import os

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageDraw
import seaborn as sb
from pathlib import Path

import cv2
""" 
    Hey guys, welcome to the Data Parser class. A lot of stuff here you WON'T need, but I've tried to label
  everything you will need: 

  - Anything with #IMPORTANT is, well, important. 
  - VERY IMPORTANT denotes something that is crucial to understand.
  - ?? ... ?? which denotes a question that you ought to think about and figure out the answer to 
       in order to keep up with the content. 
  - !! ... !! denotes a question (or set of questions) that you absolute need to know the answer to 
      in order to understand how the program works.

    I would make sure that you know how to replicate these functions yourself. A lot of this code will stay
 the same throughout the semester, but there will be tweaks that you'll (likely) have to make, and ideally
 you want to make those without everything breaking. Other than that, feel free to ask me questions on Slack
 or during our meeting on Friday!
 """


class DataParser:

    # IMPORTANT
    def __init__(self, basedir, videoId, rows, cols):
        """ Getting user data paths and frame image paths, opening images, selecting frames, other setup"""
        self.rows = rows
        self.cols = cols
        self.usertracepath = f"{basedir}/Data/UserTracesByVideo/{videoId}/"
        self.frameimgs = f"{basedir}/Data/VideosData/Videos/SourceFrames/{videoId}/"
        with Image.open(f"{self.frameimgs}/frame1.jpg") as im:
            self.imagesize = (im.size[0], im.size[1])
        self.importusertraces()
        self.testFrames = [121, 271, 691, 811, 1111, 1351, 1681]
        self.videoId = videoId

    # NOT IMPORTANT
    def createControlImages(self):
        """ Creates images without any compression (for comparsion) """
        controlPath = f'{os.getcwd()}/21S/data/control/{self.videoId}'
        if not os.path.isdir(controlPath):
            frames = [f'{self.frameimgs}/frame{frame}.jpg' for frame in self.frameList()]
            Path(controlPath).mkdir(777, parents=True, exist_ok=True)
            for frame in frames:
                imgPath = f'{frame}'
                img = Image.open(frame)
                img.save(imgPath, quality=95)

    # IMPORTANT
    def frameList(self):
        """ Retrieve a list of frame numbers """
        framenums = sorted([int(frame[5:-4]) for frame in os.listdir(self.frameimgs)])
        return framenums

    # VERY IMPORTANT
    @staticmethod
    def convvec2angl(vector):
        """ Convert vectors to angles (Pitch, Yaw) """
        # ?? Which one is which, and how do the calculations work ??
        phi = math.degrees(math.asin(vector[1]))
        theta = math.degrees(math.atan2(vector[0], vector[2]))
        return theta, phi

    # IMPORTANT
    def getFrame(self, id):
        """ Gets a frame image given its id """
        frameName = 'frame{}.jpg'.format(id)
        img = cv2.imread(os.path.join(self.frameimgs, frameName))
        return img

    # VERY IMPORTANT - Understand what a Pandas DataFrame is and how to use it
    def importusertraces(self):
        """ Imports user traces and converts to a pandas DataFrame """
        self.all_user_traces = []
        user_folders = [trace for trace in os.listdir(self.usertracepath)]
        for user in user_folders:
            userid = user[:user.find('.csv')]
            trace_data = pd.read_csv(f"{self.usertracepath}/{user}")
            trace_rows = trace_data.values
            self.all_user_traces.append((trace_rows, userid))

    # VERY IMPORTANT
    def convertusertraces(self, frame):
        # draw user trace points
        self.usertraces = []
        # ?? What is the purpose of splitting image into columns ??
        colwidth = self.imagesize[0] / self.cols
        rowheight = self.imagesize[1] / self.rows
        for trace_rows, userid in self.all_user_traces:

            trace_row = trace_rows[frame - 1]  # Be careful about indexing!!
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
            self.usertraces.append((userid, frame, (x_index, y_index)))

    # NOT IMPORTANT
    def convertTracesForAllUsers(self):
        traces_per_user = {}
        for user in self.all_user_traces:
            traces_per_user[user[1]] = self.convertTracesPerUser(user)
        return traces_per_user

    # NOT IMPORTANT
    def convertTracesPerUser(self, user):
        traces = []
        colwidth = self.imagesize[0] / self.cols
        rowheight = self.imagesize[1] / self.rows
        trace_rows, userid = user
        for frame in self.frameList():
            trace_row = trace_rows[frame - 1]  # Be careful about indexing!!
            arr = [trace_row[5], trace_row[6], trace_row[7]]
            x, y = self.convvec2angl(arr)
            x = ((x + 180) / 360) * self.imagesize[0]
            y = ((90 - y) / 180) * self.imagesize[1]
            x_index = int(x / colwidth)
            y_index = int(y / rowheight)
            traces.append((frame, (x_index, y_index)))
        return traces

    # NOT IMPORTANT
    def createControlVideo(self, fps, videoName='Control.avi'):
        frames = [f'{self.frameimgs}/frame{frame}.jpg' for frame in self.frameList()]
        out = cv2.VideoWriter(videoName, cv2.VideoWriter_fourcc(*'DIVX'), fps, self.imagesize)
        print(f'Creating {videoName} video')
        numofframes = len(frames)
        progress = 0
        for frame in frames:
            img = cv2.imread(frame)
            out.write(img)
            progress += (100 / numofframes)
            print("Progress " + str(int(progress)) + "%", end='\r', flush=True)
        out.release()
        print()


#Will need to split up source videos into frames once ML is used