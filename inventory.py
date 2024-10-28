import pandas as pd

class AssetInventory:
    def __init__(self):
        self.assets = pd.DataFrame(columns=['Asset ID', 'Asset Name', 'Location', 'Condition', 'Installation Date', 'Value ($)', 'Last Maintenance'])

    def add_asset(self, asset_id, asset_name, location, condition, installation_date, value, last_maintenance):
        new_asset = pd.DataFrame({
            'Asset ID': [asset_id],
            'Asset Name': [asset_name],
            'Location': [location],
            'Condition': [condition],
            'Installation Date': [installation_date],
            'Value ($)': [value],
            'Last Maintenance': [last_maintenance]
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


# Example usage
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


