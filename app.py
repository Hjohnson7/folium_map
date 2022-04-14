import folium
import pandas as pd

#Create Map Object
map = folium.Map(location=[51.75, -2.45], zoom_start=12)


#Create Walks and Cycles Feature Groups
fg_walks=folium.FeatureGroup("Walks")
fg_cycles=folium.FeatureGroup("Cycles")



def add_route(file, walk_cycle, name, distance):
    """
    Reads in polyline data, creates a child feature and adds to feature group.
    """

    data = pd.read_csv(file)
    lat_lon = zip(list(data["lat"]), list(data["lon"]))
    lat_lon_unpacked = [[x,y] for x, y in lat_lon]
    
    vector = folium.vector_layers.PolyLine(lat_lon_unpacked,popup=f'<b>{name}</b>{walk_cycle}<br>{distance}',tooltip=name,color='black',weight=3)
    if walk_cycle == "walk":
        fg_walks.add_child(vector)
    else:
        fg_cycles.add_child(vector)


add_route("cycle_track.csv", "cycle","Cycle Track", "15 miles")
add_route("peddle.csv", "cycle","Cycle Centre", "6 miles")
add_route("speech_house.csv", "walk","Speech House", "3 miles")
add_route("worgreen.csv", "walk","Worgreen Lake", "1.5 miles")


#Read in pub/lakes/viewpoint data
data = pd.read_csv("forest_info.csv")

HTML = """
Name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
"""

def colour_selector(place):
    if place == "pub":
        return "red"
    elif place == "lake":
        return "blue"
    elif place == "view":
        return "green"


fg_lakes = folium.FeatureGroup(name="Lakes/Ponds")
fg_pubs = folium.FeatureGroup(name="Pubs")
fg_views = folium.FeatureGroup(name="View Points")


#For place in data, create a marker on the map.
for name, place, lt, ln in zip(list(data["name"]), list(data["type"]), list(data["lat"]), list(data["lon"])):
    iframe = folium.IFrame(html=HTML % (name, name), width=200, height=100)
    if place == "pub":
        fg_pubs.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon = folium.Icon(color = colour_selector(place))))
    elif place == "lake":
        fg_lakes.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon = folium.Icon(color = colour_selector(place))))
    else:
        fg_views.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon = folium.Icon(color = colour_selector(place))))


#Add feature groups to the map.
map.add_child(fg_walks)
map.add_child(fg_cycles)
map.add_child(fg_lakes)
map.add_child(fg_pubs)
map.add_child(fg_views)


#Add control to remove feature groups.
map.add_child(folium.LayerControl())

map.save("forestmap.html")