## Running Silhouette Data Collection

```
python Silhouette.py true true true
```

Each boolean argument specifies whether silhouette scores should be computed for geodesic, K-means, or DBSCAN based clustering. For example,

```
python Silhouette.py false true false
```

will only compute scores for K-means clustering.