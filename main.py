from flask import Flask
import folium
import geopy.distance
import math


charging_stations = [[40,40], [19.10309955133587, 72.83346415808536], [19.104312805163, 72.83062279180376], [19.1001,72.839], [19.101,72.8423], [19.1100,72.85], [19.113,72.85], [19.13,72.8299], [19.135,72.849], [19.1222,72.8511], [19.113892545613968, 72.84446967234075], [19.136177045058858, 72.847114051259], [19.133414966567408, 72.8529076226722], [19.11999561574401, 72.8374776694386], [19.22541189447384, 72.85523167205281], [19.111326198026063, 72.8585909137273], [19.112560055473075, 72.9149698291551], [19.10535652723413, 72.90739128754285], [19.172887031085132, 72.85385838108493], [19.17295431222666, 72.85339195850364],  [19.119295420258567, 72.8355551559458], [19.118292473507925, 72.87802531214494], [19.120003660208937, 72.89942706138956], [19.104665721370683, 72.87072522710993], [19.109227720590457, 72.87380440295193], [19.13185476163701, 72.86802027163893], [19.13476666741024, 72.88186762526044], [19.15926673847634, 72.93419590270526], [19.24680610246423, 72.85729160850461], [19.148888617517983, 72.87171116366723], [19.12229170368244, 72.84012547140627],[19.072329, 72.99947], [19.1135,72.8697],[19.1146,72.8677],[19.110388097547,72.862489494608],[19.1185,72.8507],[19.111602253966836, 72.8972746089051], [19.24680610246423, 72.85729160850461], [19.22541189447384, 72.85523167205281], [19.172887031085132, 72.85385838108493], [19.15926673847634, 72.93419590270526], [19.148888617517983, 72.87171116366723], [19.12229170368244, 72.84012547140627], [19.112560055473075, 72.9149698291551]]
found_station = False


square_ward = [[],[],[],[],[],[],[],[],[]]
square_ward[0] = [[19.099954, 72.828711],[19.099954, 72.838720],[19.111969, 72.838720],[19.111969, 72.828711],1]
square_ward[1] = [[19.099954, 72.838720],[19.099954, 72.861105],[19.111969, 72.861105],[19.111969 ,72.838720],2]
square_ward[2] = [[19.099954, 72.861105],[19.099954, 72.90088224087725],[19.111969 ,72.90088224087725],[19.111969, 72.861105],2]
square_ward[3] = [[19.111969, 72.828711],[19.111969,72.838720],[19.127961,72.838720],[19.127961, 72.828711],1]
square_ward[4] = [[19.111969,72.838720],[19.111969, 72.861105],[19.127961, 72.861105],[19.127961,72.838720],2]
square_ward[5] = [[19.111969, 72.861105],[19.111969 ,72.90088224087725],[19.127961 , 72.90088224087725],[19.127961,72.861105],0]
square_ward[6] = [[19.127961 , 72.828711],[19.127961,72.83872],[19.14026186335908, 72.838720],[19.14026186335908,72.828711],0]
square_ward[7] = [[19.127961,72.83872],[19.127961, 72.861105],[19.14026186335908, 72.861105],[19.14026186335908, 72.838720],1]
square_ward[8] = [[19.127961, 72.861105],[19.127961,72.90088224087725],[19.14026186335908, 72.90088224087725],[19.14026186335908, 72.861105],1]

def get_traffic_level(latitude,longitude):
  for i in range(9):
    if latitude >=square_ward[i][0][0] and latitude < square_ward[i][2][0]:
      if longitude >=square_ward[i][0][1] and longitude <= square_ward[i][2][1]:
        return( square_ward[i][4] )
  return -1

def get_travel_distance(traffic_level, charge_left):
    average = 0
    if  traffic_level == 2 :  
        average = 2.2
    elif traffic_level == 1 : 
        average = 3.1
    elif traffic_level == 0 :
        average = 4.65
    return average * charge_left


