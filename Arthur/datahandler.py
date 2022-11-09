import datetime
from time import sleep
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
# pip install -e "git+https://github.com/openskynetwork/opensky-api.git#egg=opensky_api&subdirectory=python"
from opensky_api import OpenSkyApi
import pandas as pd
from tqdm import tqdm
import seaborn as sns
import geopy
import geopy.distance
from functions import get_filename
import os

OS_USER = 'rubendebbaudt'
OS_PASS = '!pH9J9*fBUnp'

# Get airplane data within bounding box on certain timestamps
def gather_data(la_airport, lo_airport, resolution, start_time, duration, name):
    rows = []

    # Create bounding box around airport within 9km radius
    airport_point = geopy.Point(la_airport, lo_airport)
    distance = geopy.distance.distance(kilometers=9)

    bbox1 = distance.destination(point=airport_point, bearing=315)
    bbox2 = distance.destination(point=airport_point, bearing=135)
    la_max, lo_min = bbox1.latitude, bbox1.longitude
    la_min, lo_max = bbox2.latitude, bbox2.longitude

    api = OpenSkyApi(OS_USER, OS_PASS)
    timestamp = datetime.datetime.fromtimestamp(start_time)

    # Use OpenSkyAPI to get data, API asks bounding box and unix time
    for x in tqdm(range(start_time - duration, start_time, resolution), desc="Gathering data"):
        states = api.get_states(time_secs=x, bbox=(la_min, la_max, lo_min, lo_max))
        sleep(5)
        if states:
            for s in states.states:
                if s.icao24 and s.latitude and s.longitude and s.geo_altitude:
                    # Add information in row, append row to rows [array]
                    row = [x, s.icao24, s.latitude, s.longitude, s.geo_altitude, s.velocity, s.vertical_rate]
                    rows.append(row)
    # Add whole array of arrays in dataframe
    df = pd.DataFrame(data=rows,
                      columns=('time', 'icao24', 'latitude', 'longitude', 'geo_altitude',
                               'velocity', 'vertical_rate'))
    # Fill N/A values with zero
    df = df.fillna(0)
    # Sort dataframe to organize samples together
    df.sort_values('time', ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)
    # Save data as csv for later
    df.to_csv(os.path.join('datasets', get_filename(name, start_time-duration, duration)) + '.csv')
    return df

# Generate heatmap
def generate_heatmap(figure, data, path, name, x_labels, y_labels):
    map_img = mpimg.imread(figure)

    sns.set()

    hmax = sns.heatmap(data,
                       alpha=0.6,  # Set map translucency
                       annot=False,
                       zorder=2,
                       xticklabels=x_labels,
                       yticklabels=y_labels,
                       )

    hmax.imshow(map_img,
                aspect=hmax.get_aspect(),
                extent=hmax.get_xlim() + hmax.get_ylim(),
                zorder=1)  # Put mapbox image under heatmap

    hmax.set_title(name)  # Add full airport name as title
    plt.savefig(path + '.jpg')  # Choose what output format you want
    # plt.savefig(path + '.pdf')
    plt.show() # Show image to get detailed dB values
