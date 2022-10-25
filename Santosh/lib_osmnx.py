import osmnx as ox
# OSMnx is a Python package that lets you download geospatial data from OpenStreetMap
# and model, project, visualize, and analyze real-world street networks and any other geospatial geometries.
# You can download and model walkable, drivable, or bikeable urban networks with a single line of Python code
# then easily analyze and visualize them. You can just as easily download and work with other infrastructure types,
# amenities/points of interest, building footprints, elevation data, street bearings/orientations, and speed/travel time.

place = 'Ghent, Belgium'
tags = {'amenity' : True,
        'landuse' : ['retail', 'commercial'],
        'highway' : 'bus_stop'}
amenity = ox.geometries_from_place(place, tags=tags)

print(amenity.keys())
print(len(amenity.index))

# amenity = amenity.query('name == name')
amenity.sort_values('name')
print(amenity.info())




