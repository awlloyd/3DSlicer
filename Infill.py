import numpy as np
import shapely.geometry as sg
import shapely.affinity as sa


density = 1.0
platformWidth = 50
platformHeight = 50
coords = [
			[[0.0,4.0],[3.0,6.0]],
			[[3.0,6.0],[8.0,6.0]],
			[[8.0,6.0],[11.0,4.0]],
			[[11.0,4.0],[8.0,2.0]],
			[[8.0,2.0],[3.0,2.0]],
			[[3.0,2.0],[0.0,4.0]]
		]
"""
coords = [
			[[5,2],[0,10]],
			[[0,10],[5,18]],
			[[5,18],[20,18]],
			[[20,18],[25,10]],
			[[25,10],[20,2]],
			[[20,2],[5,2]]
		 ]
"""

if (coords[0][0] != coords[-1][1]):
	print("Shape is not closed. Exiting...")
	exit(1)
coordsSize = len(coords)
coordsPoints = [[]]
coordsPoints[0] = coords[0][0]
for i in range(coordsSize):
	coordsPoints.append(coords[i][1])
shape = sg.LineString(coordsPoints)


def __main__():
	print("\tCoords")
	for c in coords:
		print(c)
	print()

	vertInfillVectors = vert_infill(shape)
	horizInfillVectors = horiz_infill(shape)
	rotShape = sa.rotate(shape, 90, 'center')
	print(rotShape)
	#infillVectorsRot = infill(rotShape)
	print("\n\tVertInfill")
	for v in vertInfillVectors:
		print(v)
	print()
	print("\n\tHorizInfill")
	for h in horizInfillVectors:
		print(h)
	print()
	#print("\n\tinfillRot")
	#for v in infillVectorsRot:
	#	print(v)
	#print()
	
	structOut = {
		"perimeter": coords,
		"infill": vertInfillVectors,
		"settings": None
	}
	#print(structOut)

	return 0


def vert_infill(shp):
	vecs = [[[],[]]]
	i = 0
	while (i <= platformWidth):
		vertLine = sg.LineString([[i,0],[i,platformHeight]])
		vertIntersect = shp.intersection(vertLine)
		if (not(vertIntersect.is_empty) and (vertIntersect.geom_type == "MultiPoint")):
			p1 = [vertIntersect[0].x,vertIntersect[0].y]
			p2 = [vertIntersect[1].x,vertIntersect[1].y]
			vecs.append([p1,p2])
		i += density

	vecs.remove([[],[]])
	
	return vecs


def horiz_infill(shp):
	vecs = [[[],[]]]
	i = 0
	while (i <= platformHeight):
		horizLine = sg.LineString([[0,i],[platformWidth,i]])
		horizIntersect = shp.intersection(horizLine)
		if (not(horizIntersect.is_empty) and (horizIntersect.geom_type == "MultiPoint")):
			p1 = [horizIntersect[0].x,horizIntersect[0].y]
			p2 = [horizIntersect[1].x,horizIntersect[1].y]
			vecs.append([p1,p2])
		i += density

	vecs.remove([[],[]])
	
	return vecs

__main__()

