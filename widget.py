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

import pandas as pd
import geopy.distance
import networkx as nx
from IPython.display import IFrame
import numpy

import gc

ox.config(use_cache=True, log_console=True)

api = overpy.Overpass()
current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(
    os.path.join(current_dir, "layout.ui"))  # layoutfile die met QTcreator gemaakt is wordt geladen


def gebiedanalyse(breedte, lengte, straal, feature_key):
    result = ox.geometries_from_point((breedte, lengte), {feature_key: True},
                                     dist=(straal))  # command dat "landuse" gegevens ophaalt uit osm
    if result.empty:
        return


    result['area'] = result.area

    DataframeOppervlakte = result.dissolve(by=feature_key, aggfunc={"area": "sum"})
    DataframeOppervlakte.head()

    w = DataframeOppervlakte.to_dict()
    res = {key:w[key] for key in w.keys() & {'area'}}
    DictOppervlak = (res['area'])   
    grootste_gebied = max(DictOppervlak, key=DictOppervlak.get)
    print(grootste_gebied)
    print(DictOppervlak)
    
    #maken van een lijst van de aanwezige landuse's
    lijst = tuple(set(result['landuse']))
    print(lijst)
    
    #printen van resultaat
    #print("This area is a", grootste_gebied, "area")
       
    return grootste_gebied, DictOppervlak

