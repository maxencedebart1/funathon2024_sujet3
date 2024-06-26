import dash
from dash import dcc
from dash import html
import dash_leaflet as dl
from dash.dependencies import Output, Input, State
from FlightRadar24 import FlightRadar24API
from utils import (
    update_rotation_angles,
    get_closest_round_angle,
    get_custom_icon,
    fetch_flight_data
)


# App initialization
app = dash.Dash(__name__)
# FlightRadar24API client
fr_api = FlightRadar24API()


default_map_children = [
    dl.TileLayer()
]


app.layout = html.Div([
    # The memory store reverts to the default on every page refresh
    dcc.Store(id="memory"),
    # The local store will take the initial data
    # only the first time the page is loaded
    # and keep it until it is cleared.
    dcc.Store(id="local", storage_type="local"),
    # Same as the local store but will lose the data
    # when the browser/tab closes.
    dcc.Store(id="session", storage_type="session"),
    dl.Map(
        id='map',
        center=[56, 10],
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
    [Output('map', 'children'), Output('memory', 'data')],
    [Input('interval-component', 'n_intervals')],
    [State('memory', 'data')]
)
def update_graph_live(n, previous_data):
    # Retrieve a list of flight dictionaries with 'latitude', 'longitude' and 'id' keys
    data = fetch_flight_data(client=fr_api, airline_icao="AFR", zone_str="europe")
    # Add a rotation_angle key to dictionaries
    if previous_data is None:
        for flight_data in data:
            flight_data.update(rotation_angle=0)
    else:
        update_rotation_angles(data, previous_data)

    # Update map children by adding markers to the default tiles layer
    children = default_map_children + [
        dl.Marker(
            id=flight['id'],
            position=[flight['latitude'], flight['longitude']],
            # TO MODIFY
            children=[
                dl.Popup(html.Div([
                    dcc.Markdown(f'''
                        Le vol au départ de {flight['origin_airport_iata']}
                        et à destination de {flight['destination_airport_iata']}
                        a une vitesse au sol de {flight['speed']} noeuds.
                    ''')
                ]))
            ],
            icon=get_custom_icon(
                get_closest_round_angle(flight['rotation_angle'])
            ),
        ) for flight in data
    ]

    return [children, data]


if __name__ == '__main__':
    app.run_server(
        debug=True, port=5000, host='0.0.0.0'
    )
