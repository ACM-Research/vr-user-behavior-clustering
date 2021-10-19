# Build Night 6

## Finish Building Visualization

1. Generate Chunks
2. Calculate clusters per Chunk
    * Find adj matrix for each frame
    * Using a certain affinity threshold (percentage of the chunk in which two users are connected), remove users that have affinity less than the threshold.
    * Use final adj matrix to define clusters for the chunk

## Parameters

1. Geodesic Distance Threshold
2. Time per Chunk
3. Affinity Threshold: Percentage of the chunk in which two users must be connected in order to be defined as connected throughout the chunk (currently 60%)

## How do we visualize a Cluster?