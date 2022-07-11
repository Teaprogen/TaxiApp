import requests
from requests.structures import CaseInsensitiveDict
place = "Kyiv"
api_key = 'b9ef4a8d94ca4e15ac4b658cd9908605'
url = f"https://api.geoapify.com/v1/geocode/search?text={place}&apiKey={api_key}"
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
resp = requests.get(url, headers=headers)
resp_json = resp.json()
lon = resp_json['features'][0]['properties']['lon']
lat = resp_json['features'][0]['properties']['lat']
print(lat, lon)
