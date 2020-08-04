# Infill.py
# Author: Andrew Lloyd (awlloyd@clemson.edu)

# Imported Libraries
import numpy as np
import shapely.geometry as sg
import shapely.affinity as sa


# init_shape
# 	Takes in a a coordinate array and returns
# 	a Shapely LineString shape for use in other functions
def init_shape(coordsIn):
	if (coordsIn[0][0] != coordsIn[-1][1]):
		print("Shape is not closed. Exiting...")
		exit(1)
	coordsSize = len(coordsIn)
	coordsPoints = [[]]
	coordsPoints[0] = coordsIn[0][0]
	for i in range(coordsSize):
		coordsPoints.append(coordsIn[i][1])
	shape = sg.LineString(coordsPoints)

	return shape
	

# find_shape_box
# 	Takes the Shapely LineString shape and returns
# 	the bounding box that encapsulates it
def find_shape_box(shape):
	minX = min(c[0] for c in shape.coords)
	minY = min(c[1] for c in shape.coords)
	maxX = max(c[0] for c in shape.coords)
	maxY = max(c[1] for c in shape.coords)
	
	return [minX, minY, maxX, maxY]


# horiz_infill
# 	Takes the Shapely LineString shape and a specified density
# 	then draws horizontal infill lines through the shape. Returns
# 	an array containing the infill vectors.
def horiz_infill(shape, density):
	box = find_shape_box(shape)
	vecs = [[[],[]]]
	i = box[1]
	while (i <= box[3]):
		horizLine = sg.LineString([[box[0],i],[box[2],i]])
		horizIntersect = shape.intersection(horizLine)
		if (not(horizIntersect.is_empty) and (horizIntersect.geom_type == "MultiPoint")):
			p1 = (horizIntersect[0].x,horizIntersect[0].y)
			p2 = (horizIntersect[1].x,horizIntersect[1].y)
			vecs.append([p1,p2])
		i += density
	vecs.remove([[],[]])
	
	return vecs


# rot_infill
# 	Takes the Shapely Linestring shape and a specified angle and density
# 	then iteratively draws infill lines through the shape, rotating
# 	by the specified angle on each iteration.
def rot_infill(shape, angle, density):
	poly = sg.Polygon(shape)
	shapeCenter = poly.centroid
	tranShape = sa.translate(shape, -shapeCenter.x, -shapeCenter.y)
	rotShape = sa.rotate(tranShape, angle, 'center')
	rotBoundBox = find_shape_box(rotShape)
	horizInfillVectors = horiz_infill(rotShape, density)
	rotInfillVectors = [[[],[]]]
	for v in horizInfillVectors:
		centVecX = (v[0][0] + v[1][0]) / 2
		centVecY = (v[0][1] + v[1][1]) / 2
		rotVec = sa.rotate(sg.LineString(v), -angle, [0,0])
		newVec = sa.translate(rotVec, shapeCenter.x, shapeCenter.y)
		rotInfillVectors.append(list(newVec.coords))
	rotInfillVectors.remove([[],[]])

	return rotInfillVectors

