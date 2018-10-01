import requests, os
from bysykkel import Station, Availability

def get(url):
	baseUrl = "https://oslobysykkel.no/api/v1/"
	url = baseUrl+url
	
	headers = {"Client-Identifier": os.getenv('BYSYKKEL_API_KEY')}
	params = {}
	cookies = {}
	
	res = requests.get(url, params=params, headers=headers, cookies=cookies)
	if res.status_code == 200:
		data = res.json()
		return data
	else:
		raise RuntimeError(str(res.status_code)+' error') from error

def get_stations():
	data = get('stations')
	stations = []
	for station in data["stations"]:
		stations.append(Station(
			station_id=station['id'],
			name=station['title'],
			subtitle=station['subtitle'],
			longitude=station['center']['longitude'],
			latitude=station['center']['latitude']
		))
	return stations

def get_availability():
	data = get('stations/availability')
	stations = []
	for station in data["stations"]:
		stations.append(Availability(
			station_id=station['id'],
			bikes=station['availability']['bikes'],
			locks=station['availability']['locks']
		))
	return stations