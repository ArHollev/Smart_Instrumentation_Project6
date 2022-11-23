import sys
import os
import io

from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import loadUiType
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtGui import QPainter,QPen
from PySide6.QtCore import Qt

import folium
import overpy
import osmnx as ox

api = overpy.Overpass()
current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(
    os.path.join(current_dir, "layout.ui"))  # layoutfile die met QTcreator gemaakt is wordt geladen


def gebiedanalyse(breedte, lengte, straal, feature_key):
    query = ox.geometries_from_point((breedte, lengte), {feature_key: True},
                                     dist=(straal))  # command dat "landuse" gegevens ophaalt uit osm
    if query.empty:
        return

    # maken van lijst voor gebiedsanalye
    f = list()  # maken van een lijst van alle areas "landuse"
    x = query[feature_key]
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
        tags = {
            feature_key: i}  # tags veranderen naar betrevende soort landuse waarvoor oppervlakte berekend moet worden
        result = ox.geometries_from_point((breedte, lengte), tags, dist=100)
        result.crs = 'epsg:4328'  # assign correct CRS in the correct format here
        gebied = sum(result.area)  # berekenen van som van de oppervlakten
        w[i] = gebied
    grootste_gebied = max(w, key=w.get)  # geeft het grootse landuse oppervlakte
    print(w)

    # printen van resultaat
    print("This area is a", grootste_gebied, "area")
    return grootste_gebied


class OCR(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.update_map(51.0557409, 3.7218855, 200)

        self.longitude.setText("51.0557409")
        self.latitude.setText("3.7218855")

        self.slider_radius.setRange(10, 1000)
        self.slider_radius.setSingleStep(10)
        self.slider_radius.setValue(200)
        self.radius.setText(str(self.slider_radius.value()))
        self.slider_radius.valueChanged.connect(lambda: self.radius.setText(str(self.slider_radius.value())))

        self.btn_analyse.clicked.connect(self.create_chart)


        self.button.clicked.connect(self.calculate)

    # calculate bekijkt hoeveel nodes van bepaalde key (bijvoorbeeld amenity) in gegeven radius bevindt
    def calculate(self):
        key = 'amenity'
        longitude = self.longitude.text()
        latitude = self.latitude.text()
        radius = str(self.slider_radius.value())
        myquery = api.query(
            'way(around:' + str(radius) + ',' + longitude + ',' + latitude + ')[' + key + ']; (._;>;); out geom;')

        self.result.setText("The number of " + key + " found in the selected area: " + str(len(myquery.nodes)))
        print(len(myquery.nodes))
        self.update_map(float(longitude), float(latitude), radius)

    # analyse functie bekijkt wat de grootste landgebruik is binnen de ingegeven straal
    def analyse(self):
        # ingegeven lon,lat en radius ophalen
        getlong = float(self.longitude.text())
        getlat = float(self.latitude.text())
        getrad = self.slider_radius.value()
        self.update_map(getlong, getlat, getrad)
        key = ["landuse"]
        self.result.setText("")
        for i in key:
            grootstegebied = gebiedanalyse(getlong, getlat, getrad, i)
            if grootstegebied:
                self.result.setText("This area is a " + grootstegebied + " area" + "\n")


    # update_map zorgt ervoor dat elke keer query met nieuwe coordinaten uitgevoerd is, de map zich verstelt
    def update_map(self, lon, lat, rad):
        m = folium.Map(location=[lon, lat], tiles="OpenStreetMap", zoom_start=14, min_zoom=8, max_zoom=25)
        folium.Circle([lon, lat], rad, fill=True).add_to(m)

        m.add_child(folium.LatLngPopup())

        data = io.BytesIO()
        m.save(data, close_file=False)
        webview = QWebEngineView()
        webview.setHtml(data.getvalue().decode())
        layout = self.mapbox
        if layout.count():
            layout.takeAt(0)
        layout.addWidget(webview)

    def create_chart(self):
        self.series = QPieSeries()
        label = ["a","b","c","d"]
        value = [10,20,30,40]
        for l,v in zip(label,value):
            self.series.append(l,v)
        self.chart = QChart()
        self.chart.addSeries(self.series)
        #chart.setAnimationOptions(QChart.SeriesAnimations)

        self.view =  QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)

        layout = self.chartWid
        if layout.count():
            layout.takeAt(0)
        layout.addWidget(self.view)






if __name__ == "__main__":
    app = QApplication([])
    widget = OCR()
    widget.show()
    sys.exit(app.exec())
