from datetime import datetime
from time import sleep
from opensky_api import OpenSkyApi  # pip install git+https://github.com/openskynetwork/opensky-api/tree/master/python
import pandas as pd
from tqdm import tqdm
import time
from functions import get_airport, get_filename
import geopy
import geopy.distance
import os


RESOLUTION = 10  # in seconds
FOLDER_NAME = 'datasets'
OS_USER = 'rubendebbaudt'
OS_PASS = '!pH9J9*fBUnp'

la_airport, lo_airport, lamin, lamax, lomin, lomax, iata = get_airport()

start_now = input("Do you want to start now? (y/n) ")
if start_now == 'y':
    start_time = int(time.time())
elif start_now == 'n':
    start_time = int(input("Give unix timestamp when to start bulking: "))

    print("Waiting for " + str(datetime.fromtimestamp(start_time)))

    while int(time.time()) <= start_time:
        sleep(0.9)


def run_data_gatherer():
    time_now = int(time.time())
    rows = []

    airport_point = geopy.Point(la_airport, lo_airport)
    distance = geopy.distance.distance(kilometers=9)

    bbox1 = distance.destination(point=airport_point, bearing=315)
    bbox2 = distance.destination(point=airport_point, bearing=135)
    la_max, lo_min = bbox1.latitude, bbox1.longitude
    la_min, lo_max = bbox2.latitude, bbox2.longitude

    ts_start = datetime.fromtimestamp(time_now)
    ts_end = datetime.fromtimestamp(time_now - 3600)

    print("Data from " + str(ts_start) + " until "
          + str(ts_end))

    sleep(1)

    file_name = get_filename(iata, ts_end, 3600)

    api = OpenSkyApi(OS_USER, OS_PASS)

    for x in tqdm(range(time_now-3600, time_now, RESOLUTION), desc="Gathering data"):
        states = api.get_states(time_secs=x, bbox=(la_min, la_max, lo_min, lo_max))
        sleep(5)
        if states:
            for s in states.states:
                if s.icao24 and s.latitude and s.longitude and s.geo_altitude:
                    row = [x, s.icao24, s.latitude, s.longitude, s.geo_altitude, s.velocity, s.vertical_rate]
                    rows.append(row)
    df = pd.DataFrame(data=rows,
                      columns=('time', 'icao24', 'latitude', 'longitude', 'geo_altitude',
                               'velocity', 'vertical_rate'))
    df.sort_values('time', ascending=True, inplace=True)
    df.to_csv(os.path.join('datasets', get_filename(iata, ts_end, 3600)) + '.csv', index=False)

    print("Waiting for " + str(datetime.fromtimestamp(time_now+3600)))
    while int(time.time()) != time_now + 3600:
        sleep(0.9)


while True:
    run_data_gatherer()
