from typing import Optional, Tuple, Union
import logging


def extract_coordinates(url: str) -> Tuple[Optional[float], Optional[float]]:
    """Given Google maps url with coordinates in a query string extract latitude and longitude"""
    try:
        coordinates = url.split('q=')[-1]
        y, x = [coor.strip() for coor in coordinates.split(',')]
    except AttributeError:
        return None, None
    try:
        lat = float(y)
    except ValueError as e:
        logging.error(f'{e} {y}')
        lat = None # type: ignore
    try:
        lon = float(x)
    except ValueError as e:
        logging.error(f'{e} {x}')
        lon = None # type: ignore
    return lat, lon


def extract_latitude(url: str) -> Optional[float]:
    """Given Google maps url with coordinates in a query string extract latitude and longitude"""
    try:
        coordinates = url.split('q=')[-1]
        lat, _ = [coor.strip() for coor in coordinates.split(',')]
    except AttributeError:
        return None
    try:
        return float(lat)
    except ValueError as e:
        logging.error(f'{e} {lat}')
        return None


def extract_longitude(url: str) -> Optional[float]:
    """Given Google maps url with coordinates in a query string extract latitude and longitude"""
    try:
        coordinates = url.split('q=')[-1]
        _, lon = [coor.strip() for coor in coordinates.split(',')]
    except AttributeError:
        return None
    try:
        return float(lon)
    except ValueError as e:
        logging.error(f'{e} {lon}')
        return None


def extract_status(status: str) -> str:
    """Given long status string extract only keyword of interest: expired, valid, withdrawn."""
    # Always last word in the string then remove trailing dot
    return status.split(' ')[-1].strip('.')
