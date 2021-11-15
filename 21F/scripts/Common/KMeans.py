import sys, random
import numpy as np
from typing import List

from numpy.ma.core import default_fill_value

from VideoUtil import VideoData, VideoDataManager
from Utilities import Vector3, geoDistance, UserDataPoint

class KMeans:
    def __init__(self, k=2, tol=0.01, random_state = None, max_iter=300):
        if random_state is not None: random.seed(random_state)
        self.k = k
        self.tol = tol
        self.max_iter = max_iter

    def fit(self, userPointList : list):
        self.centroids = random.sample(userPointList, self.k)
        
        for i in range(self.max_iter):
            self.classifications = {}

            for i in range(self.k):
                self.classifications[i] = []

            for userPoint in userPointList:
                geodesicDistances = [geoDistance(userPoint.location, centroid.location) for centroid in self.centroids]
                classification = geodesicDistances.index(min(geodesicDistances))
                self.classifications[classification].append(userPoint)

            prev_centroids = self.centroids

            for classification in self.classifications:
                locationsList = [pos.location for pos in self.classifications[classification]]
                self.centroids[classification] = UserDataPoint(classification, np.average(locationsList,axis=0))

            optimized = True

            for idx, value in enumerate(self.centroids):
                original_centroid = np.array(prev_centroids[idx].location)
                current_centroid = np.array(value.location)
                
                # mape = np.mean(np.abs(original_centroid - original_centroid) / original_centroid) * 100
                mape = np.sum((current_centroid - original_centroid) / original_centroid * 100.0)
                if mape > self.tol: optimized = False

            if optimized:
                break
    
    def getCluster(self):
        cluster = []
        for classification in self.classifications:
            cluster.append([user.idx for user in self.classifications[classification]])
        return cluster
