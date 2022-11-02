import osmnx as ox

breedte, lengte = 51.2232747408709, 2.980362630411266  # ingeven breedte en lengte coordinaten
result = ox.geometries_from_point((breedte, lengte), {"landuse": True},
                                  dist=(100))  # command dat "landuse" gegevens ophaalt uit osm

# plotten van geselecteerde gebied
result.plot(column='landuse', cmap='jet')  # plotten van map "landuse" cmap is kleuren index

# maken van lijst voor gebiedsanalye
f = list()  # maken van een lijst van alle areas "landuse"
x = result['landuse']
for i in x:
    f.append(i)

r = list()  # lijst die elke soort "landuse" maar een keer bevat
for i in f:
    if i in r:
        continue
    if i not in r:
        r.append(i)
print(f)
print(r)

# berekenen van som van de oppervlakte van de gebiedstypes
w = {}  # directory creeren
for i in r:
    tags = {'landuse': i}  # tags veranderen naar betrevende soort landuse waarvoor oppervlakte berekend moet worden
    result = ox.geometries_from_point((breedte, lengte), tags, dist=100)

    result.crs = 'epsg:4328'  # assign correct CRS in the correct format here

    gebied = sum(result.area)  # berekenen van som van de oppervlakten
    w[i] = gebied
grootste_gebied = max(w, key=w.get)  # geeft het grootse landuse oppervlakte
print(w)

# printen van resultaat
print("This area is a", grootste_gebied, "area")
