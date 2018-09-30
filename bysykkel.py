from cognite.v05.assets import get_assets, post_assets, get_asset_subtree, delete_assets
from cognite.v05.dto import Asset

class Station():
	def __init__(self, station_id, name, subtitle, longitude, latitude):
		self.id = station_id
		self.name = name
		self.subtitle = subtitle
		self.longitude = longitude
		self.latitude = latitude
	def __repr__(self):
		return 'Station: '+self.name

def find_or_create_asset(name, description, parent_id = None):
	# Search for existing asset
	result = get_assets(name=name).to_json()
	if len(result) > 0:
		return result[0]['id']
	
	# Didn't find it, create new instead
	result = post_assets([Asset(name=name, parent_id=parent_id, description=description)]).to_json()
	return result[0]['id']

def find_or_create_root_assets(cities):
	# Create root asset to contain multiple cities
	root_id = find_or_create_asset(name='City bikes', description = 'City bikes data')
	print('Found root id: ', root_id)
	# Create assets for cities
	for city in cities.keys():
		asset_id = find_or_create_asset(name=city, description = 'City bikes in %s' % city, parent_id=root_id)
		cities[city]['asset_id'] = asset_id
		print(city, ' root asset has id: ', asset_id)