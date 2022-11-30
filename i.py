#importeren libraries
import osmnx as ox
import overpy
import matplotlib.pyplot as plt
import geopandas
import os


#invoeren van positie en straal

breedte, lengte = 51.908927, 7.601180 #ingeven breedte en lengte coordinaten
straal = 200
result = ox.geometries.geometries_from_point((breedte, lengte), {"landuse":True}, dist = straal )#command dat "landuse" gegevens ophaalt uit osm
#plotten van geselecteerde gebied

result['area'] = result.area
result2 = result.dissolve(by='landuse', aggfunc={
         "area": "sum"
     })
result2.head()



w = result2.to_dict()
res = {key:w[key] for key in w.keys() & {'area'}}
DictOppervlak = (res['area'])   
grootste_gebied = max(DictOppervlak, key=DictOppervlak.get)
print(grootste_gebied)
print(DictOppervlak)

#printen van resultaat
print("This area is a", grootste_gebied, "area")