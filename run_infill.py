import Infill_v1 as iv


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

shape = iv.init_shape(coordsIn)

horizInfillVectors = iv.horiz_infill(shape, 1.0)
print("\n\tHorizInfill")
for h in horizInfillVectors:
	print(h)
print()

rotInfillVectors = iv.rot_infill(shape, 60, 1.0)
print("\n\tRotInfill")
for v in rotInfillVectors:
	print(v)
print()

"""
structOut = {
	"perimeter": coords,
	"infill": vertInfillVectors,
	"settings": None
}
#print(structOut)
"""