def routeanalyse(lat_A, lon_A, lat_B, lon_B):
    #inputs van de gebruiker
    # download the street network for Piedmont, CA
    place = "gent,belgie"
    #start punt 
    start = (lon_A, lat_A)
    #eindpunt
    finish = (lon_B, lat_B)

    #hier worden alle netwerken van de osmnx data base die handig zijn voor onze opdacht opgeslagen.
    #verschillende netwerk types worden in gegeven om zo meerdere verschillende routes te kunnen genereren
    G = ox.graph_from_place(place, network_type="all",retain_all=True, truncate_by_edge=True, clean_periphery=True,) #blauw
    # G2 = ox.graph_from_place(place, network_type='all') #rood
    # G3 = ox.graph_from_address(place, dist=800, network_type='all') #oranje
    G4 = ox.graph_from_address(place, network_type="bike") #geel 
    # G5 = ox.graph_from_address(place, network_type="walk") #groen
    # G6 = ox.graph_from_address(place, network_type="all_private") #rose
    # G7 = ox.graph_from_address(place, network_type="drive_service") #paars

    #al bovenstaande netwerken worden in een list gestoken zodat ze verder in de code 
    #gemakkelijker kunnen worden opgehaald in bijvoorbeeld for lussen.
    #netwerken
    G_all = []
    # G_all.append(G)
    # G_all.append(G2)
    # G_all.append(G3)
    G_all.append(G4)
    # G_all.append(G5)
    # G_all.append(G6)
    # G_all.append(G7)
    #ook alle kleuren worden in een lijst gestoken om de zelfde reden
    #deze waarden staan in het nederlands en zijn dus output singnalen om te printen naar de gebruiker
    kleuren = []
    # kleuren.append("blauw")
    # kleuren.append("rood")
    # kleuren.append("oranje")
    kleuren.append("geel")
    # kleuren.append("groen")
    # kleuren.append("rose")
    # kleuren.append("paars")
    #deze lijst heeft de zelfde waarden maar in het engels om de routes een kleur te kunnen toe eigenen
    colors = []
    # colors.append("blue")
    # colors.append("red")
    # colors.append("orange")
    colors.append("yellow")
    # colors.append("green")
    # colors.append("pink")
    # colors.append("purple")
    
    
    # use networkx to calculate the shortest path between two nodes
    #geeft de korste nodes bij een bepaald coordinaat
    start_node = ox.nearest_nodes(G, start[1], start[0])
    finish_node = ox.nearest_nodes(G, finish[1], finish[0])

    #routes:
    #allemaal verschillende routes gegenereerd uit een bepaald G netwerk
    #elk G netwerk is anders dus er worden verschillende routes gemaakt
    #de start en finish node tonen de functie welke twee punten moeten verbonden worden
    # route1 = nx.shortest_path(G, start_node, finish_node)
    # route2 = nx.shortest_path(G2, start_node, finish_node, weight='length')
    # route3 = nx.shortest_path(G3, start_node, finish_node)
    route4 = nx.shortest_path(G4, start_node, finish_node)
    # route5 = nx.shortest_path(G5, start_node, finish_node)
    # route6 = nx.shortest_path(G6, start_node, finish_node)
    # route7 = nx.shortest_path(G7, start_node, finish_node)

    #opnieuw voor het gemak alle nodes in een lijst gestoken
    routes = []
    # routes.append(route1) 
    # routes.append(route2)
    # routes.append(route3) 
    routes.append(route4) 
    # routes.append(route5) 
    # routes.append(route6) 
    # routes.append(route7)
    
    
    #hier worden de verschillende lengtes van de routes berekend.
    # route1_length = int(sum(ox.utils_graph.get_route_edge_attributes(G, route1, 'length')))
    # route2_length = int(sum(ox.utils_graph.get_route_edge_attributes(G2, route2, 'length')))
    # route3_length = int(sum(ox.utils_graph.get_route_edge_attributes(G3, route3, 'length')))
    route4_length = int(sum(ox.utils_graph.get_route_edge_attributes(G4, route4, 'length')))
    # route5_length = int(sum(ox.utils_graph.get_route_edge_attributes(G5, route5, 'length')))
    # route6_length = int(sum(ox.utils_graph.get_route_edge_attributes(G6, route6, 'length')))
    # route7_length = int(sum(ox.utils_graph.get_route_edge_attributes(G7, route7, 'length')))

    #lengtes worden opnieuw in een list gestoken hier met een while lus omdat we toch weten dat er altijd 7 routes zijn
    i = 0
    routes_lengths = []
    while i < 7:
        
        lengte = int(sum(ox.utils_graph.get_route_edge_attributes(G_all[i], routes[i], 'length')))
        routes_lengths.append(lengte)
        i = i +1
    
    
    #in deze code wordt van elke route de omgeving benaderd en berekend.
    #de while lus wordt gebruikt om de 7 verschillende routes af te gaan 
    teller = 3
    while teller == 3:
        #hieronder zijn 4 verschillende listen waarin per node in de route
        #de x-y cordianten en de omgeving worden in opgeslagen
        y_cor = []
        x_cor = []
        omgeving = []

        #het vullen van bovesntaande lists gebeurd met onderstaande for lus
        nummer1 = 0
        for i in routes[0]:
            y = G.nodes[i]['y']
            x = G.nodes[i]['x']
            y_cor.append(y)
            x_cor.append(x)
            #result bevat alle landuse informatie in een straal van 100meter op een bepaalde cordinaat.
            result = ox.geometries_from_point((y, x),{"landuse":True}, dist =(100))
            nummer1 =+ 1
            
            #de f list wordt gevuld met elk gevonden landuse element uit result
            f = list()
            for i in result["landuse"]:
                f.append(i)
                #de r list bevat de zelfde waarden als in f maar dan zonder dubbels
                r = list()
                for i in f:
                    if i in r:
                        continue
                    if i not in r:
                        r.append(i)
                    
            # controleert welke landuse de grootste oppervlakte heeft in een straal van 50m 
            # dict w wordt gevuld met de landuse elementen in de omgeving met als waarde de oppervlakte      
            w = {}   
            for i in r:
                tags = {'landuse': i}
                result = ox.geometries.geometries_from_point((y, x), tags, dist =(50))
                result.crs = 'epsg:4328'
                gebied = sum(result.area)
                w[i] = gebied
            
            #de grootste oppervlakte wordt toegekend aan de node en in de omgeving lijst gestoken
            grootste_gebied = max(w, key=w.get)
            omgeving.append(grootste_gebied)  

        # de lengte tussen gebieden wordt berekend voor zo een beter beeld te krijgen hoelang we in een bepaald gebied lopen
        nummer = 0
        totaal = 0
        omgeving_lengths = {}
        getal = 0
        r = list()
        
        for i in omgeving:
            if i in r:
                continue
            if i not in r:
                r.append(i)
            getal += 1

        #de dict wordt gevuld met de verschillende gebieden 
        #aan elk gebied wordt ook een waarde nul toegekend om later in de while lus gemakkelijk waardes te kunnen bijvoegen
        for i in r:
            omgeving_lengths[i] =0
        while nummer < len(routes[teller])-1:
            lengte = int(sum(ox.utils_graph.get_route_edge_attributes(G_all[teller],(routes[teller][nummer],routes[teller][nummer+1]) , 'length')))
            nummer = nummer+1
            totaal += lengte
            omgeving_lengths[omgeving[nummer]] += lengte
        
        #output voor gebruiker
        print("totale lengte route:",teller+1,"-",kleuren[teller])
        print(routes_lengths[teller],"meter")
        print()
        print("omgeving van route:")
        for i in omgeving_lengths:
            lengte = omgeving_lengths[i]
            percent = float(lengte/routes_lengths[teller])*100
            print("%.2f" % percent,"%",i,"(",omgeving_lengths[i],"meter )")
        print()
        print()
        teller += 1

    
    #na keuze gebruiker, de route plotten
    #kies een waarde (1,2,4,5,6 of 7)
    keuze = 5
    my_map = folium.Map(location=[51.026316, 3.710697],zoom_start=15)
    map = ox.plot_route_folium(G_all[keuze-1], routes[keuze-1], route_map=my_map, popup_attribute="length", zoom=25, weight=7, color=colors[keuze-1])
    center = ((start[0]+finish[0])/2,(start[1]+finish[1])/2)

    # radius afstand omzetten naar meter afstand plus een marge
    afstand = geopy.distance.geodesic(start, finish).km

    #start punt
    folium.Marker(
        location=start,
        popup=('start punt'),
        tooltip=('start punt'),
        icon=folium.Icon(color='green',icon='circle',prefix='fa'),
    ).add_to(map)

    #eind punt 
    folium.Marker(
        location=finish,
        popup=('eind punt'),
        tooltip=('eind punt'),
        icon=folium.Icon(color='red'),
    ).add_to(map)

    #toont een cirkel waarin de routes geconstrueerd worden
    folium.Circle(
        location=[center[0],center[1]],
        radius= (afstand*1000)/1.2,
        popup = 'area',
        color='#2642ab',
        fill=True,
        fill_color='#e1e9f7'
    ).add_to(map)
    return map
    

