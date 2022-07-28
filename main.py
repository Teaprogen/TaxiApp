
from turtle import distance
import requests
import uvicorn
from fastapi import FastAPI
from requests import request
from requests.structures import CaseInsensitiveDict

app = FastAPI()


def place_to_latlon(place: str):
    url = f"https://api.geoapify.com/v1/geocode/search?text={place}&apiKey=b9ef4a8d94ca4e15ac4b658cd9908605"
    resp = requests.get(url)
    resp_json = resp.json()
    lat = resp_json['features'][0]['properties']['lat']
    lon = resp_json['features'][0]['properties']['lon']
    return [lat, lon]


def get_price_of_ride(loc1: list, loc2: list):
    url = "https://api.geoapify.com/v1/routematrix?apiKey=b9ef4a8d94ca4e15ac4b658cd9908605"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    data = '{"mode":"drive","sources":[{"location":['+str(loc1[1])+','+str(
        loc1[0])+']}],"targets":[{"location":['+str(loc2[1])+','+str(loc2[0])+']}]}'
    resp = requests.post(url, headers=headers, data=data).json()
    distance_of_ride = resp['sources_to_targets'][0][0]['distance']
    uklon_price = distance_of_ride * 0.022
    uber_price = distance_of_ride * 0.035
    bolt_price = distance_of_ride * 0.025
    result = {'distance': distance_of_ride,
              'units': "meters",
              'currency': "UAH",
              'uber_price': uber_price,
              'uklon_price': uklon_price,
              'bolt_price': bolt_price}
    return result


@app.get("/")
def read_root():
    return "go to /docs"


@app.get("/taxi/")
def get_price(location1: str, location2: str):
    locLatLon1 = place_to_latlon(location1)
    locLatLon2 = place_to_latlon(location2)
    price_of_ride = get_price_of_ride(locLatLon1, locLatLon2)
    return price_of_ride


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
