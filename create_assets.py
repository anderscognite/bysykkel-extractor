import os, argparse, json

from cognite.config import configure_session
from cognite.v05.assets import post_assets, get_asset_subtree, delete_assets
from cognite.v05.dto import Asset
from bysykkel import Station, find_or_create_asset, find_or_create_root_assets
import oslobysykkelsdk as oslo
import bergenbysykkelsdk as bergen

parser = argparse.ArgumentParser()
parser.add_argument('--apikey', type=str, required=True)
parser.add_argument('--project', type=str, required=True)
parser.add_argument('--delete_stations', action='store_true')
parser.add_argument('--create_stations', action='store_true')
args = parser.parse_args()

def delete_stations(cities):
	# delete all stations for given cities
	asset_ids = []

	for city, data in cities.items():
		assets = get_asset_subtree(asset_id = data['assetId']).to_json()
		
		for asset in assets:
			if asset["id"] != city['assetId']:
				asset_ids.append(asset["id"])

	if len(asset_ids) > 0:
		delete_assets(asset_ids)

def find_name_for_station(name, existingNames):
	# Some names are duplicates, append number to get unique numbers
	i = 1
	newName = name
	while newName in existingNames:
		newName = name+" "+str(i)
		i += 1
	existingNames[newName] = True
	return newName

def create_assets(cities):
	assets = []
	names = {}
	for city, data in cities.items():
		city_id = data['asset_id']
		for station in data['stations']:
			# We will store the station id as metadata.
			# Would rather use source and sourceId, but Python SDK doesn't support it yet.
			metadata = {}
			metadata["bysykkel_id"] = json.dumps(station.id)
			name = find_name_for_station(station.name, names) # Avoid duplicate names
			assets.append(Asset(name, parent_id=city_id, description=station.subtitle, metadata=metadata))
	print('Creating assets in CDP')
	post_assets(assets)
	print('Done')

# Set API key and project for current session
configure_session(api_key=args.apikey, project=args.project)

# Setup all assets
cities = {
	'Oslo': {'stations': oslo.get_stations()},
	'Bergen': {'stations': bergen.get_stations()}
}
find_or_create_root_assets(cities)

if args.delete_stations:
	delete_stations(cities)
	
if args.create_stations:
	try:
		create_assets(cities)
	except Exception as e:
		print('Error creating assets: ' + str(e))
	print('This could be that there already exists assets with name conflicts.')