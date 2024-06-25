"""
Utils.
"""
from typing import Dict, Optional, List
from FlightRadar24 import FlightRadar24API


def fetch_flight_data(
    client: FlightRadar24API,
    airline_icao: Optional[str] = None,
    aircraft_type: Optional[str] = None,
    zone_str: Optional[str] = None
) -> List[Dict]:
    """
    Fetch flight data from FlightRadar24 API for
    a given airline, aircraft type and zone.

    Args:
        client (FlightRadar24API): FlightRadar24API client.
        airline_icao (str): ICAO code of the airline.
        aircraft_type (str): Type of aircraft.
        zone_str (str): Zone string.

    Returns:
        List[Dict]: List of flights. A flight should be represented
            as a dictionary with latitude, longitude and id keys.
    """
    zone_de_vol = client.get_zones()[zone_str]
    bounds = client.get_bounds(zone_de_vol)
    vols = client.get_flights(aircraft_type=aircraft_type, airline=airline_icao, bounds=bounds)
    return [{"latitude": vol.latitude,
             "longitude": vol.longitude,
             "id": vol.id,
             } for vol in vols
            ]
