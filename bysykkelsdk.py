import requests, os

class Station():
	def __init__(self, data):
		self.id = data["id"]
		self.in_service = data["in_service"]
		self.title = data["title"]
		self.subtitle = data["subtitle"]
		self.number_of_locks = data["number_of_locks"]
		self.center = data["center"]
		self.bounds = data["bounds"]
	def __repr__(self):
		return 'Asset: '+self.title

def get_request(url):
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

def delete_request(url):
	baseUrl = "https://api.cognitedata.com/api/0.5/"
	url = baseUrl+url
	
	headers = {"api-key": os.getenv('COGNITE_API_KEY_AH')}
	params = {}
	cookies = {}
	
	res = requests.delete(url, params=params, headers=headers, cookies=cookies)
	
def get_stations():
	data = get_request('stations')
	stations = []
	for station in data["stations"]:
		stations.append(Station(station))
	return stations

def get_availability():
	return get_request('stations/availability')