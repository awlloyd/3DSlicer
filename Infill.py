import numpy as np
import shapely.geometry as sg
import shapely.affinity as sa


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
	

def find_shape_box(shape):
	minX = min(c[0] for c in shape.coords)
	minY = min(c[1] for c in shape.coords)
	maxX = max(c[0] for c in shape.coords)
	maxY = max(c[1] for c in shape.coords)
	
	return [minX, minY, maxX, maxY]


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

