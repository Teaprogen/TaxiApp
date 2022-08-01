

import requests
import uvicorn
from turtle import distance
from urllib import error
from fastapi import FastAPI, HTTPException
from requests import request
from requests.structures import CaseInsensitiveDict
from fastapi.responses import RedirectResponse

app = FastAPI()


def place_to_latlon(place: str):
    url = f"https://api.geoapify.com/v1/geocode/search?text={place}&apiKey=b9ef4a8d94ca4e15ac4b658cd9908605"
    resp = requests.get(url)
    if resp.status_code == 401:
        raise HTTPException(
            status_code=400, detail="Bad request: wrong place address")
    resp_json = resp.json()
    lat = resp_json['features'][0]['properties']['lat']
    lon = resp_json['features'][0]['properties']['lon']
    return [lat, lon]


def get_price_of_ride(loc1: list, loc2: list):
    waypoints1 = str(loc1[0])+","+str(loc1[1])
    waypoints2 = str(loc2[0])+","+str(loc2[1])
    url = "https://api.geoapify.com/v1/routing?waypoints={waypoints}&mode=drive&apiKey=b9ef4a8d94ca4e15ac4b658cd9908605".format(
        waypoints=waypoints1+"|"+waypoints2)
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    resp = requests.get(url, headers=headers).json()
    distance_of_ride = resp["features"][0]["properties"]["distance"]
    time_in_route = resp["features"][0]["properties"]["time"]
    if distance_of_ride == 0:
        raise HTTPException(
            status_code=400, detail="Bad request: distance is zero or no route is found")
    uklon_price = distance_of_ride * 0.01087 + 49
    uber_price = distance_of_ride * 0.01217 + 49
    bolt_price = distance_of_ride * 0.01117 + 49
    result = {'distance': distance_of_ride,
              'units': "meters",
              'time_in_seconds': time_in_route,
              'currency': "UAH",
              'uber_price': format(uber_price, ".2f"),
              'uklon_price': format(uklon_price, ".2f"),
              'bolt_price': format(bolt_price, ".2f")}
    return result


@app.get("/")
def read_root():
    return RedirectResponse("/docs")

@app.get("/taxi/")
async def get_price(location1: str, location2: str):
    locLatLon1 = place_to_latlon(location1)
    locLatLon2 = place_to_latlon(location2)
    price_of_ride = get_price_of_ride(locLatLon1, locLatLon2)
    return price_of_ride


if __name__ == "__main__":
    uvicorn.run("main:app")
