import sys, random
import numpy as np
from typing import Tuple, List
from queue import Queue
from Utilities import geoDistance

class DBScan:
    def __init__(self, Eps : float, MinPt : int):
        self.core = -1
        self.border = -2
        self.Eps = Eps
        self.MintPt = MinPt

    def get_neighbor(self, userPointList : list, sample_idx):
        neighbors = []
        curUser = userPointList[sample_idx]

        for usrIdx, usrVal in enumerate(userPointList):            
            if (usrIdx != sample_idx):    
                # Geodesic distance
                geodesic_distance = geoDistance(usrVal.location, curUser.location)
                if geodesic_distance < self.Eps:
                    neighbors.append(usrIdx)
        
        return neighbors

    def fit(self, userPointList : list):
        # initialize all points as outliers
        self.point_label = [0] * len(userPointList)
        point_count = []

        # initilize list for core/border points
        core = []
        border = []

        # print(point_label)
        
        # Find the neighbours of each individual point
        for usrIdx, usrVal in enumerate(userPointList):
            point_count.append(self.get_neighbor(userPointList, usrIdx))

        # print(point_count)

        # Find all the core points, border points and outliers
        for usrIdx in range(len(point_count)):
            if (len(point_count[usrIdx]) >= self.MintPt):
                self.point_label[usrIdx] = self.core
                core.append(usrIdx)
            else:
                border.append(usrIdx)

        for i in border:
            for j in point_count[i]:
                if j in core:
                    self.point_label[i] = self.border
                    break
        
        # Assign points to a cluster
        self.cluster = 1

        # Here we use a queue to find all the neighbourhood points of a core point and find the indirectly reachable points
        # We are essentially performing Breadth First search of all points which are within Epsilon distance for each other
        for i in range(len(self.point_label)):
            q = Queue()
            if (self.point_label[i] == self.core):
                self.point_label[i] = self.cluster
                for x in point_count[i]:
                    if(self.point_label[x] == self.core):
                        q.put(x)
                        self.point_label[x] = self.cluster
                    elif(self.point_label[x] == self.border):
                        self.point_label[x] = self.cluster
                while not q.empty():
                    neighbors = point_count[q.get()]
                    for y in neighbors:
                        if (self.point_label[y] == self.core):
                            self.point_label[y] = self.cluster
                            q.put(y)
                        if (self.point_label[y] == self.border):
                            self.point_label[y] = self.cluster
                self.cluster += 1  # Move on to the next cluster
        
        # return self.point_label, self.cluster #label for each userIdx and nunber of cluster

    def getCluster(self) -> List:
        clusterArray = [[] for i in range(self.cluster)]
        for userIdx, label in enumerate(self.point_label):
            clusterArray[label].append(userIdx)

        return clusterArray
