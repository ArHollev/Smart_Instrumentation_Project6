import io
import sys

import folium
from folium.features import DivIcon
from PySide6 import QtWidgets, QtWebEngineWidgets
text = 'Circle of intrest ;°'
circle_lat = 28.257569465364416
circle_lon = 83.97760270096194
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    m = folium.Map(
        location=[circle_lat, circle_lon], tiles="OpenStreetMap", zoom_start= 17,min_zoom=8,max_zoom=25
    )
    folium.Circle([circle_lat,circle_lon],100, fill=True).add_child(folium.Popup(text)).add_to(m)
    folium.map.Marker(
    [circle_lat+0.5, circle_lon - 1.6],icon=DivIcon(icon_size=(150,36),icon_anchor=(0,0),
        html='<div style=""font-size: 24pt">%s</div>' % text,
    )).add_to(m)

    data = io.BytesIO()
    m.save(data, close_file=False)

    w = QtWebEngineWidgets.QWebEngineView()
    w.setHtml(data.getvalue().decode())
    w.resize(640, 480)
    w.show()

    sys.exit(app.exec())
