# Build Night 2

## Potential Ideas

1. Head Velocity to tune prediction

2. Mapping 2D Projection to 3D :

- Map each row of pixels to a ring of pixels on the sphere (Top would be only 1 pixels, next row down would be a small ring, ... , middle would be circumference of sphere, ... small again)

## Heat Map Procedure

For a frame number,

1. Take last 3 numbers from csv for each user
2. Convert vector to angle
3. Angle Ratio = 2D cartesian Ratio -> use to find where in the 2D image everyone is looking
4. Turn coordinates into indices for a grid
5. Make heat map using grid

#### Parser

Input: a video number and a frame number.

Procedure: for every user trace for the video, take the last three columns of the row corresponding to the frame number, form a 3d vector from them, and add the vector to a list.

Output: the list of 3d vectors. Each vector is the location a user was looking at during the frame.

#### Heatmap Data Collection

Input: a list of 3d vectors (from the parser).

Procedure: create a 2d array of numbers. Each number is the frequency value for a square of the heatmap. Iterate over the list of 3d vectors, determine the X and Y values of the square that the point belongs to, and increment the frequency value of that square.

Output: a 2d array of frequency values.

#### Heatmap Generation

Input: a 2d array of frequency values (from the heatmap data collection step).

Procedure: pass the frequency array into seaborn's heatmap generation function.

Output: a heatmap image.

## EOBN Order

1. Arsen Yang