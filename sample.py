import os

from cognite.v05.assets import get_asset_subtree
from cognite.config import configure_session
import argparse,json,time,threading

from bysykkel import find_or_create_root_assets
import oslobysykkelsdk as oslo
import bergenbysykkelsdk as bergen
import trondheimbysykkelsdk as trondheim

def create_id_mapping(assets):
	id_mapping = {}
	for city, data in cities.items():
		for asset in data['assets']:
			if 'metadata' in asset.keys():
				bysykkel_id = int(asset['metadata']['bysykkel_id'].replace('"', ''))
				id_mapping[bysykkel_id] = {'assetId': asset['id'], 'assetName': asset['name']}
	return id_mapping

def get_timeseries_ids(cities):
	city_ids = []
	for city, data in cities.items():
		city_ids.append(data['id'])
	return get_timeseries(path=json.dumps(city_ids))
	
def find_all_assets(cities):
	for city, data in cities.items():
		city_id = data['asset_id']
		data['assets'] = get_asset_subtree(asset_id = city_id).to_json()

# def sample_availability():
# 	try:
# 		availability = get_availability()
# 		datapoints = []

# 		for station in availability['stations']:
# 			bysykkel_id = station['id']
# 			numBikes = station['availability']['bikes']
# 			numLocks = station['availability']['locks']
			
# 			if bysykkel_id in id_mapping:
# 				bikesAssetName = id_mapping[bysykkel_id]['assetName']+'_bikes'
# 				locksAssetName = id_mapping[bysykkel_id]['assetName']+'_locks'
# 				timestamp = int(time.time()*1000)
# 				datapoints.append(TimeseriesWithDatapoints(bikesAssetName, [Datapoint(timestamp, numBikes)]))
# 				datapoints.append(TimeseriesWithDatapoints(locksAssetName, [Datapoint(timestamp, numLocks)]))
# 		timestamp = int(time.time()*1000)
# 		print('Posting %d data points' % len(datapoints))
# 		print('Now is ', timestamp)
# 		post_multi_tag_datapoints(datapoints)
# 	except:
# 		print('Error')
# 	threading.Timer(1.0, sample_availability).start()


# Set API key and project for current session
configure_session(api_key=os.getenv('COGNITE_API_KEY_AH'), project='andershaf')

# Find root assets
cities = {
	'Oslo': {'stations': oslo.get_stations()},
	'Bergen': {'stations': bergen.get_stations()},
	'Trondheim': {'stations': trondheim.get_stations()}
}
find_or_create_root_assets(cities)
find_all_assets(cities)
id_mapping = create_id_mapping(cities)
print(id_mapping)
# timeseries_ids = getTimeseriesIds()

#fetchAvailability()