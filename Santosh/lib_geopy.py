from geopy.geocoders import Nominatim
import pandas as pd
from geopy.extra.rate_limiter import RateLimiter

# to show full table data in console
pd.set_option('display.width', 100)
pd.set_option('display.max_columns', 10)

loc = ['Batulechour','Brugge, 8000', 'aaigemstraat 103, 9000']

df = pd.DataFrame({'add': loc})

geolocator = Nominatim(user_agent="my_request")

geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

df['location'] = df['add'].apply(geocode)
df['Lat'] = df['location'].apply(lambda x: x.latitude if x else None)
df['Lon'] = df['location'].apply(lambda x: x.latitude if x else None)

print(df.head())
