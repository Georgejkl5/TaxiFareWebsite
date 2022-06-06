import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from datetime import datetime
import pytz
import requests

st.markdown(" # NY taxi")

pickup_datetime = st.text_input("Enter date and time: 2022-06-06 12:00:00")
pickup_longitude = st.text_input("pickup_longitude")
pickup_latitude = st.text_input("pickup_latitude")
dropoff_longitude = st.text_input("dropoff_longitude")
dropoff_latitude = st.text_input("dropoff_latitude")
passenger_count = st.number_input("passenger_count", min_value =0, max_value = 10)


def predict(pickup_datetime,
            pickup_longitude,
            pickup_latitude,
            dropoff_longitude,
            dropoff_latitude,
            passenger_count):

    pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")
    eastern = pytz.timezone("US/Eastern")
    localized_pickup_datetime = eastern.localize(pickup_datetime, is_dst=None)
    utc_pickup_datetime = localized_pickup_datetime.astimezone(pytz.utc)
    formatted_pickup_datetime = utc_pickup_datetime.strftime("%Y-%m-%d %H:%M:%S")

    X_pred = pd.DataFrame(
        {
            "key": "2013-07-06",
            "pickup_datetime": formatted_pickup_datetime,
            "pickup_longitude": float(pickup_longitude),
            "pickup_latitude": float(pickup_latitude),
            "dropoff_longitude": float(dropoff_longitude),
            "dropoff_latitude": float(dropoff_latitude),
            "passenger_count": int(passenger_count)
    }, index=[0])

    return X_pred


df = predict(pickup_datetime,
            pickup_longitude,
            pickup_latitude,
            dropoff_longitude,
            dropoff_latitude,
            passenger_count)

st.write(df)


params = dict(
  pickup_datetime=df['pickup_datetime'],
  pickup_longitude=df['pickup_longitude'],
  pickup_latitude=-df['pickup_latitude'],
  dropoff_longitude=df['dropoff_longitude'],
  dropoff_latitude=-df['dropoff_latitude'],
  passenger_count=df['passenger_count']
)
url = 'https://taxifare.lewagon.ai/predict'

if url == 'https://taxifare.lewagon.ai/predict':
    response = requests.get(
        url,
        params=params
        )

if response.status_code == 200:
    print("API call success")
else:
    print("API call error")

st.write(round(response.json().get('fare'),2))

data = {'lat':[float(pickup_longitude),float(dropoff_longitude)],
        'lon': [float(pickup_latitude), float(dropoff_latitude)]}
map_df = pd.DataFrame.from_dict(data)

st.map(map_df)
