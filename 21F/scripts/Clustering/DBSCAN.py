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
  
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

def dbscan(distanceMatrix, epsilon=20, min_samples=1):

    X = distanceMatrix
    epsilon = 20
    min_samples = 1

    # DBSCAN with epsilon val provided and min_samples provided
    # .fit(distanceMatrix) for to apply DBSCAN on THOSE points
    db = DBSCAN(eps=epsilon, min_samples=min_samples).fit(X)
    print(db)
    labels = db.labels_
    print(labels)

    # prints clusters
    no_clusters = len(np.unique(labels) )
    # outliers have value -1, so below prints number of those
    no_noise = np.sum(np.array(labels) == -1, axis=0)

    # silhoutte score
    #print(silhouette_score(X,labels))
    print('Estimated no. of clusters: %d' % no_clusters)
    print('Estimated no. of noise points: %d' % no_noise)

    # Generate scatter plot for training 
    #def mapColor(x):
    #    col = {-1:"#000000",0:"#7d08d1" ,1:"#3b4cc0", 2:"#b40426",3:"#8bd108",4:"#a19427",5:"#10134d"}
    #    if x in col:
    #        return col[x]
    #    else:
    #        return "#ff6bd3"
    #colors = list(map(mapColor, labels))
    #plt.scatter(X[:,0], X[:,1], c=colors, marker="o", picker=True)
    #plt.title('Two clusters with data')
    #plt.xlabel('Axis X[0]')
    #plt.ylabel('Axis X[1]')
    #plt.show()

