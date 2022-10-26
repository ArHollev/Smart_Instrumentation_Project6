import sys
import os
import io

import OSMPythonTools.api
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import loadUiType
from PySide6.QtWebEngineWidgets import QWebEngineView
import folium
from folium.features import DivIcon
import overpy


api = overpy.Overpass()
text = 'Circle'

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "form.ui"))


def clicked():
    print("Button clicked!!!!!!")


class OCR(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        # self.button.clicked.connect(lambda: clicked())
        self.button.clicked.connect(self.okk)
        self.testbutton.clicked.connect(self.testValue)
        self.map(51.0557409,3.7218855,500)

    def okk(self):
        longitude = self.longitude.text()
        latitude = self.latitude.text()
        radius = self.radius.text()
        # if not longitude or not latitude or not radius:
        print("longitude: " + longitude + " latitude: " + latitude + " radius: " + radius)
        amenity = api.query('way(around:' + radius + ',' + longitude + ',' + latitude + ')["amenity"="pub"]; (._;>;); out geom;')
        self.result.setText("The number of amenities found in the selected area: Pubs =  " + str(len(amenity.nodes)))
        print(len(amenity.nodes))
        if amenity.nodes:
            id = amenity.nodes[0].id
            print(api.parse_json(id))

        self.map(float(longitude),float(latitude),radius)

    def testValue(self):
        self.radius.setText("500")
        self.longitude.setText("51.0557409")
        self.latitude.setText("3.7218855")

    def map(self,lon,lat,rad):
        m = folium.Map(location=[lon,lat], tiles="OpenStreetMap", zoom_start=14, min_zoom=8, max_zoom=25)
        folium.Circle([lon, lat], rad, fill=True).add_child(folium.Popup(text)).add_to(m)
        folium.map.Marker([lon + 0.5, lat - 1.6],icon=DivIcon(icon_size=(150, 36), icon_anchor=(0,0),
                                   html='<div style=""font-size: 24pt">%s</div>' % text, )).add_to(m)

        data = io.BytesIO()
        m.save(data, close_file=False)
        webview = QWebEngineView()
        webview.setHtml(data.getvalue().decode())
        layout = self.mapbox
        if layout.count():
            layout.takeAt(0)
        layout.addWidget(webview)



if __name__ == "__main__":
    app = QApplication([])
    widget = OCR()
    widget.show()
    sys.exit(app.exec())
