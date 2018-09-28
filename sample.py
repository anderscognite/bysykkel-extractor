import os
import subprocess

from cognite.config import configure_session
from cognite.v05.assets import get_assets, post_assets, get_asset_subtree, delete_assets
from cognite.v05.timeseries import post_time_series, get_timeseries, post_multi_tag_datapoints
from cognite.v05.dto import Asset, TimeSeries, Datapoint, TimeseriesWithDatapoints
from bysykkelsdk import get_stations, get_availability, delete_request
import os.path
import argparse,json,time,threading

bysykkel_asset_parent_id = 6764981534423173

def deleteAllAssets():
	assets = get_asset_subtree(asset_id = bysykkel_asset_parent_id).to_json()
	asset_ids = []
	for asset in assets:
		if asset["id"] != bysykkel_asset_parent_id:
			asset_ids.append(asset["id"])

	if len(asset_ids) > 0:
		delete_assets(asset_ids)

def createAssets():
	assets = []
	names = {}
	for station in get_stations():
		metadata = {}
		metadata["bysykkel_id"] = json.dumps(station.id)
		i = 1
		name = station.title
		while name in names:
			name = station.title+" "+str(i)
			i += 1
		names[name] = True
		assets.append(Asset(name, parent_id=bysykkel_asset_parent_id, description=station.subtitle, metadata=metadata))

	post_assets(assets)

def createTimeseries():
	assets = get_asset_subtree(asset_id = bysykkel_asset_parent_id).to_json()
	timeseriesList = []
	for asset in assets:
		if 'metadata' in asset.keys():
			timeseries_bikes = TimeSeries(name = asset['name']+'_bikes', asset_id=asset['id'], step=True)
			timeseriesList.append(timeseries_bikes)

			timeseries_locks = TimeSeries(name = asset['name']+'_locks', asset_id=asset['id'], step=True)
			timeseriesList.append(timeseries_locks)
			
	post_time_series(timeseriesList)

def createIdMapping(assets):
	id_mapping = {}
	for asset in assets:
		if 'metadata' in asset.keys():
			bysykkel_id = int(asset['metadata']['bysykkel_id'])
			id_mapping[bysykkel_id] = {'assetId': asset['id'], 'assetName': asset['name']}
	return id_mapping

def getTimeseriesIds():
	return get_timeseries(path=json.dumps([bysykkel_asset_parent_id]))

def fetchAvailability():
	try:
		availability = get_availability()
		datapoints = []

		for station in availability['stations']:
			bysykkel_id = station['id']
			numBikes = station['availability']['bikes']
			numLocks = station['availability']['locks']
			
			if bysykkel_id in id_mapping:
				bikesAssetName = id_mapping[bysykkel_id]['assetName']+'_bikes'
				locksAssetName = id_mapping[bysykkel_id]['assetName']+'_locks'
				timestamp = int(time.time()*1000)
				datapoints.append(TimeseriesWithDatapoints(bikesAssetName, [Datapoint(timestamp, numBikes)]))
				datapoints.append(TimeseriesWithDatapoints(locksAssetName, [Datapoint(timestamp, numLocks)]))
		timestamp = int(time.time()*1000)
		print('Posting %d data points' % len(datapoints))
		print('Now is ', timestamp)
		#post_multi_tag_datapoints(datapoints)
	except:
		print('Error')
	threading.Timer(1.0, fetchAvailability).start()


# Set API key and project for current session
configure_session(api_key=os.getenv('COGNITE_API_KEY_AH'), project='andershaf')

if False:
	# Setup all assets
	#deleteAllAssets()
	createAssets()
	createTimeseries()
else:
	assets = get_asset_subtree(asset_id = bysykkel_asset_parent_id).to_json()
	id_mapping = createIdMapping(assets)
	timeseries_ids = getTimeseriesIds()

	fetchAvailability()