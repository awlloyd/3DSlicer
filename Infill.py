import numpy as np
import shapely.geometry as sg
import shapely.affinity as sa


density = 1.0
platformWidth = 50
platformHeight = 50
coordsIn = [
			[[0.0,4.0],[3.0,6.0]],
			[[3.0,6.0],[8.0,6.0]],
			[[8.0,6.0],[11.0,4.0]],
			[[11.0,4.0],[8.0,2.0]],
			[[8.0,2.0],[3.0,2.0]],
			[[3.0,2.0],[0.0,4.0]]
		]
"""
coordsIn = [
			[[5,2],[0,10]],
			[[0,10],[5,18]],
			[[5,18],[20,18]],
			[[20,18],[25,10]],
			[[25,10],[20,2]],
			[[20,2],[5,2]]
		 ]
"""

if (coordsIn[0][0] != coordsIn[-1][1]):
	print("Shape is not closed. Exiting...")
	exit(1)
#minX = min(c[0][0] for c in coords)
#minY = min(c[0][1] for c in coords)
#maxX = max(c[0][0] for c in coords)
#maxY = max(c[0][1] for c in coords)
coordsSize = len(coordsIn)
coordsPoints = [[]]
coordsPoints[0] = coordsIn[0][0]
for i in range(coordsSize):
	coordsPoints.append(coordsIn[i][1])
shape = sg.LineString(coordsPoints)
rotShape = sa.rotate(shape, 90, 'center')
#print(rotShape)

def __main__():
	print("\tCoordsIn")
	for c in coordsIn:
		print(c)
	print()

	boundBox = find_shape_box(shape)
	vertInfillVectors = vert_infill(shape, boundBox)
	horizInfillVectors = horiz_infill(shape, boundBox)
	rotBoundBox = find_shape_box(rotShape)
	rotInfillVectors = horiz_infill(rotShape, rotBoundBox)
	print("\n\tVertInfill")
	for v in vertInfillVectors:
		print(v)
	print()
	print("\n\tHorizInfill")
	for h in horizInfillVectors:
		print(h)
	print()
	print("\n\tRotInfill")
	for v in rotInfillVectors:
		print(v)
	print()
	
	structOut = {
		"perimeter": coordsIn,
		"infill": vertInfillVectors,
		"settings": None
	}
	#print(structOut)

	return 0


def find_shape_box(shp):
	minX = min(c[0] for c in shp.coords)
	minY = min(c[1] for c in shp.coords)
	maxX = max(c[0] for c in shp.coords)
	maxY = max(c[1] for c in shp.coords)
	
	return [minX, minY, maxX, maxY]

def vert_infill(shp, box):
	vecs = [[[],[]]]
	i = box[0]
	while (i <= box[2]):
		vertLine = sg.LineString([[i,box[1]],[i,box[3]]])
		vertIntersect = shp.intersection(vertLine)
		if (not(vertIntersect.is_empty) and (vertIntersect.geom_type == "MultiPoint")):
			p1 = [vertIntersect[0].x,vertIntersect[0].y]
			p2 = [vertIntersect[1].x,vertIntersect[1].y]
			vecs.append([p1,p2])
		i += density

	vecs.remove([[],[]])
	
	return vecs


def horiz_infill(shp, box):
	vecs = [[[],[]]]
	i = box[1]
	while (i <= box[3]):
		horizLine = sg.LineString([[box[0],i],[box[2],i]])
		horizIntersect = shp.intersection(horizLine)
		if (not(horizIntersect.is_empty) and (horizIntersect.geom_type == "MultiPoint")):
			p1 = [horizIntersect[0].x,horizIntersect[0].y]
			p2 = [horizIntersect[1].x,horizIntersect[1].y]
			vecs.append([p1,p2])
		i += density

	vecs.remove([[],[]])
	
	return vecs

__main__()

