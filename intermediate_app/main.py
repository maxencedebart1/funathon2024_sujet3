"""
First version of a visualisation app for FlightRadar24 data.
"""
import dash
from dash import html, dcc, Output, Input
import dash_leaflet as dl
from FlightRadar24 import FlightRadar24API
from utils import fetch_flight_data


# App initialization
app = dash.Dash(__name__)
# FlightRadar24API client
fr_api = FlightRadar24API()

# Map children default is an OpenStreetMap tiles layer
default_map_children = [
    dl.TileLayer()
]

# App layout
app.layout = html.Div([
    dl.Map(
        id='map',
        center=[45, 0],
        zoom=6,
        style={'width': '100%', 'height': '800px'},
        children=default_map_children
    ),
    dcc.Interval(
        id="interval-component",
        interval=2*1000,  # in milliseconds
        n_intervals=0
    )
])


@app.callback(
    Output('map', 'children'),
    Input('interval-component', 'n_intervals'),
)
def update_graph_live(n):
    # Retrieve a list of flight dictionaries with 'latitude', 'longitude' and 'id' keys
    data = fetch_flight_data(
        client=fr_api,
        airline_icao="AFR",
        zone_str="europe"
    )

    # TO MODIFY: Update map children by adding markers to the default tiles layer
    children = default_map_children + [
        dl.Marker(
            id=flight['id'],
            position=[flight['latitude'], flight['longitude']],
            children=[dl.Popup(content=f"Id: {flight['id']}")],
        ) for flight in data
    ]

    return children


if __name__ == '__main__':
    app.run_server(
        debug=True, port=5000, host='0.0.0.0'
    )