class OCR(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.update_map(51.0557409, 3.7218855, 200)

        self.longitude_P.setText("51.0557409")
        self.latitude_P.setText("3.7218855")

        self.slider_radius.setRange(10, 1000)
        self.slider_radius.setSingleStep(10)
        self.slider_radius.setValue(200)
        self.radius.setText(str(self.slider_radius.value()))
        self.slider_radius.valueChanged.connect(lambda: self.radius.setText(str(self.slider_radius.value())))

        self.btn_gebied.clicked.connect(self.g_analyse)
        
        self.btn_route.clicked.connect(self.r_analyse)

        self.straal_calc.clicked.connect(self.calculate)
        

    # calculate bekijkt hoeveel nodes van bepaalde key (bijvoorbeeld amenity) in gegeven radius bevindt
    def calculate(self):
        key = 'amenity'
        longitude = self.longitude_P.text()
        latitude = self.latitude_P.text()
        radius = str(self.slider_radius.value())
        myquery = api.query(
            'way(around:' + str(radius) + ',' + longitude + ',' + latitude + ')[' + key + ']; (._;>;); out geom;')
        self.tekst_result.setText("The number of " + key + " found in the selected area: " + str(len(myquery.nodes)))
        print(len(myquery.nodes))
        self.update_map(float(longitude), float(latitude), radius)

    # analyse functie bekijkt wat de grootste landgebruik is binnen de ingegeven straal
    def g_analyse(self):
        # ingegeven lon,lat en radius ophalen
        getlong = float(self.longitude_P.text())
        getlat = float(self.latitude_P.text())
        getrad = self.slider_radius.value()
        self.update_map(getlong, getlat, getrad)
        key = ["landuse"]
        self.tekst_result.setText("")
        for i in key:
            return_g_ana = gebiedanalyse(getlong, getlat, getrad, i)
            if return_g_ana[0]:
                self.tekst_result.setText("This area is a " + return_g_ana[0] + " area" + "\n")
        #self.create_chart(return_g_ana[1])
                
    def r_analyse(self):
        getlongA = float(self.longitude_A.text())
        getlatA = float(self.latitude_A.text())
        getlongB = float(self.longitude_B.text())
        getlatB = float(self.latitude_B.text())
        map = routeanalyse(getlatA, getlongA, getlatB, getlongB)
        map.update_map(self, getlongA, getlatA, 0)     


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

    def create_chart(self, gebiedarray):
        label, waarde = [], []
        for key, value in gebiedarray.items():
            label.append(key)
            waarde.append(value)
        self.series = QPieSeries()
        for l,v in zip(label,waarde):
            self.series.append(l,v)
        chart = QChart()
        chart.addSeries(self.series)

        view =  QChartView(chart)
        view.setRenderHint(QPainter.Antialiasing)

        layout = self.chartWid
        if layout.count():
            layout.takeAt(0)
        layout.addWidget(view)


        
if __name__ == "__main__":
    app = QApplication([])
    widget = OCR()
    widget.show()
    sys.exit(app.exec())
