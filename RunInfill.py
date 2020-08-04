# RunInfill.py
# Author: Andrew Lloyd (awlloyd@clemson.edu)

# Import Infill.py
import Infill as iv


# Define the input coordinates for the shape to be sliced
coordsIn = [
			[(0.0,4.0),(3.0,6.0)],
			[(3.0,6.0),(8.0,6.0)],
			[(8.0,6.0),(11.0,4.0)],
			[(11.0,4.0),(8.0,2.0)],
			[(8.0,2.0),(3.0,2.0)],
			[(3.0,2.0),(0.0,4.0)]
		]

print("\tCoords")
for c in coordsIn:
	print(c)
print()

# Initialize the Shapely LineString shape
shape = iv.init_shape(coordsIn)

# Generate horizontal infill vectors
horizInfillVectors = iv.horiz_infill(shape, 1.0)
print("\n\tHorizInfill")
for h in horizInfillVectors:
	print(h)
print()

# Generate rotated infill vectors
rotInfillVectors = iv.rot_infill(shape, 60, 1.0)
print("\n\tRotInfill")
for v in rotInfillVectors:
	print(v)
print()

