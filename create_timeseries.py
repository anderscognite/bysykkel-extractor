import os, argparse, json

from cognite.config import configure_session
from cognite.v05.assets import get_asset_subtree
from cognite.v05.timeseries import post_time_series, get_timeseries
from cognite.v05.dto import TimeSeries
from bysykkel import Station, find_or_create_asset, find_or_create_root_assets
import oslobysykkelsdk as oslo
import bergenbysykkelsdk as bergen
import trondheimbysykkelsdk as trondheim

parser = argparse.ArgumentParser()
parser.add_argument('--apikey', type=str, required=True)
parser.add_argument('--project', type=str, required=True)
parser.add_argument('--delete_timeseries', action='store_true')
parser.add_argument('--create_timeseries', action='store_true')
args = parser.parse_args()

# Set API key and project for current session
configure_session(api_key=args.apikey, project=args.project)

def delete_timeseries(cities):
	# TODO: implement
	print('delete_timeseries is not yet implemented')

def create_timeseries(cities):
	timeseries = []

	for city, data in cities.items():
		city_id = data['asset_id']
		assets = get_asset_subtree(asset_id = city_id).to_json()
		for asset in assets:
			timeseries_bikes = TimeSeries(name = asset['name']+'_bikes', asset_id=asset['id'], step=True)
			timeseries.append(timeseries_bikes)

			timeseries_locks = TimeSeries(name = asset['name']+'_locks', asset_id=asset['id'], step=True)
			timeseries.append(timeseries_locks)
	print('Creating timeseries in CDP')
	post_time_series(timeseries)
	print('Done')

# Find root assets
cities = {
	'Oslo': {'stations': oslo.get_stations()},
	'Bergen': {'stations': bergen.get_stations()},
	'Trondheim': {'stations': trondheim.get_stations()}
}
find_or_create_root_assets(cities)

if args.delete_timeseries:
	delete_timeseries(cities)
	
if args.create_timeseries:
	try:
		create_timeseries(cities)
	except Exception as e:
		print('Error creating timeseries: ' + str(e))
