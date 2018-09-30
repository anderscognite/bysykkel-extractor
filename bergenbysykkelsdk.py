import requests, os
from bysykkel import Station

def get(url):
	headers = {}
	params = {}
	cookies = {}
	
	res = requests.get(url, params=params, headers=headers, cookies=cookies)
	if res.status_code == 200:
		data = res.json()
		return data
	else:
		raise RuntimeError(str(res.status_code)+' error') from error

def get_stations():
	data = get('http://gbfs.urbansharing.com/bergen-city-bike/station_information.json')['data']
	stations = []
	for station in data["stations"]:
		stations.append(Station(
			station_id=station['station_id'],
			name=station['name'],
			subtitle=station['address'],
			longitude=station['lon'],
			latitude=station['lat']
		))
	return stations

def get_availability():
	return get('stations/availability')