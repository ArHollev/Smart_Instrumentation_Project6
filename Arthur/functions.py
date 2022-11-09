import math
import numpy as np
from point import Point
import pandas as pd
import requests
import urllib
import geopy
import geopy.distance
from datetime import datetime
import os

ALPHA = 0.0005
D1 = 1
p0 = 2E-5  # Pa
MATRIX_G = 100

# Converts dB into Pascal
def db_to_pa(lmax):
    p = p0 * 10 ** (lmax / 20)  # Pa
    return p

# Calculates sound after losses due to distance
def sound_calculation(point, flight):
    position = Point(flight.latitude, flight.longitude, flight.geo_altitude)
    distance = point.distance(position)
    source = flight.source

    lmax = source - 20 * math.log10(distance / D1) - 8.69 * ALPHA * (distance - D1)
    return lmax

# Fill matrix with pressures based on single plane on single timestamp
def fill_matrix(flight, lamin, lamax, lomin, lomax):
    position = Point(flight.latitude, flight.longitude, flight.geo_altitude)
    source = flight.source # dB emitted by plane
    d_matrix = np.zeros((MATRIX_G, MATRIX_G))
    for y in range(len(d_matrix)):
        latitude = lamax - ((lamax - lamin) / MATRIX_G) * y  # Latitude in matrix[y]
        for x in range(len(d_matrix[0])):
            longitude = lomin + ((lomax - lomin) / MATRIX_G) * x  # Longitude in matrix[x]
            # Add distance to plane on every point in matrix
            d_matrix[x][y] = position.distance(Point(latitude, longitude, 0))
    lmax = source - 20 * np.log10(d_matrix / D1) - 8.69 * ALPHA * (d_matrix - D1)  # in dB
    lmax[lmax < 1] = 0  # Deletes useless values, makes function run faster
    p = p0*np.power(10*np.ones((MATRIX_G, MATRIX_G)), lmax/20)
    result = np.square(p) / (p0 * p0)
    return result

# Gets map image of 1200x1200 pixels, with bounding box as parameter
def get_map(lamin, lamax, lomin, lomax):
    url = "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/[" + str(lomin) + "," + str(lamin) + "," + str(
        lomax) + "," + str(
        lamax) + "]/1280x1280?access_token=pk.eyJ1IjoiYXJub2hlbmNrZXMiLCJhIjoiY2t3ejI4a2JmM" \
                 "GRzazJ6bDQzMGI2aGVjeSJ9.nY8_SQscwoLs0FjwP8Y4vA"

    response = requests.get(url)

    file = open("map.png", "wb")
    file.write(response.content)

# Get airport information based on IATA-code
def get_airport():
    airport = input('Give airport code: ')
    # Search in airports csv (contains information of all global airports)
    airports = pd.read_csv('airports.csv', usecols=["name", "latitude_deg", "longitude_deg", "iata_code"])
    airports = airports.dropna()  # Ignore airports with N/A values

    selected = airports[airports.iata_code == airport]
    print('You selected: ' + selected["name"].iloc[0])
    # iloc used to select first value (normally only 1 airport should match)
    latitude = selected["latitude_deg"].iloc[0]
    longitude = selected["longitude_deg"].iloc[0]

    # Make bounding box around airport within 7km radius
    airport_point = geopy.Point(latitude, longitude)
    distance = geopy.distance.distance(kilometers=7)

    bbox1 = distance.destination(point=airport_point, bearing=315)
    bbox2 = distance.destination(point=airport_point, bearing=135)
    lamax, lomin = bbox1.latitude, bbox1.longitude
    lamin, lomax = bbox2.latitude, bbox2.longitude

    return latitude, longitude, lamin, lamax, lomin, lomax, selected["iata_code"].iloc[0], selected["name"].iloc[0]

# Makes main look cleaner by creating file name of dataset + generated heatmap here
def get_filename(airport, time, duration):
    filename = airport + "_" + datetime.fromtimestamp(time).strftime("%d-%m-%Y_%H-%M").replace('/', '-') \
               + "_" + str(duration)
    return filename
