import pyodbc
import sqlite3

from geopy.distance import geodesic


class DatabaseManager:
    """Perform actions on sqlite database."""
    def __init__(self, db_name: str, db_configuration: dict):
        self.conn = None
        self.db_name = db_name
        self.db_configuration = db_configuration
        self.create_database()

    def create_database(self):
        """Create new database with defined name if not exists."""
        conn = sqlite3.connect(f'{self.db_name}.db')
        conn.close()

    def connect_to_database(self):
        """Connect to the database."""
        self.conn = pyodbc.connect("Driver=Devart ODBC Driver for SQLite;"f"Database={self.db_name}.db", autocommit=True)
        print(f'Connected to "{self.db_name}" database.')

    def disconnect_from_database(self):
        """Disconnect from the database."""
        self.conn.close()
        print(f'Disconnected from "{self.db_name}" database.')

    def create_database_structure(self):
        """Create database tables with the given database configuration."""
        for table_name, columns_details in self.db_configuration.items():
            self.create_table(table_name, columns_details)

    def create_table(self, table_name: str, table_configuration: dict):
        """
        Creates table with given configuration.
        :param table_name: name of the table
        :param table_configuration: columns names with their datatype
        """
        columns_details = [f'{column_name} {datatype}' for column_name, datatype in table_configuration.items()]
        columns_config = ', '.join(columns_details)

        cursor = self.conn.cursor()
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_config});')
        cursor.close()

        print(f'Created "{table_name}" table.')

    def check_for_duplicates(self, table_name: str = None, conditions: dict = None):
        """
        Checks if in the table data already exists.
        :param table_name: name of the table
        :param conditions: collection of record details
        """
        if conditions:
            conditions = [f"{column_name} = {value}" for column_name, value in conditions.items()]
            sql_check = f"""
            SELECT COUNT(*)
            FROM {table_name}
            WHERE {" AND ".join(conditions)};"""

            cursor = self.conn.cursor()
            cursor.execute(sql_check)
            result = cursor.fetchone()[0]
            cursor.close()

            if result == 0:
                return True
            else:
                return False

    def save_data(self, details: dict):
        """
        Inserts data into matching table.
        :param details: data for insertion
        """
        table_name = details.get('table_name')
        conditions = details.get('conditions')

        if table_name and conditions:
            if self.check_for_duplicates(table_name, conditions):
                values = [str(value) for value in conditions.values()]

                sql_insert = f"""
                INSERT INTO {table_name} ({", ".join(conditions.keys())})
                VALUES ({", ".join(values)});"""

                try:
                    cursor = self.conn.cursor()
                    cursor.execute(sql_insert)
                    cursor.close()

                    print('Data saved.')
                except pyodbc.Error as e:
                    print(f"Error: {e}")

    def fetch_data(self, details: dict):
        table_name = details['table_name']
        filters = details['filters']

        sql_fetch = f"""
        SELECT *
        FROM {table_name}
        WHERE {' AND '.join(filters)};"""

        cursor = self.conn.cursor()
        cursor.execute(sql_fetch)
        fetched_data = cursor.fetchall()
        cursor.close()

        return fetched_data


class GeoCalculator:

    def __init__(self):
        self.storage = None
        self.cities_details = {}
        self.calculated_distances = []
        self.current_pair = []

    def create_geo_storage(self):
        """Create storage for geographic data."""
        db_structure_conf = {
            "cities": {
                "city_id": "INT PRIMARY KEY",
                "city_name": "TEXT",
                "longitude": "FLOAT",
                "latitude": "FLOAT"
            },
            'distances': {
                'distance_id': 'INT PRIMARY KEY',
                'city_a': 'TEXT',
                'city_b': 'TEXT',
                'distance_km': 'FLOAT'
            }
        }

        self.storage = DatabaseManager('geo_storage', db_structure_conf)
        self.storage.create_database()
        self.storage.connect_to_database()
        self.storage.create_database_structure()

    def get_city_details(self):
        """Get from the user city details."""
        city = input('Provide city name: ').upper()
        long, lat = self.get_city_coordinates(city)
        print(f'City {city}: long: {long}, lat: {lat}')
        self.cities_details[city] = {'longitude': long, 'latitude': lat}
        if city not in self.current_pair:
            self.current_pair.append(city)
            self.current_pair.sort()

    def get_city_coordinates(self, city_name):
        """
        Get city coordinates from the storage or
        from the user is missing and save in the storage.
        """
        query_details = {
            'table_name': 'cities',
            'filters': [f"UPPER(city_name) = '{city_name}'"]
        }
        results = self.storage.fetch_data(query_details)
        if results:
            row = results[0]
            return row.longitude, row.latitude
        else:
            while True:
                long = input(f'Provide {city_name} longitude: ')
                lat = input(f'Provide {city_name} latitude: ')
                try:
                    long = float(long)
                    lat = float(lat)

                    city_details = {
                        "table_name": "cities",
                        "conditions": {
                            "city_name": f"'{city_name}'",
                            "longitude": long,
                            "latitude": lat
                        }
                    }
                    self.storage.save_data(city_details)

                    return long, lat
                except TypeError:
                    print(TypeError)
                    print('Provided incorrect data - please try again.')

    def calculate_distance(self):
        """Calculate distance between the cities in the current pair."""
        cities_cords = []
        for city in self.current_pair:
            cords = self.cities_details[city]
            cities_cords.append(cords)

        # Coordinates for two locations (latitude, longitude)
        city_a = (cities_cords[0]['latitude'], cities_cords[0]['longitude'])
        city_b = (cities_cords[1]['latitude'], cities_cords[0]['longitude'])

        # Calculate the distance between given cities.
        distance_km = round(geodesic(city_a, city_b).kilometers, 2)
        distance_info = f'Distance between {" and ".join(self.current_pair)}: {distance_km} km.'
        print(distance_info)
        self.calculated_distances.append(distance_info)

        distance_details = {
            "table_name": "distances",
            "conditions": {
                "city_a": f"'{self.current_pair[0]}'",
                "city_b": f"'{self.current_pair[1]}'",
                "distance_km": distance_km
            }
        }
        self.storage.save_data(distance_details)
        self.current_pair.clear()

    def display_calculated_distances(self):
        """Display all calculated distances during current session."""
        for order, distance_info in enumerate(self.calculated_distances):
            print(f"{order+1}. {distance_info}")

    def display_longest_distance(self):
        """Display the longest calculated distance."""

        cursor = self.storage.conn.cursor()
        cursor.execute("SELECT * FROM distances ORDER BY distance_km DESC LIMIT 1;")
        row = cursor.fetchone()
        cursor.close()

        print(f'\nThe longest calculated distance is {row.distance_km} km between {row.city_a} and {row.city_b}.')
