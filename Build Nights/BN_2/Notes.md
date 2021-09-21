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

## EOBN Order

1. Arsen Yang
