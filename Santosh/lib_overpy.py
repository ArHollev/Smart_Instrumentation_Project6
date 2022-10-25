# The around filter selects all elements within a certain radius in metres around the elements in the input set.
# If you provide coordinates, then these coordinates are used instead of the input set.
# The input set can be changed with an adapted prefix notation.
# As for all filters, the result set is specified by the whole statement, not the individual filter.

# The bounding box query filter selects all elements within a rectangular bounding box.

import overpy
api = overpy.Overpass()
radius = 2500
circle_lat = 51.0557409
circle_lon = 3.7218855
#restaurant = api.query ('way(around:'+str(radius)+','+str(circle_lat)+','+str(circle_lon)+')["amenity"="restaurant"]; (._;>;); out geom;')
#amenity = api.query('way(around:'+str(radius)+','+str(circle_lat)+','+str(circle_lon)+')["amenity"]; (._;>;); out geom;')
amenity = api.query('way(around:'+str(radius)+','+str(circle_lat)+','+str(circle_lon)+')["landuse"="railway"]; (._;>;); out geom;')
print(len(amenity.nodes))
print(amenity.nodes[0])
#for nod in amenity.nodes: print(nod.id)
for node in amenity.nodes:
        print("    Lat: %f, Lon: %f" % (node.lat, node.lon))






