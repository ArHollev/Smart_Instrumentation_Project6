import folium
from folium.features import DivIcon

text = 'Test'
circle_lat = 51.0500
circle_lon = 3.7303

m = folium.Map([60,10],tiles='OpenStreetMap', zoom_start= 5)
folium.Circle([circle_lat,circle_lon],1500, fill=True).add_child(folium.Popup('My name is Circle')).add_to(m)

folium.map.Marker(
    [circle_lat+0.5, circle_lon - 1.6],icon=DivIcon(icon_size=(150,36),icon_anchor=(0,0),
        html='<div style=""font-size: 24pt">%s</div>' % text,
    )).add_to(m)

m.save('map.html')


