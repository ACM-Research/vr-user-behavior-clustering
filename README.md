# VR User Behavior Clustering

![poster](C:\Users\A Yan\Documents\UTD\2021_fall\acm-research\vr-user-behavior-clustering\Images\poster.jpg)

## Motivation

Streaming 360-degree videos has high bandwidth requirements owing to the high resolutions (4k or higher) necessary to deliver a satisfactory viewing experience in VR. During video playback, many users may tend to focus on the same areas within a video, known as *regions of interest*. Video content delivery can be optimized by rendering only these regions at high resolution while reducing resolution elsewhere, thus reducing bandwidth usage while maintaining an acceptable viewing experience.

## **Introduction**

Identifying regions of interest requires analyzing the viewing behaviors of many users. Since users may exhibit diverse viewing behaviors, it is useful to group users with *similar* viewing behaviors together, and tailor video content delivery for each group individually, rather than adopting a one-size-fits-all-approach. We refer to such groups of users as *clusters*.

There are many ways of identifying users with similar viewing behavior. We adopt an approach based on *viewport overlap*: the greater the overlap between the field-of-views, or *viewports* of two users, the more likely it is that they are looking at the same area of a video.

We evaluate the efficacy of three different methods of determining whether users are similar based on their viewport overlap:

- K-means clustering
- DBSCAN clustering
- Geodesic distance

## Hypothesis

Methods for determining user similarity that take into account user viewport *density* can effectively identify distinct groups of users with similar behavior.

## Method

1. Find users with similar viewports using each method for determining similarity
2. Group users which are similar for a certain time interval into clusters
3. Evaluate the quality of each cluster

Using this method, we analyzed 28 different 360-degree videos, categorized by the type of camera movement and number of moving objects present in each video.

### Identifying Similar Users

#### Approximating Viewport Overlap

Calculating the exact area of the geometric overlap between viewports is complex. We approximated the amount of overlap between two viewports by the shortest arc length between the centers of those viewports, known as the *geodesic distance*.

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Illustration_of_great-circle_distance.svg/1200px-Illustration_of_great-circle_distance.svg.png" style="zoom:20%;" />

#### Overview

|                   | Two users are similar during a video frame if . . .          |
| ----------------- | ------------------------------------------------------------ |
| K-means           | . . . their viewport centers belong to the same K-means cluster. |
| DBSCAN            | . . . their viewport centers belong to the same DBSCAN cluster. |
| Geodesic distance | . . . their geodesic distance between their viewport centers is within a certain distance threshold. |

#### K-means Clustering

K-means clustering is a popular and fast clustering algorithm that partitions data points into a fixed number of clusters *k*. It aims to minimize the distance between points in a cluster and the *centroid* of the cluster. We used *k* = 3 clusters.

<img src="C:\Users\A Yan\Documents\UTD\2021_fall\acm-research\vr-user-behavior-clustering\Images\kmeans.png" alt="kmeans" style="zoom:50%;" />

#### DBSCAN

Density-Based Spatial Clustering of Applications with Noise (DBSCAN) defines clusters as regions of high data point density, consisting of tightly-packed *core* points and sparser *non-core* points. DBSCAN allows for a variable number of clusters of varying size, and excludes outlier points.

<img src="C:\Users\A Yan\Documents\UTD\2021_fall\acm-research\vr-user-behavior-clustering\Images\dbscan.png" alt="dbscan" style="zoom:60%;" />

### Clustering Users

Frame-by-frame analyses alone are insufficient to determine whether users exhibit similar behavior or not - that requires analyzing user behavior over time.

![clustering](C:\Users\A Yan\Documents\UTD\2021_fall\acm-research\vr-user-behavior-clustering\Images\clustering.png)

We split videos into 60-frame time intervals called *chunks*, and grouped users who were similar to one another for 60% of a chunk into the same cluster, thus obtaining a set of clusters for each video chunk.

### Evaluating Cluster Quality

Intuitively, the denser a cluster is, the greater the viewport overlap is between users in the cluster, and the more likely it is that users in the cluster exhibit similar behavior.



# OLD README BELOW

# VR User Behavior Clustering

ACM Research Fall 2021

## Background

VR videos have massive storage and streaming requirements in order to perform as well as modern day 2D videos. One unique property of these videos is that not all of the video can be viewed at any given time by one user, due to limited field of view. This suggests that, through analyzing user behavior within a VR video, we could optimize the video specifically for what a user is seeing at any given moment, and cut out the rest of the unnecessary information.

## Introduction

Last semester, we did just that: take into account where users tend to look using a heat map and massively improve storage space (and therefore streaming speed) by removing extraneous parts of the video.

This semester, our goal is to further improve such general strategies by narrowing down the scope. By separating users into clusters based on their viewing behavior, we can then create more specialized videos for each cluster that can cut out additional parts of the video without compromising the parts of the video that a user in that cluster sees.

Furthermore, an additional goal is to then try and predict which cluster a new user watching the video for the first time will fit into. Multiple approaches will be considered including Probablistic, Machine Learning, and other popular approaches within the field.
