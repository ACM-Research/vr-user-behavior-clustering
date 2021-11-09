#### Bar graph

- X-axis consists of three categories: one for each video type, each category has three bars, one for each algorithm
- Y-axis is silhouette score averaged over all videos in respective category

#### Line graph

- X-axis is time in chunks
- Y-axis is silhouette score for chunk
- Have multiple lines, each lines for one video from one category

#### Computing silhouette scores per chunk

1. Create affinity matrix for a chunk using each algorithm: geodistance, k-means, and DBscan
2. Construct graph from affinity matrix using affinity threshold
3. Find max cliques of graph to obtain clusters for chunk
4. Compute silhouette score per frame by comparing users in that frame to computed clusters
5. Average silhouette scores per frame to get silhouette score per chunk