# -*- coding: utf-8 -*-
# Copyright 2018-2019 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This app will assist you to avoid crowd gathering locations"""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

# LOADING DATA
DATE_TIME = "date/time"
DATA_URL = (
    "lat.csv"
)

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv('uber-raw-data-sep15.csv', nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data

data = load_data(800000)

# CREATING FUNCTION FOR MAPS

def map(data, lat, lon, zoom):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["lon", "lat"],
                radius=50,
                elevation_scale=2,
                elevation_range=[0, 200],
                pickable=True,
                extruded=True,
            ),
        ]
    ))

# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.beta_columns((2,3))

with row1_1:
    st.title("Dublic City Footfall Analsysis")
    hour_selected = st.slider("At what time you want to go out ?", 0, 23)

with row1_2:
    st.write(
    """
    ##
    .
    """)

# FILTERING DATA BY HOUR SELECTED
data = data[data[DATE_TIME].dt.hour == hour_selected]

# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
row2_1, row2_2, row2_3, row2_4 = st.beta_columns((2,1,1,1))

# SETTING THE ZOOM LOCATIONS FOR THE AIRPORTS
# la_guardia= [48.7900, -73.8700]
# jfk = [40.6650, -73.7821]
# newark = [40.7090, -74.1805]
# dublin = [53.3498, 6.2603]

bachelors_walk = [53.34719979, -6.260863323]
aston_quay = [53.34662,	-6.25982]
grafton_street = [53.34082,-6.26035]

zoom_level = 14
midpoint = (np.average(data["lat"]), np.average(data["lon"]))

with row2_1:
    st.write("**All Dublin City from %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
    map(data, midpoint[0], midpoint[1], 14)

with row2_2:
    st.write("**bachelors_walk**")
    map(data, bachelors_walk[0],bachelors_walk[1], zoom_level)

with row2_3:
    st.write("**aston_quay**")
    map(data, aston_quay[0],aston_quay[1], zoom_level)

with row2_4:
    st.write("**grafton_street**")
    map(data, grafton_street[0],grafton_street[1], zoom_level)




# # FILTERING DATA FOR THE HISTOGRAM
# filtered = data[
#     (data[DATE_TIME].dt.hour >= hour_selected) & (data[DATE_TIME].dt.hour < (hour_selected + 1))
#     ]

# hist = np.histogram(filtered[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]

# chart_data = pd.DataFrame({"minute": range(60), "footfall": hist})

# # LAYING OUT THE HISTOGRAM SECTION

# st.write("")

# st.write("**Breakdown of footfall per minute between %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))

# st.altair_chart(alt.Chart(chart_data)
#     .mark_area(
#         interpolate='step-after',
#     ).encode(
#         x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
#         y=alt.Y("pickups:Q"),
#         tooltip=['minute', 'footfall']
#     ).configure_mark(
#         opacity=0.5,
#         color='red'
#     ), use_container_width=True)




with row2_1:
    data = pd.read_csv("fuced2019.csv", index_col='Time', parse_dates=True)


    option = st.selectbox(
    'Select a place that you like to go ?',
        data.columns.values)

    'You selected: ', option

chart_data =  pd.read_csv("daily.csv", index_col='Time', parse_dates=True)


st.line_chart(chart_data[[option]])




with row2_2:
    option = st.selectbox(
    'How many people are you going with ?',
        [0,1,2,3,4,5,6,7,'10+'])



with row2_3:
    option = st.selectbox(
    'At what time ?',
        ['00:00-02:00', '00:02-04:00', '04:00-06:00', '06:00-08:00' ,'08:00-10:00' ,'10:00-12:00' ,'12:00-14:00' ,'14:00-16:00' ])