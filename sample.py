import os

from cognite.v05.assets import get_asset_subtree
from cognite.v05.timeseries import post_multi_tag_datapoints
from cognite.v05.dto import TimeseriesWithDatapoints, Datapoint
from cognite.config import configure_session
import argparse, json, time, datetime

from bysykkel import find_or_create_root_assets
import oslobysykkelsdk as oslo
import bergenbysykkelsdk as bergen
import trondheimbysykkelsdk as trondheim

print('Initializing bysykkel sampler ...')

def find_all_assets(cities):
	# Find all assets representing city bike stations
	for city, data in cities.items():
		city_id = data['asset_id']
		data['assets'] = get_asset_subtree(asset_id = city_id).to_json()

def create_id_mapping(cities):
	# Create mapping between city bike station id's to asset id's
	for city, data in cities.items():
		id_mapping = {}
		for asset in data['assets']:
			if 'metadata' in asset.keys():
				bysykkel_id = int(asset['metadata']['bysykkel_id'].replace('"', ''))
				id_mapping[bysykkel_id] = {'asset_id': asset['id'], 'asset_name': asset['name']}
		data['id_mapping'] = id_mapping
		
def sample(cities):
	# Sample bike availability for all cities
	for city, data in cities.items():
		try:
			datapoints = []
			for station in data['get_availability']():
				bysykkel_id = station.id
				num_bikes = station.bikes
				num_locks = station.locks
				
				if bysykkel_id in data['id_mapping']:
					bikes_asset_name = data['id_mapping'][bysykkel_id]['asset_name']+'_bikes'
					locks_asset_name = data['id_mapping'][bysykkel_id]['asset_name']+'_locks'
					timestamp = int(time.time()*1000)
					datapoints.append(TimeseriesWithDatapoints(bikes_asset_name, [Datapoint(timestamp, num_bikes)]))
					datapoints.append(TimeseriesWithDatapoints(locks_asset_name, [Datapoint(timestamp, num_locks)]))
			timestamp = int(time.time()*1000)
			print(datetime.datetime.now(), 'Posting %d data points' % len(datapoints), ' for ', city, ' at ', timestamp)
			post_multi_tag_datapoints(datapoints)
		except Exception as e:
			print('Error fetching availaility for ', city, ': ' + str(e))

# Set API key and project for current session
configure_session(api_key=os.getenv('COGNITE_API_KEY'), project=os.getenv('COGNITE_PROJECT'))

# Find root assets
cities = {
	'Oslo': {'stations': oslo.get_stations(), 'get_availability': oslo.get_availability},
	'Bergen': {'stations': bergen.get_stations(), 'get_availability': bergen.get_availability},
	'Trondheim': {'stations': trondheim.get_stations(), 'get_availability': trondheim.get_availability}
}
print('Finding root assets')
find_or_create_root_assets(cities)
print('Finding all assets')
find_all_assets(cities)
print('Creating id mapping')
create_id_mapping(cities)
print('Starting sampling ...')
while True:
	sample(cities)
	time.sleep(5)