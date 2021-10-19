## High-Level Overview

```python
all_colours = [blue, red, green ...] # 30 colours

# output from clustering algorithm
[[id1, id5, id4], [id3, id2]]

class Chunk:
    clusters = [[id1, id5, id4], [id3, id2]]
    colours = [blue, green]
    frame_range = [60, 120]
	
  	def getIterator():
        return UserIterator(self)

class UserIterator:
    chunk
    cluster_index
    user_index
    
    # (user, colour)
    def __next__():
        # cluster/user index incrementing logic goes here
        return (chunk.clusters[cluster_index][user_index], 
                chunk.colours[cluster_index])

# pseudo-code
for chunk in video:
    clusters = chunk.clusters
    for (user, colour) in chunk.getIterator():
		for frame_number in range(chunk.frame_range[0], chunk.frame_range[1] + 1):
        	position = get_position(frame_number, user)
        	plot(position, colour)
```

## Clustering

For a particular chunk (some fixed number of frames), create a list of clusters for that chunk (a cluster is a list of userIDs).

##### Example Input

 `[60, 120]` (chunk comprised of frames 60 through 120)

##### Example Output

`[[id1, id5, id4], [id2, id3], [id6]]`

(`[id1, id5, id4]` is one cluster, `[id2, id3]` is another cluster, etc)

## Colouring

For a list of clusters, associate a unique colour with each cluster in the chunk.

##### Example Input

`[[id1, id5, id4], [id2, id3], [id6]]` 

##### Example Output

`[blue, green, red]`

For example, `[id1, id5, id4]` is the first element in the input, so its corresponding colour is the first element of the output, blue.

## Plotting 

##### Example Input

`100` (frame number 100)

##### Example Procedure

- Find the chunk that frame #100 belongs to - in this case it is chunk `[60, 120]`.
- Get the list of clusters associated with that chunk - in this case, `[[id1, id5, id4], [id2, id3], [id6]]`.
- Get the list of colours associated with the list of clusters - in this case, `[blue, green, red]`.
- For each user, colour the point they are looking at during that frame with corresponding colour. For example, colour the position that user `id2` is looking at green.

