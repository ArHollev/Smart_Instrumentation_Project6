import io
import sys

import folium
from folium.features import DivIcon
from PySide6 import QtWidgets, QtWebEngineWidgets

import overpy

api = overpy.Overpass()
text = 'Circle of intrest ;°'
radius = 500
circle_lat = 51.0557409
circle_lon = 3.7218855

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    amenity = api.query('way(around:' + str(radius) + ',' + str(circle_lat) + ',' + str(circle_lon) + ')["amenity"="pharmacy"]; (._;>;); out geom;')

    m = folium.Map(location=[circle_lat, circle_lon], tiles="OpenStreetMap", zoom_start=15, min_zoom=8, max_zoom=25)
    folium.Circle([circle_lat, circle_lon], radius, fill=True).add_child(folium.Popup(text)).add_to(m)
    folium.map.Marker([circle_lat + 0.5, circle_lon - 1.6],
                      icon=DivIcon(icon_size=(150, 36), icon_anchor=(0, 0),
                                   html='<div style=""font-size: 24pt">%s</div>' % text, )).add_to(m)

    data = io.BytesIO()
    m.save(data, close_file=False)

    w = QtWebEngineWidgets.QWebEngineView()
    w.setHtml(data.getvalue().decode())
    w.resize(640, 480)
    w.show()

    print(len(amenity.nodes))
    if amenity.nodes:
        print(amenity.nodes[0])

    sys.exit(app.exec())
