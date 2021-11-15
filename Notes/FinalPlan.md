### **Goal** 

Determine which clustering algorithm is best for a particular video type.

### Metrics

We use silhouette score to measure cluster quality. Silhouette score ranges from -1 to 1 and indicates how close a particular user is to other users in its cluster compared to users in other clusters (higher values are better).

### **Algorithms to evaluate:**

- Geodesic distance
- K-means
- DB scan

### **Method**

1. Split the video into fixed-size chunks (for example, 60 frames long).
2. Use each algorithm to generate *per-frame* clusters for each frame in the chunk. 
   - Note that using the geodesic approach, users will be in the same cluster if they are all within a particular distance from one another.
3. Create an *affinity matrix* for the entire chunk, which indicates how often two users belonged to the same cluster throughout the chunk. The [i, j]th entry of the matrix is the *affinity* of users i and j - the number of frames for which users i and j were in the same cluster.
4. Convert the affinity matrix into a graph. Any two users whose affinity value exceeds a certain threshold (for example, 40 frames) are set to be adjacent in the graph.
5. Generate clusters *for the entire chunk* by using the BK algorithm to find disjoint max cliques of the graph. Each clique is a cluster.
6. Using the clusters computed in the previous step, compute the silhouette scores for each user for every frame in the chunk, and average them to compute the average silhouette score for the chunk.
7. Repeat 2-7 for all chunks in the video. Average the per-chunk silhouette scores to obtain an average silhouette score for the entire video.

### Graphs

#### Bar graph

- X-axis consists of three categories: one for each video type, each category has three bars, one for each algorithm
- Y-axis is silhouette score averaged over all videos in respective category

#### Line graph

- X-axis is time in chunks
- Y-axis is silhouette score for chunk
- Have multiple lines, each lines for one video from one category

#### Computing silhouette scores per chunk

1. Create affinity matrix for a chunk using each algorithm: geodistance DONE, k-means, and DBscan
2. Construct graph from affinity matrix using affinity threshold DONE
3. Find max cliques of graph to obtain clusters for chunk DONE
4. Compute silhouette score per frame by comparing users in that frame to computed clusters DONE
5. Average silhouette scores per frame to get silhouette score per chunk DONE
=======
### **Goal** 

Determine which clustering algorithm is best for a particular video type.

### Metrics

We use silhouette score to measure cluster quality. Silhouette score ranges from -1 to 1 and indicates how close a particular user is to other users in its cluster compared to users in other clusters (higher values are better).

### **Algorithms to evaluate:**

- Geodesic distance
- K-means
- DB scan

### **Method**

1. Split the video into fixed-size chunks (for example, 60 frames long).
2. Use each algorithm to generate *per-frame* clusters for each frame in the chunk. 
   - Note that using the geodesic approach, users will be in the same cluster if they are all within a particular distance from one another.
3. Create an *affinity matrix* for the entire chunk, which indicates how often two users belonged to the same cluster throughout the chunk. The [i, j]th entry of the matrix is the *affinity* of users i and j - the number of frames for which users i and j were in the same cluster.
4. Convert the affinity matrix into a graph. Any two users whose affinity value exceeds a certain threshold (for example, 40 frames) are set to be adjacent in the graph.
5. Generate clusters *for the entire chunk* by using the BK algorithm to find disjoint max cliques of the graph. Each clique is a cluster.
6. Using the clusters computed in the previous step, compute the silhouette scores for each user for every frame in the chunk, and average them to compute the average silhouette score for the chunk.
7. Repeat 2-7 for all chunks in the video. Average the per-chunk silhouette scores to obtain an average silhouette score for the entire video.

### Graphs

#### Average silhouette scores per video catergory (bar graph)

- X-axis consists of three categories: one for each video type, each category has three bars, one for each algorithm
- Y-axis is silhouette score averaged over all videos in respective category

#### Chunk-based silhouette scores over time (line graph)

- X-axis is time in chunks
- Y-axis is silhouette score for chunk
- Have multiple lines, each lines for one video from one category

#### Average silhouette scores per user (bar graph)

- X-axis is users (numbered 1 through 30)
- Y-axis is average silhouette score for a user (for a particular video, or maybe video category)

#### Computing silhouette scores per chunk

1. Create affinity matrix for a chunk using each algorithm: geodistance DONE, k-means, and DBscan
2. Construct graph from affinity matrix using affinity threshold DONE
3. Find max cliques of graph to obtain clusters for chunk DONE
4. Compute silhouette score per frame by comparing users in that frame to computed clusters DONE
5. Average silhouette scores per frame to get silhouette score per chunk DONE
