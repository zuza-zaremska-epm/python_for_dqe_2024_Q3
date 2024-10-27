# Create a tool which will calculate straight-line distance between different cities based on coordinates:
#  1. User will provide two city names by console interface
#  2. If tool do not know about city coordinates, it will ask user for input and store it in SQLite database for future use
#  3. Return distance between cities in kilometers
# Do not forgot that Earth is a sphere, so length of one degree is different.
from geo_calc import GeoCalculator

geo_calc = GeoCalculator()
geo_calc.create_geo_storage()


for city in range(2):
    geo_calc.get_city_details()
