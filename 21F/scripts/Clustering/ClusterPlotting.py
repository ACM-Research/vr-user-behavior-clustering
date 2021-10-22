import geopy
#import app.env
import math, csv, os, glob
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sympy
from PIL import Image, ImageDraw
import networkx as nx
import cv2



'''
Creating A overarching encompassing dictionary for the entire video.
Each key in this dictionary represents a frame number. Per each frame number,
there exists keys of userIDs with the value (x, y) positions. We use this to
simplify the process of just creating some data structure that holds all the
user positions for each frame all under on dictionary.
When provided a list of clusters and the frame range we want to access our 
data structure, for that frame, grab the userID, color their coordinates based
on what color that userID fell under in the cluster list with. One way is 
for each frame in our frame range, we iterate through Color: IDs values and
plot those userID positions, accessed from our overarching data structure with
the color of the key. We do this until the end of the list in our clusters. 
'''
class DataParser:
    def __init__(self, basedir, videoId): #, rows, cols):
        """ Getting user data paths and frame image paths, opening images, selecting frames, other setup"""
        #self.rows = rows
        #self.cols = cols
        self.usertracepath = f"{basedir}/Data/UserTracesByVideo/{videoId}/"
        self.frameimgs = f"{basedir}/Data/VideosData/Videos/SourceFrames/{videoId}/"
        with Image.open(f"{self.frameimgs}/frame1.jpg") as im:
            self.imagesize = (im.size[0], im.size[1])
        self.importusertraces()
        #self.testFrames = [121, 271, 691, 811, 1111, 1351, 1681]
        #self.videoId = videoId
        #self.frame_dict = {}

    @staticmethod
    def convvec2angl(vector):
        """ Convert vectors to angles (Pitch, Yaw) """
        # ?? Which one is which, and how do the calculations work ??
        phi = math.degrees(math.asin(vector[1]))
        theta = math.degrees(math.atan2(vector[0], vector[2]))
        return theta, phi

    """
        This method in the end take in a frame_list like [60,120] to represent frames 60 to 120.
        It iterates through the frames and converts user traces
    """
    def pos_id_frame(self, frame_list = 1):
        self.frames_dict = {}
        for frame in range(frame_list):
            self.convertusertraces(frame+1)
        return self.frames_dict

    def importusertraces(self):
        """ Imports user traces and converts to a pandas DataFrame """
        self.all_user_traces = []
        user_folders = [trace for trace in os.listdir(self.usertracepath)]
        for user in user_folders:
            userid = user[:user.find('.csv')]
            trace_data = pd.read_csv(f"{self.usertracepath}/{user}")
            trace_rows = trace_data.values

            self.all_user_traces.append((trace_rows, userid))

    def convertusertraces(self, frame):

        # frames_dict has a new key which is the frame
        self.frames_dict[frame] = {}
        for trace_rows, userid in self.all_user_traces:
        
            trace_row = trace_rows[frame - 1]  # Be careful about indexing!!
            arr = [trace_row[5], trace_row[6], trace_row[7]]
            yaw, pitch = self.convvec2angl(arr)
        
       
            x = ((yaw + 180) / 360) * self.imagesize[0]
            y = ((90 - pitch) / 180) * self.imagesize[1]
            pos = (x, y)

            """
                In that frame, for each user, add their position to the dictionary
            """
            self.frames_dict[frame][userid] = pos
    
    

"""
This method takes in a dictionary with keys representing color and the values are a list of 
user IDs. We will color these users position based on their key. The 2nd parameter is a frame
range such as 1-60. 3rd is videoID such as 23. It will construct an object and call a method to
populate the positions of the userIDs for that frame range and return that dictionary. 

frames_dict keys are the frame numbers in our frame range, the values are dictionarys. These
dictionaries key is the userID and value is their (x, y) position. The for loop essentially
loops through each frame in our frames_dict. In my implemenation below I simply am calling 
frames_dict[frame_number] to get the collection of useIDs then for each userID in the for 
loop below I am getting their position with frame_to_IDs[userID][0] & frame_to_IDs[userID][1]

What we need:
What we need is to iterate through each frame in our frames dictionary. Then we need to iterate
through every color in our cluster_color_id. For each color, we need to iterate through the list
of IDs that belong to that color.  Using this userID we want to access the users position in that
frame with someting like x = frames_to_IDs[userID][0] for example for the x value. Then we need
to plot it. 

pseudocode:
    for frame_number in frames:
        for colour in cluster_color_id:
            frame_to_ids = frames[frame_number]
            for userID in cluster_color_id[color]:
                x = frame_to_ids[userID][0]
                y = frame_to_ids[userID][1]
                plot x & y with the color 

"""




def clusterPlotting( cluster_color_id, frame_range, videoID):
    dp = DataParser("C:/Users/salma/vr-user-behavior-clustering",videoID)

    # for now not supplying the frame range just want to see if we can plot user positions for one frame
    frames_dict = dp.pos_id_frame()
    print(frames_dict.keys())
    for frame_number in frames_dict.keys():
        frame_to_IDs = frames_dict[frame_number]
        for userID in frame_to_IDs.keys():
            x = frame_to_IDs[userID][0]
            y = frame_to_IDs[userID][1]
            print(f"{userID} X: {x} y: {y}")
            
    return True
    
e = clusterPlotting({"red":[1,3,3]},1,23)