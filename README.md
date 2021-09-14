# VR User Behavior Clustering

ACM Research Fall 2021

## Background

VR videos have massive storage and streaming requirements in order to perform as well as modern day 2D videos. One unique property of these videos is that not all of the video can be viewed at any given time by one user, due to limited field of view. This suggests that, through analyzing user behavior within a VR video, we could optimize the video specifically for what a user is seeing at any given moment, and cut out the rest of the unnecessary information.

## Introduction

Last semester, we did just that: take into account where users tend to look using a heat map and massively improve storage space (and therefore streaming speed) by removing extraneous parts of the video.

This semester, our goal is to further improve such general strategies by narrowing down the scope. By separating users into clusters based on their viewing behavior, we can then create more specialized videos for each cluster that can cut out additional parts of the video without compromising the parts of the video that a user in that cluster sees.

Furthermore, an additional goal is to then try and predict which cluster a new user watching the video for the first time will fit into. Multiple approaches will be considered including Probablistic, Machine Learning, and other popular approaches within the field.
