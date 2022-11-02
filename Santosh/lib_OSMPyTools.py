from OSMPythonTools.overpass import Overpass
import pandas as pd
import plotly.express as px

overpass = Overpass()

query = '''
area[name="Austin"];
(relation
    ["type"="boundary"]
    ["name"="Austin"]
    ["admin_level"="8"]
    ["place"!="town"](area););
(._;>;);
out body;
'''
r = overpass.query(query)
js = r.toJSON()
filtered = [i for i in js['elements']if 'tags' not in i.keys()]
df = pd.DataFrame(filtered)
print(df.sample(5))
