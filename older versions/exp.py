import geopandas as gpd

# Load the GeoJSON file for USA
usa_data = gpd.read_file("EU.geojson")
c_data = gpd.read_file("china.geojson")

# Print the column names to check
print(usa_data.columns)
print(c_data.columns)
