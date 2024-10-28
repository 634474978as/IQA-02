import pandas as pd

class AssetInventory:
    def __init__(self):
        self.assets = pd.DataFrame(columns=[
            'Asset ID', 'Asset Name', 'Location', 'Condition',
            'Installation Date', 'Value ($)', 'Last Maintenance',
            'Geotab Device ID', 'Latitude', 'Longitude', 'Speed', 'Engine Status'
        ])

    def add_asset(self, asset_id, asset_name, location, condition, installation_date, value, last_maintenance, geotab_device_id=None):
        new_asset = pd.DataFrame({
            'Asset ID': [asset_id],
            'Asset Name': [asset_name],
            'Location': [location],
            'Condition': [condition],
            'Installation Date': [installation_date],
            'Value ($)': [value],
            'Last Maintenance': [last_maintenance],
            'Geotab Device ID': [geotab_device_id],
            'Latitude': [None],
            'Longitude': [None],
            'Speed': [None],
            'Engine Status': [None]
        })
        self.assets = pd.concat([self.assets, new_asset], ignore_index=True)
    
    def search_assets(self, search_query):
        if search_query:
            return self.assets[self.assets.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
        return self.assets

    def sort_assets(self, sort_by, ascending=True):
        return self.assets.sort_values(by=sort_by, ascending=ascending)
    
    def search_and_sort_assets(self, search_query=None, sort_by=None, ascending=True):
        filtered_assets = self.search_assets(search_query)
        if sort_by:
            return filtered_assets.sort_values(by=sort_by, ascending=ascending)
        return filtered_assets
    
    def display_assets(self):
        return self.assets
    def update_assets_from_geotab(self, geotab_api):
        device_statuses = geotab_api.get_device_status()
        for status in device_statuses:
            device_id = status['device']['id']
            latitude = status.get('latitude')
            longitude = status.get('longitude')
            speed = status.get('speed')
            engine_status = status['device'].get('isCommunicating')
            # Find the asset with the matching Geotab Device ID
            mask = self.assets['Geotab Device ID'] == device_id
            if mask.any():
                idx = self.assets.index[mask][0]
                self.assets.at[idx, 'Latitude'] = latitude
                self.assets.at[idx, 'Longitude'] = longitude
                self.assets.at[idx, 'Speed'] = speed
                self.assets.at[idx, 'Engine Status'] = engine_status
            else:
                # Optionally, add new assets to the inventory
                pass

'''
# Example usage of Inventory
# Initialize
inventory = AssetInventory()

# Add some assets to the inventory
inventory.add_asset(101, 'Water Pipe', 'Street A', 'Good', '2010-06-15', 5000, '2021-01-15')
inventory.add_asset(102, 'Street Light', 'Street B', 'Poor', '2015-08-25', 1200, '2020-10-18')
inventory.add_asset(103, 'Fire Hydrant', 'Street C', 'Good', '2012-12-05', 1500, '2022-02-05')
inventory.add_asset(104, 'Road Segment', 'Street D', 'Fair', '2009-03-22', 20000, '2019-05-10')
inventory.add_asset(105, 'Park Bench', 'Street E', 'Poor', '2018-07-10', 800, '2020-11-20')

# Search for assets with 'Poor' condition and sort by 'Value ($)' in descending order
result = inventory.search_and_sort_assets(search_query='Poor', sort_by='Value ($)', ascending=False)

# Display the search and sort result
print(result)

'''


########################################################

import requests
import json

class GeotabAPI:
    def __init__(self, username, password, database):
        self.server = 'my.geotab.com'
        self.credentials = None
        self.username = "a42shen@uwaterloo.ca"
        self.password = "QAZwsx548847+"
        self.database = "IQA_02"
        self.authenticate()

    def authenticate(self):
        url = f'https://{self.server}/apiv1'
        headers = {'Content-Type': 'application/json'}
        payload = {
            'method': 'Authenticate',
            'params': {
                'userName': self.username,
                'password': self.password,
                'database': self.database
            },
            'id': -1
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        data = response.json()
        if 'error' in data:
            raise Exception(f"Authentication failed: {data['error']}")
        self.credentials = data['result']['credentials']

    def get_device_status(self):
        url = f'https://{self.server}/apiv1'
        headers = {'Content-Type': 'application/json'}
        payload = {
            'method': 'Get',
            'params': {
                'typeName': 'DeviceStatusInfo',
                'credentials': self.credentials
            },
            'id': -1
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        data = response.json()
        if 'error' in data:
            raise Exception(f"Error fetching device status: {data['error']}")
        return data['result']


# Sample usage of Geotab
# Initialize the inventory
inventory = AssetInventory()

# Add assets (including Geotab Device IDs)
inventory.add_asset(101, 'Water Pipe', 'Street A', 'Good', '2010-06-15', 5000, '2021-01-15')
inventory.add_asset(102, 'Maintenance Vehicle', 'Depot', 'Good', '2015-08-25', 12000, '2021-06-18', geotab_device_id='b123')
inventory.add_asset(103, 'Snow Plow', 'Depot', 'Good', '2018-12-05', 25000, '2022-01-05', geotab_device_id='c456')

# Set up Geotab API
geotab_api = GeotabAPI('YOUR_USERNAME', 'YOUR_PASSWORD', 'YOUR_DATABASE')

# Update inventory with Geotab data
inventory.update_assets_from_geotab(geotab_api)

# Display the updated assets
print(inventory.display_assets())