def choose_charging_station(start, end, distance_permitted):
    selected_station = [math.inf, math.inf, charging_stations[0]]
    for cs in charging_stations:
        distance_between_start_and_station = geopy.distance.geodesic(start, cs).km
        if (distance_between_start_and_station <= distance_permitted):
            distance_between_end_and_station = geopy.distance.geodesic(end, cs).km
            detour_distance = distance_between_start_and_station + distance_between_end_and_station
            if detour_distance < selected_station[0]:
                selected_station[0] = detour_distance
                selected_station[1] = distance_between_end_and_station
                selected_station[2] = cs
            elif detour_distance == selected_station[0]:
                if (distance_between_end_and_station < selected_station[1]):
                    selected_station[1] = distance_between_end_and_station
                    selected_station[2] = cs
    print(selected_station[0])
    print(selected_station[1])
    return selected_station[2]

# print("Enter start location latitude")
# start_latitude= float(input())
# print("Enter start location longitude")
# start_longitude= float(input())

# start = (start_latitude, start_longitude)

# print("Enter end location latitude")
# end_latitude= float(input())
# print("Enter end location longitude")
# end_longitude= float(input())

# end = (end_latitude, end_longitude)

start = [19.103144586003904, 72.83171942843613]
end = [19.13648436695336, 72.85435574970387]

print("Enter charge Left")
charge_left = float(input())

traffic_level = get_traffic_level(start[0], start[1])
distance_permitted = get_travel_distance(traffic_level, charge_left)
charging_station = choose_charging_station(start, end, distance_permitted)


app = Flask(__name__)

@app.route("/")
def open_street_map():
    # this map using stamen toner
    map = folium.Map(
        location=[19.11847212668482, 72.863168970785],
        tiles='OpenStreetMap',
        zoom_start=15
    )
    color = ["#76FC00", "#EEEB00", "#FCA000"]
    folium.Rectangle([square_ward[0][0], square_ward[0][2]], fill = True, weight = 10, color=color[square_ward[0][4]], fillcolor=color[square_ward[0][4]]).add_to(map)
    folium.Rectangle([square_ward[1][0], square_ward[1][2]], fill = True, weight = 10, color=color[square_ward[1][4]], fillcolor=color[square_ward[1][4]]).add_to(map)
    folium.Rectangle([square_ward[2][0], square_ward[2][2]], fill = True, weight = 10, color=color[square_ward[2][4]], fillcolor=color[square_ward[2][4]]).add_to(map)
    folium.Rectangle([square_ward[3][0], square_ward[3][2]], fill = True, weight = 10, color=color[square_ward[3][4]], fillcolor=color[square_ward[3][4]]).add_to(map)
    folium.Rectangle([square_ward[4][0], square_ward[4][2]], fill = True, weight = 10, color=color[square_ward[4][4]], fillcolor=color[square_ward[4][4]]).add_to(map)
    folium.Rectangle([square_ward[5][0], square_ward[5][2]], fill = True, weight = 10, color=color[square_ward[5][4]], fillcolor=color[square_ward[5][4]]).add_to(map)
    folium.Rectangle([square_ward[6][0], square_ward[6][2]], fill = True, weight = 10, color=color[square_ward[6][4]], fillcolor=color[square_ward[6][4]]).add_to(map)
    folium.Rectangle([square_ward[7][0], square_ward[7][2]], fill = True, weight = 10, color=color[square_ward[7][4]], fillcolor=color[square_ward[7][4]]).add_to(map)
    folium.Rectangle([square_ward[8][0], square_ward[8][2]], fill = True, weight = 10, color=color[square_ward[8][4]], fillcolor=color[square_ward[8][4]]).add_to(map)

    for i in range(len(charging_stations)):
        folium.Marker(
            location=[charging_stations[i][0], charging_stations[i][1]]).add_to(map)
    
    folium.Marker(
            location=[start[0], start[1]],
            popup="<b>Origin</b>",
            icon=folium.Icon(color='green', icon='ok-sign')
            ).add_to(map)

    folium.Marker(
            location=[end[0], end[1]],
            popup="<b>Destination</b>",
            icon=folium.Icon(color='red', icon='ok-sign')
            ).add_to(map)

    print(charging_station)
    folium.Marker(
            location=[charging_station[0], charging_station[1]],
            popup="<b>Selected Station</b>",
            icon=folium.Icon(color='purple', icon='ok-sign')
            ).add_to(map)   

    if (charging_station == charging_stations[0]):
        points = [start]
    else:
        points = [start, charging_station, end]

    folium.PolyLine(points, color='green').add_to(map)

    return map._repr_html_()


if __name__ == "__main__":
    app.run(debug=True)